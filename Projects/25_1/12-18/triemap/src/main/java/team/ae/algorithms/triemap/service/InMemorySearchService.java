package team.ae.algorithms.triemap.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import team.ae.algorithms.triemap.dto.Centroid2D;
import team.ae.algorithms.triemap.dto.Centroid3D;
import team.ae.algorithms.triemap.dto.ElbowPoint;
import team.ae.algorithms.triemap.dto.Item;
import team.ae.algorithms.triemap.dto.KMeansResult;
import team.ae.algorithms.triemap.dto.LoadRequest;
import team.ae.algorithms.triemap.dto.Point2D;
import team.ae.algorithms.triemap.dto.Point3D;
import team.ae.algorithms.triemap.dto.SearchResultDto;
import team.ae.algorithms.triemap.dto.Visualization2D;
import team.ae.algorithms.triemap.dto.Visualization3D;
import team.ae.algorithms.triemap.dto.Visualization2DDto;
import team.ae.algorithms.triemap.dto.Visualization3DDto;
import team.ae.algorithms.triemap.util.TextVectorizer;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/**
 * In-memory search and clustering service.
 * <p>
 * Responsibilities:
 * 1) Load textual items from JSON (data.json or request payload).
 * 2) Vectorize items using Embeddings and run K-Means clustering.
 * 3) Provide cluster-aware semantic search using cosine similarity.
 * 4) Provide cluster inspection APIs.
 * 5) Collect cluster centroids and items via TSNE dimensional reduction for visualization.
 */
@Service
@RequiredArgsConstructor
public class InMemorySearchService {

    private final ObjectMapper objectMapper = new ObjectMapper();
    @Qualifier("gloveEmbeddingService")
    private final EmbeddingService embeddingService;
    private final KMeansService kMeansService;
    private final TSneService tSneService;

    /**
     * All items loaded in memory. Each item knows its clusterId and character vector.
     */
    private volatile List<Item> items = List.of();

    /**
     * Centroids produced by K-Means clustering.
     * centroids[clusterIndex] is the numeric vector of that cluster center.
     */
    private volatile double[][] centroids = new double[0][];

    /**
     * How many clusters we consider during search.
     * For example, if there are 10 clusters in total,
     * we may search only in the 3 best matching clusters.
     */
    private static final int MAX_CLUSTERS_TO_USE_IN_SEARCH = 3;

    /**
     * The maximum number of clusters (k) to be evaluated in the elbow method for
     * determining the optimal number of clusters in a dataset.
     */
    private static final int MAX_K_FOR_ELBOW = 10;

    // -------------------------------------------------------------------------
    // Loading
    // -------------------------------------------------------------------------

    /**
     * Loads items from classpath resource "static/data.json" and runs clustering.
     * This method is synchronized to avoid concurrent reloads that could
     * corrupt the shared items/centroids state.
     */
    public synchronized Map<String, Object> loadFromClasspath() {
        try (InputStream inputStream =
                     new ClassPathResource("static/data.json").getInputStream()) {

            LoadRequest request = objectMapper.readValue(inputStream, LoadRequest.class);
            return load(request);

        } catch (Exception exception) {
            throw new RuntimeException("Failed to load static/data.json", exception);
        }
    }

    /**
     * Loads items from request DTO, vectorizes them and runs K-Means clustering.
     * This method is synchronized to ensure that items and centroids are updated
     * atomically in a multi-threaded environment.
     */
    public synchronized Map<String, Object> load(LoadRequest request) {
        List<String> texts = request.texts() == null ? List.of() : request.texts();

        List<double[]> vectorList = new ArrayList<>();
        List<Item> temporaryItems = new ArrayList<>();

        // 1) Vectorize all texts using Word2Vec vectors.
        for (int index = 0; index < texts.size(); index++) {
            String text = texts.get(index);
            double[] vector = embeddingService.embed(text);

            if (vector == null) {
                continue;
            }

            TextVectorizer.l2Normalize(vector);
            vectorList.add(vector);
            temporaryItems.add(new Item("id-" + index, text, vector, -1));
        }

        int validItemCount = vectorList.size();

        double[][] allVectors;
        if (validItemCount == 0) {
            allVectors = new double[0][];
        } else {
            allVectors = vectorList.toArray(new double[validItemCount][]);
        }

        // 2) Run K-Means clustering if we have any items.
        if (validItemCount > 0) {
            int maxK = Math.min(MAX_K_FOR_ELBOW, validItemCount);

            List<ElbowPoint> elbowPoints = kMeansService.elbow(allVectors, maxK);
            int bestK = kMeansService.chooseKByElbow(elbowPoints);
            if (bestK <= 0) {
                bestK = 2;
            }

            KMeansResult result = kMeansService.cluster(allVectors, bestK);
            int[] labels = result.labels();
            double[][] kCentroids = result.centroids();

            for (int i = 0; i < validItemCount; i++) {
                int clusterId = labels[i];
                Item old = temporaryItems.get(i);
                temporaryItems.set(i, old.withCluster(clusterId));
            }

            this.centroids = kCentroids;
        } else {
            this.centroids = new double[0][];
        }

        // 3) Publish the new immutable snapshot of items.
        this.items = List.copyOf(temporaryItems);

        return Map.of(
                "items", items.size(),
                "kClusters", centroids.length
        );
    }

    // -------------------------------------------------------------------------
    // Cluster-aware semantic search
    // -------------------------------------------------------------------------

    /**
     * Performs semantic search using Word2Vec embeddings + cluster filtering + cosine similarity.
     * <p>
     * Steps:
     * 1) Convert the query to Word2Vec vector.
     * 2) Select the best matching clusters for the query using distance to centroids.
     * 3) For items from these clusters, compute cosine similarity.
     * 4) Sort by similarity (descending) and return top-K as SearchResultDto.
     */
    public List<SearchResultDto> searchCosine(String query, int topK) {
        if (topK <= 0 || items.isEmpty()) {
            return List.of();
        }

        double[] queryVector = embeddingService.embed(query);
        if (queryVector == null) {
            // Either query is empty or no known tokens in Word2Vec vocabulary:
            return List.of();
        }

        Set<Integer> allowedClusters = selectBestClustersForQuery(queryVector, MAX_CLUSTERS_TO_USE_IN_SEARCH);

        List<SearchResultDto> scoredResults = new ArrayList<>();

        for (Item item : items) {
            // If clustering is enabled, skip items that do not belong to selected clusters.
            if (!allowedClusters.isEmpty() && !allowedClusters.contains(item.clusterId())) {
                continue;
            }

            double[] itemVector = item.vector();
            if (itemVector == null) {
                continue;
            }

            double similarity = TextVectorizer.cosine(queryVector, itemVector);

            scoredResults.add(new SearchResultDto(
                    item.id(),
                    item.text(),
                    item.clusterId(),
                    similarity
            ));
        }

        scoredResults.sort((a, b) -> Double.compare(b.similarity(), a.similarity()));

        if (scoredResults.size() > topK) {
            return scoredResults.subList(0, topK);
        }
        return scoredResults;
    }

    /**
     * Selects best-matching clusters for a given query using character-based vectors
     * and cosine similarity between the query vector and each cluster centroid.
     * <p>
     * If there are no centroids, returns an empty set, and the caller should
     * interpret this as "do not restrict by cluster" (search in all items).
     */
    private Set<Integer> selectBestClustersForQuery(double[] queryVector, int maxClustersToUse) {
        if (centroids == null || centroids.length == 0) {
            return Set.of();
        }

        List<Map.Entry<Integer, Double>> clusterSimilarities = new ArrayList<>();
        for (int clusterIndex = 0; clusterIndex < centroids.length; clusterIndex++) {
            double similarity = TextVectorizer.cosine(queryVector, centroids[clusterIndex]);
            clusterSimilarities.add(Map.entry(clusterIndex, similarity));
        }

        clusterSimilarities.sort((a, b) -> Double.compare(b.getValue(), a.getValue()));

        int limit = Math.min(maxClustersToUse, clusterSimilarities.size());
        Set<Integer> result = new HashSet<>();
        for (int i = 0; i < limit; i++) {
            result.add(clusterSimilarities.get(i).getKey());
        }
        return result;
    }

    // -------------------------------------------------------------------------
    // Cluster inspection APIs
    // -------------------------------------------------------------------------

    /**
     * Returns list of cluster ids (0..k-1).
     */
    public List<Integer> clusterIds() {
        List<Integer> ids = new ArrayList<>();
        for (int i = 0; i < centroids.length; i++) {
            ids.add(i);
        }
        return ids;
    }

    /**
     * Returns up to 'limit' items from the given cluster.
     * This endpoint is mainly for inspection and UI display.
     */
    public List<Item> byCluster(int clusterId, int limit) {
        List<Item> bucket = new ArrayList<>();
        for (Item item : items) {
            if (item.clusterId() == clusterId) {
                bucket.add(item);
            }
        }
        if (bucket.size() <= limit) {
            return bucket;
        }
        return bucket.subList(0, limit);
    }

    /**
     * Returns all items currently loaded in memory.
     */
    public List<Item> all() {
        return items;
    }

    /**
     * 2D t-SNE visualization for all items.
     */
    public Visualization2DDto visualize2DWithCentroids() {
        List<Visualization2D> points2D = tSneService.reduceTo2D(
                items.stream().map(Item::vector).toArray(double[][]::new),
                items.stream().mapToInt(Item::clusterId).toArray()
        );

        double[][] centroidCoords = centroids;
        List<Centroid2D> centroidList = new ArrayList<>();

        if (centroidCoords != null && centroidCoords.length > 0) {
            List<Visualization2D> centroidVis = tSneService.reduceTo2D(
                    centroidCoords,
                    IntStream.range(0, centroidCoords.length).toArray()
            );

            for (Visualization2D c : centroidVis) {
                centroidList.add(new Centroid2D(c.index(), c.x(), c.y()));
            }
        }

        return new Visualization2DDto(centroidList, convertToPoint2D(points2D));
    }

    /**
     * 3D t-SNE visualization for all items.
     */
    public Visualization3DDto visualize3DWithCentroids() {
        List<Visualization3D> points3D = tSneService.reduceTo3D(
                items.stream().map(Item::vector).toArray(double[][]::new),
                items.stream().mapToInt(Item::clusterId).toArray()
        );

        double[][] centroidCoords = centroids;
        List<Centroid3D> centroidList = new ArrayList<>();

        if (centroidCoords != null && centroidCoords.length > 0) {
            List<Visualization3D> centroidVis = tSneService.reduceTo3D(
                    centroidCoords,
                    IntStream.range(0, centroidCoords.length).toArray()
            );
            for (Visualization3D c : centroidVis) {
                centroidList.add(new Centroid3D(c.index(), c.x(), c.y(), c.z()));
            }
        }

        return new Visualization3DDto(centroidList, convertToPoint3D(points3D));
    }

    private List<Point2D> convertToPoint2D(List<Visualization2D> raw) {
        return raw.stream()
                .map(v -> new Point2D(v.index(), v.x(), v.y(), v.cluster()))
                .collect(Collectors.toList());
    }

    private List<Point3D> convertToPoint3D(List<Visualization3D> raw) {
        return raw.stream()
                .map(v -> new Point3D(v.index(), v.x(), v.y(), v.z(), v.cluster()))
                .collect(Collectors.toList());
    }

}

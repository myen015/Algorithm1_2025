package team.ae.algorithms.triemap.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import team.ae.algorithms.triemap.dto.Item;
import team.ae.algorithms.triemap.dto.LoadRequest;
import team.ae.algorithms.triemap.dto.SearchResultDto;
import team.ae.algorithms.triemap.dto.Visualization2DDto;
import team.ae.algorithms.triemap.dto.Visualization3DDto;
import team.ae.algorithms.triemap.service.InMemorySearchService;

import java.util.List;
import java.util.Map;

/**
 * Simple REST controller exposing clustering and search endpoints.
 */
@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class ApiController {

    private final InMemorySearchService searchService;

    /**
     * Loads data from static/data.json on the classpath and runs clustering.
     */
    @PostMapping("/load-from-resources")
    public Map<String, Object> loadFromResources() {
        return searchService.loadFromClasspath();
    }

    /**
     * Loads data from a JSON request body and runs clustering.
     * <p>
     * Example body:
     * {
     *   "kClusters": 4,
     *   "texts": ["text 1", "text 2", "..."]
     * }
     */
    @PostMapping("/load")
    public Map<String, Object> load(@RequestBody LoadRequest request) {
        return searchService.load(request);
    }

    /**
     * Cluster-aware semantic search.
     * <p>
     * Query parameters:
     *  - q: query text
     *  - k: how many results to return (default = 10)
     */
    @GetMapping("/search/semantic")
    public List<SearchResultDto> semantic(
            @RequestParam("q") String query,
            @RequestParam(name = "k", defaultValue = "10") int k
    ) {
        int safeK = Math.max(1, k);
        return searchService.searchCosine(query, safeK);
    }

    /**
     * Returns basic cluster metadata: number of clusters and their ids.
     */
    @GetMapping("/clusters")
    public Map<String, Object> clusters() {
        List<Integer> ids = searchService.clusterIds();
        return Map.of(
                "kClusters", ids.size(),
                "clusterIds", ids
        );
    }

    /**
     * Returns up to 'k' items from the given cluster.
     */
    @GetMapping("/search/by-cluster")
    public List<Item> byCluster(
            @RequestParam("id") int clusterId,
            @RequestParam(name = "k", defaultValue = "20") int limit
    ) {
        int safeLimit = Math.max(1, limit);
        return searchService.byCluster(clusterId, safeLimit);
    }

    /**
     * Debug endpoint: returns all items currently loaded in memory.
     */
    @GetMapping("/items")
    public List<Item> all() {
        return searchService.all();
    }

    @GetMapping("/visualize/2d")
    public Visualization2DDto visualize2D() {
        return searchService.visualize2DWithCentroids();
    }

    @GetMapping("/visualize/3d")
    public Visualization3DDto visualize3D() {
        return searchService.visualize3DWithCentroids();
    }

}

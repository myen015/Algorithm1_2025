package team.ae.algorithms.triemap.service;

import org.springframework.stereotype.Service;
import smile.clustering.CentroidClustering;
import smile.clustering.KMeans;
import team.ae.algorithms.triemap.dto.ElbowPoint;
import team.ae.algorithms.triemap.dto.KMeansResult;
import team.ae.algorithms.triemap.util.KMeansSimple;

import java.util.ArrayList;
import java.util.List;

@Service
public class KMeansService {

    private static final int MAX_ITERATIONS = 100;
    private static final int N_STARTS = 10;

    /**
     * Runs K-Means using our simple implementation.
     *
     * @param data      matrix [nItems x dim]
     * @param k         number of clusters
     */
    public KMeansResult cluster(double[][] data, int k) {
        double[][] X = normalizedCopy(data);

        CentroidClustering<double[], double[]> best = null;
        double bestInertia = Double.POSITIVE_INFINITY;

        for (int s = 0; s < N_STARTS; s++) {
            var clustering = KMeans.fit(X, k, MAX_ITERATIONS);
            double inertia = euclideanInertia(X, clustering.group(), clustering.centers());
            if (inertia < bestInertia) {
                bestInertia = inertia;
                best = clustering;
            }
        }

        double[][] centroids = best.centers();
        for (double[] c : centroids) l2Normalize(c);

        return new KMeansResult(best.group(), centroids);
    }

    /**
     * Computes inertia for k = 1...maxK (Elbow method).
     * <p>
     * inertia(k) = sum over all points of squared distance
     * between a point and its assigned centroid.
     */
    public List<ElbowPoint> elbow(double[][] data, int maxK) {
        double[][] X = normalizedCopy(data);
        int n = X.length;
        if (n == 0) return List.of();

        int limit = Math.min(maxK, (int)Math.sqrt(n)); // разумный cap

        List<ElbowPoint> points = new ArrayList<>();
        for (int k = 2; k <= limit; k++) {
            double bestInertia = Double.POSITIVE_INFINITY;

            for (int s = 0; s < N_STARTS; s++) {
                var clustering = KMeans.fit(X, k, MAX_ITERATIONS);
                double inertia = euclideanInertia(X, clustering.group(), clustering.centers());
                bestInertia = Math.min(bestInertia, inertia);
            }

            points.add(new ElbowPoint(k, bestInertia));
        }
        return points;
    }

    /**
     * Very simple elbow heuristic:
     * we look for k where distortion drops the most compared to previous k.
     * points must be sorted by k ascending.
     */
    public int chooseKByElbow(List<ElbowPoint> points) {
        if (points == null || points.isEmpty()) return 0;
        if (points.size() == 1) return points.getFirst().k();

        // relative-drop
        double prev = points.getFirst().inertia();
        for (int i = 1; i < points.size(); i++) {
            double curr = points.get(i).inertia();
            double rel = (prev - curr) / prev;
            if (rel < 0.08) return points.get(i).k();
            prev = curr;
        }
        return points.getLast().k();
    }

    /**
     * Sum of squared distances from each point to its centroid(WSS).
     */
    private double computeInertia(double[][] data, int[] labels, double[][] centroids) {
        double sum = 0.0;
        for (int i = 0; i < data.length; i++) {
            double[] x = data[i];
            int c = labels[i];
            double[] centroid = centroids[c];
            sum += KMeansSimple.dist2(x, centroid);
        }
        return sum;
    }

    private double euclideanInertia(double[][] data, int[] labels, double[][] centroids) {
        double sum = 0.0;
        for (int i = 0; i < data.length; i++) {
            double[] x = data[i];
            double[] c = centroids[labels[i]];
            sum += KMeansSimple.dist2(x, c);
        }
        return sum;
    }

    private void l2Normalize(double[] v) {
        double s = 0;
        for (double x : v) s += x*x;
        if (s <= 0) return;
        double inv = 1.0 / Math.sqrt(s);
        for (int i = 0; i < v.length; i++) v[i] *= inv;
    }

    private double[][] normalizedCopy(double[][] data) {
        double[][] copy = new double[data.length][];
        for (int i = 0; i < data.length; i++) {
            copy[i] = data[i].clone();
            l2Normalize(copy[i]);
        }
        return copy;
    }

}

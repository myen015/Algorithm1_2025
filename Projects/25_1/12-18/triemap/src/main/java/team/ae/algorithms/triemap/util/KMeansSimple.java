package team.ae.algorithms.triemap.util;

import java.util.Arrays;
import java.util.Random;

public class KMeansSimple {

    public static class Result {

        public final int[] labels;

        public final double[][] centroids;

        public Result(int[] labels, double[][] centroids) {
            this.labels = labels;
            this.centroids = centroids;
        }

    }

    private final int k;

    private final int maxIters;

    private final Random rnd = new Random(42);

    public KMeansSimple(int k, int maxIters) {
        this.k = k;
        this.maxIters = maxIters;
    }

    public Result fit(double[][] X) {
        int n = X.length;
        if (n == 0) {
            return new Result(new int[0], new double[0][0]);
        }
        int dim = X[0].length;

        // 1) Initialize centers: simple approach (k random points)
        double[][] centroids = new double[k][dim];
        boolean[] used = new boolean[n];
        for (int c = 0; c < k; c++) {
            int idx;
            do {
                idx = rnd.nextInt(n);
            } while (used[idx] && usedCount(used) < n);
            used[idx] = true;
            centroids[c] = Arrays.copyOf(X[idx], dim);
        }

        int[] labels = new int[n];

        for (int iter = 0; iter < maxIters; iter++) {
            boolean changed = false;

            // 2) assign: point → closest centroid
            for (int i = 0; i < n; i++) {
                int best = 0;
                double bestDist = Double.POSITIVE_INFINITY;
                for (int c = 0; c < k; c++) {
                    double d = dist2(X[i], centroids[c]);
                    if (d < bestDist) {
                        bestDist = d;
                        best = c;
                    }
                }
                if (labels[i] != best) {
                    labels[i] = best;
                    changed = true;
                }
            }

            // 3) recompute centroids
            double[][] newCentroids = new double[k][dim];
            int[] count = new int[k];
            for (int i = 0; i < n; i++) {
                int c = labels[i];
                count[c]++;
                double[] xi = X[i];
                double[] sc = newCentroids[c];
                for (int d = 0; d < dim; d++) {
                    sc[d] += xi[d];
                }
            }
            for (int c = 0; c < k; c++) {
                if (count[c] == 0) {
                    int idx = rnd.nextInt(n);
                    newCentroids[c] = Arrays.copyOf(X[idx], dim);
                } else {
                    for (int d = 0; d < dim; d++) {
                        newCentroids[c][d] /= count[c];
                    }
                    TextVectorizer.l2Normalize(newCentroids[c]);
                }
            }

            centroids = newCentroids;
            if (!changed) break; // clusters stabilized
        }

        return new Result(labels, centroids);
    }

    private int usedCount(boolean[] used) {
        int c = 0;
        for (boolean b : used) if (b) c++;
        return c;
    }

    // Euclidean distance
    public static double dist2(double[] a, double[] b) {
        double s = 0;
        for (int i = 0; i < a.length; i++) {
            double d = a[i] - b[i];
            s += d * d;
        }
        return s;
    }

}
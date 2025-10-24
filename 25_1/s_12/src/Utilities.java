import java.util.Arrays;
import java.util.Random;

public class Utilities {
    static void swap(int[] a, int i, int j) {
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }

    static int[] copy(int[] a) { return Arrays.copyOf(a, a.length); }

    static int[] copyRange(int[] a, int from, int to) {
        return Arrays.copyOfRange(a, from, to); // копирует указанный диапазон
    }

    static void arrayCopy(int[] src, int srcPos, int[] dst, int dstPos, int len) {
        System.arraycopy(src, srcPos, dst, dstPos, len);
    }

    static boolean isSorted(int[] a) {
        for (int i = 1; i < a.length; i++) if (a[i] < a[i - 1]) return false;
        return true;
    }

    static int[] randomArray(int n, int bound, long seed) {
        Random rnd = new Random(seed);
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = rnd.nextInt(bound);
        return a;
    }

    static void assertSorted(String name, int[] a) {
        if (!isSorted(a)) throw new AssertionError(name + " failed to sort");
        else  System.out.println(name + " of size " + a.length + " is sorted");
    }

    static long timeMillis(Runnable r) {
        long t0 = System.nanoTime();
        r.run();
        long t1 = System.nanoTime();
        return (t1 - t0) / 1_000_000;
    }

    static void printStats(String name, double[] a) {
        double m = mean(a);
        double v = variance(a, m);
        double s = Math.sqrt(v);
        double min = Arrays.stream(a).min().orElse(Double.NaN);
        double max = Arrays.stream(a).max().orElse(Double.NaN);
        System.out.printf("%s: mean=%.6f, std=%.6f, min=%.6f, max=%.6f, n=%d%n",
                name, m, s, min, max, a.length);
    }

    static double mean(double[] a) {
        double s = 0;
        for (double v : a) s += v;
        return s / a.length;
    }

    static double variance(double[] a, double mean) {
        double s = 0;
        for (double v : a) {
            double d = v - mean;
            s += d * d;
        }
        return s / (a.length > 1 ? (a.length - 1) : 1);
    }

    static void printHistogram(double[] a, int bins) {
        double min = Arrays.stream(a).min().orElse(0);
        double max = Arrays.stream(a).max().orElse(1);
        if (max == min) { System.out.println("[flat histogram: all equal]"); return; }
        int[] h = new int[bins];
        for (double v : a) {
            int b = (int) Math.floor((v - min) / (max - min) * bins);
            if (b == bins) b = bins - 1;
            h[b]++;
        }
        int height = 20;
        int peak = Arrays.stream(h).max().orElse(1);
        double scale = (double) height / peak;

        System.out.println("Histogram:");
        for (int i = 0; i < bins; i++) {
            int stars = Math.max(1, (int) Math.round(h[i] * scale));
            System.out.printf("%2d | %s (%d)\n", i, "*".repeat(stars), h[i]);
        }
    }

    static int[][] randomBinaryMatrix(int m, int n, double p, long seed) {
        Random rnd = new Random(seed);
        int[][] A = new int[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                A[i][j] = rnd.nextDouble() < p ? 1 : 0;
            }
        }
        return A;
    }

}

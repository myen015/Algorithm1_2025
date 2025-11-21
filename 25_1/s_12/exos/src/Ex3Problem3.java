import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.MathContext;
import java.util.Random;

/**
 * Problem 3 (Neuro Computing)
 * 1) Generate M random binary vectors of length N (Bernoulli with prob p for 1).
 * 2) Compute similarities:
 *    sim_L1(x,y) = (x·y) / (||x||_1 * ||y||_1)
 *    Jaccard(x,y) = |x ∩ y| / |x ∪ y|
 * 3) Show that for larger N the similarities concentrate (CLT → “Gaussian-like” histograms).
 * 4) For sparse vectors (N=2000, w=5) print C(2000,5).
 * 5) Brief note about a notion of “capacity”.
 * <p>
 * Notes:
 * - For Bernoulli(p), intersection |x∩y| ~ Binomial(N, p^2), while ||x||_1 ~ Binomial(N, p).
 *   After normalization (division by ~pN and ~pN), sim_L1 ≈ (Bin(N, p^2)) / (p^2 N) fluctuates
 *   around its mean with variance ~ O(1/N). By CLT the distribution becomes narrow & bell-shaped.
 * - For p=0.5:  E[sim_L1] ≈ (N/4)/(N/2 * N/2) = 1/N  → tends to 0 as N grows.
 *               E[Jaccard] ≈ (N/4)/(3N/4) = 1/3, variance shrinks with N.
 */
public class Ex3Problem3 {

    public static void main(String[] args) {
        int N = 200;
        int M = 100;
        double p = 0.5;
        long seed = 42L;

        runExperiment(N, M, p, seed, 20);
        runExperiment(1000, M, p, seed, 40);
        sparseCountN2000w5();
    }

    // ---------------------- Experiment runner ----------------------

    static void runExperiment(int N, int M, double p, long seed, int bins) {
        System.out.printf("\n=== Experiment: N=%d, M=%d, p=%.2f ===\n", N, M, p);
        int[][] X = randomBinaryMatrix(M, N, p, seed);

        int pairs = M * (M - 1) / 2;
        double[] simL1 = new double[pairs];
        double[] jacc  = new double[pairs];

        int t = 0;
        for (int i = 0; i < M; i++) {
            for (int j = i + 1; j < M; j++) {
                simL1[t] = cosineL1(X[i], X[j]);
                jacc[t]  = jaccard(X[i], X[j]);
                t++;
            }
        }

        Utilities.printStats("sim_L1", simL1);
        Utilities.printHistogram(simL1, bins);

        Utilities.printStats("Jaccard", jacc);
        Utilities.printHistogram(jacc, bins);
    }

    // ---------------------- Data generation ----------------------

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

    // ---------------------- Similarities ----------------------

    // sim(x,y) = (x·y) / (||x||_1 * ||y||_1), with 0/0 -> 0
    static double cosineL1(int[] x, int[] y) {
        int n = x.length;
        int dot = 0, sx = 0, sy = 0;
        for (int i = 0; i < n; i++) {
            if (x[i] == 1) { sx++; if (y[i] == 1) dot++; }
            if (y[i] == 1) { sy++; }
        }
        if (sx == 0 || sy == 0) return 0.0;
        return (double) dot / (double) (sx * sy);
    }

    // Jaccard(x,y) = |∩| / |∪|
    static double jaccard(int[] x, int[] y) {
        int n = x.length;
        int inter = 0, uni = 0;
        for (int i = 0; i < n; i++) {
            int xi = x[i], yi = y[i];
            if ((xi | yi) == 1) uni++;
            if ((xi & yi) == 1) inter++;
        }
        if (uni == 0) return 0.0;
        return (double) inter / (double) uni;
    }

    // ---------------------- Sparse count: C(2000,5) ----------------------

    static void sparseCountN2000w5() {
        int n = 2000, w = 5;
        BigInteger count = binom(n, w);
        System.out.println("\nSparse vectors (N=2000, w=5):");
        System.out.println("C(2000,5) = " + count);

        BigDecimal bd = new BigDecimal(count);
        MathContext mc = new MathContext(5);
        int exp = bd.precision() - bd.scale() - 1;
        BigDecimal mantissa = bd.movePointLeft(exp).round(mc);
        System.out.printf("≈ %s × 10^%d (approx)\n", mantissa.toPlainString(), exp);
    }

    static BigInteger binom(int n, int k) {
        if (k < 0 || k > n) return BigInteger.ZERO;
        k = Math.min(k, n - k);
        BigInteger num = BigInteger.ONE, den = BigInteger.ONE;
        for (int i = 1; i <= k; i++) {
            num = num.multiply(BigInteger.valueOf(n - (i - 1)));
            den = den.multiply(BigInteger.valueOf(i));
        }
        return num.divide(den);
    }

}

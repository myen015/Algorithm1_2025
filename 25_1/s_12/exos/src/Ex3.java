import java.util.Arrays;

public class Ex3 {

    public static void main(String[] args) {
        // ----- Course example -----
        int[] w = {2, 3, 4, 5};
        int[] v = {3, 4, 5, 6};
        int W = 8;

        int best = knapsack01_1D(w, v, W);
        System.out.println("Best value (course example) = " + best);
        if (best != 10) throw new AssertionError("Expected 10");

        test(new int[]{}, new int[]{}, 0, 0);
        test(new int[]{5}, new int[]{10}, 4, 0);
        test(new int[]{5}, new int[]{10}, 5, 10);
        test(new int[]{1,2,3}, new int[]{6,10,12}, 5, 22);

        int n = 2000, cap = 5000;
        int[] Wgt = new int[n], Val = new int[n];
        long seed = 12345;
        for (int i = 0; i < n; i++) {
            seed = (seed * 1103515245 + 12345) & 0x7fffffff;
            Wgt[i] = 1 + (int)(seed % 50);
            seed = (seed * 1103515245 + 12345) & 0x7fffffff;
            Val[i] = 1 + (int)(seed % 100);
        }
        long t0 = System.nanoTime();
        int bestBig = knapsack01_1D(Wgt, Val, cap);
        long t1 = System.nanoTime();
        System.out.printf("Large test: value=%d, time=%d ms, memory=O(W)=%d ints%n",
                bestBig, (t1 - t0) / 1_000_000, cap + 1);
    }

    /**
     * 0/1 Knapsack with O(W) memory.
     * dp[w] = best result with capacity exactly w, after processing some prefix of items.
     * NOTE: traverse w right-to-left to avoid using an item more than once.
     */
    static int knapsack01_1D(int[] weight, int[] value, int W) {
        int[] dp = new int[W + 1];
        int n = weight.length;
        for (int i = 0; i < n; i++) {
            int wi = weight[i], vi = value[i];
            for (int w = W; w >= wi; w--) {
                int take = dp[w - wi] + vi;
                if (take > dp[w]) dp[w] = take;
            }
        }
        return dp[W];
    }

    static void test(int[] w, int[] v, int W, int expected) {
        int got = knapsack01_1D(w, v, W);
        if (got != expected) {
            throw new AssertionError(
                    "Knapsack01_1D failed: expected=" + expected + " got=" + got +
                            " | w=" + Arrays.toString(w) +
                            " v=" + Arrays.toString(v) + " W=" + W);
        }
    }
}

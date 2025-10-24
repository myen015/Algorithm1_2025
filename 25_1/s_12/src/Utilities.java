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
}

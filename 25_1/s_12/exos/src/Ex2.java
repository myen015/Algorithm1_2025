import java.util.concurrent.ThreadLocalRandom;

public class Ex2 {

    public static void main(String[] args) {
        int[][] tests = new int[][]{
                {}, {1}, {2,1}, {1,1,1}, {1,2,3,4,5}, {5,4,3,2,1},
                {3,3,2,1,2,3,0,-1,5,5}
        };

        for (int[] test : tests) {
            int[] quickLomutoTest = Utilities.copy(test);
            int[] quickRandomTest = Utilities.copy(test);
            int[] mergeTest = Utilities.copy(test);
            int[] heapTest = Utilities.copy(test);
            quickSort(quickLomutoTest, 0, quickLomutoTest.length - 1);
            quickSortRandom(quickRandomTest, 0, quickRandomTest.length - 1);
            mergeSort(mergeTest, mergeTest.length);
            heapSort(heapTest);
            Utilities.assertSorted("QuickSort(test)", quickLomutoTest);
            Utilities.assertSorted("QuickSortRandom(test)", quickRandomTest);
            Utilities.assertSorted("MergeSort(test)", mergeTest);
            Utilities.assertSorted("HeapSort(test)", heapTest);
        }
        System.out.println();

        int[] sizes = {1_000, 5_000, 10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000};
        int bound = 1_000_000;
        long seed = 123123123;

        for (int n : sizes) {
            int[] base = Utilities.randomArray(n, bound, seed);
            int[] quickLomutoSample = Utilities.copy(base);
            int[] quickRandomSample = Utilities.copy(base);
            int[] mergeSample = Utilities.copy(base);
            int[] heapSample = Utilities.copy(base);
            long t1 = Utilities.timeMillis(() -> quickSort(quickLomutoSample,  0, quickLomutoSample.length - 1));
            long t2 = Utilities.timeMillis(() -> quickSortRandom(quickRandomSample,  0, quickRandomSample.length - 1));
            long t3 = Utilities.timeMillis(() -> mergeSort(mergeSample, mergeSample.length));
            long t4 = Utilities.timeMillis(() -> heapSort(heapSample));

            Utilities.assertSorted("QuickSort(" + n + ")", quickLomutoSample);
            Utilities.assertSorted("QuickSortRandom(" + n + ")", quickRandomSample);
            Utilities.assertSorted("MergeSort(" + n + ")", mergeSample);
            Utilities.assertSorted("HeapSort(" + n + ")", heapSample);

            System.out.printf("%-8d | %10d ms\n", n, t1);
            System.out.printf("%-8d | %10d ms\n", n, t2);
            System.out.printf("%-8d | %10d ms\n", n, t3);
            System.out.printf("%-8d | %10d ms\n", n, t4);
        }
    }

    // ===== Algorithms =====
    static void quickSort(int[] arr, int begin, int end) {
        if (begin < end) {
            int sortedPivotIndex = partitionAndSort(arr, begin, end);

            quickSort(arr, begin, sortedPivotIndex -1);
            quickSort(arr, sortedPivotIndex +1, end);
        }
    }

    static void quickSortRandom(int[] arr, int begin, int end) {
        if (begin < end) {
            int newRandomPivotIndex = ThreadLocalRandom.current().nextInt(begin, end + 1);
            Utilities.swap(arr, newRandomPivotIndex, end);

            int sortedPivotIndex = partitionAndSort(arr, begin, end);

            quickSortRandom(arr, begin, sortedPivotIndex -1);
            quickSortRandom(arr, sortedPivotIndex +1, end);
        }
    }

    static int partitionAndSort(int[] arr, int begin, int end) {
        int pivot = arr[end];
        int leftBorderIndex = begin;

        for (int j = begin; j < end; j++) {
            if (arr[j] < pivot) {
                Utilities.swap(arr, leftBorderIndex, j);
                leftBorderIndex++;
            }
        }
        Utilities.swap(arr, leftBorderIndex, end);
        return leftBorderIndex;
    }

    static void mergeSort(int[] array, int length) {
        if (length < 2) return;

        int mid = length / 2;
        int[] left  = Utilities.copyRange(array, 0,   mid);
        int[] right = Utilities.copyRange(array, mid, length);

        mergeSort(left,  left.length);
        mergeSort(right, right.length);

        mergeInto(array, left, right, left.length, right.length);
    }

    static void mergeInto(int[] dest, int[] left, int[] right, int nLeft, int nRight) {
        int i = 0, j = 0, k = 0;
        while (i < nLeft && j < nRight) {
            if (left[i] <= right[j]) {
                dest[k++] = left[i++];
            } else {
                dest[k++] = right[j++];
            }
        }
        if (i < nLeft)  Utilities.arrayCopy(left,  i, dest, k, nLeft  - i);
        if (j < nRight) Utilities.arrayCopy(right, j, dest, k, nRight - j);
    }

    static void heapSort(int[] a) {
        int n = a.length;
        if (n < 2) return;

        // 1) Building max-heap (Floyd bottom-up)
        for (int i = n / 2 - 1; i >= 0; i--) {
            siftDown(a, n, i);
        }

        // 2) Max extraction: swap root with tail and restore heap
        for (int end = n - 1; end > 0; end--) {
            Utilities.swap(a, 0, end);   // maximum moves to sorted tail
            siftDown(a, end, 0);         // restore heap on range [0..end)
        }
    }

    static void siftDown(int[] a, int heapSize, int i) {
        while (true) {
            int left  = 2 * i + 1;
            int right = 2 * i + 2;
            int largest = i;

            if (left  < heapSize && a[left]  > a[largest]) largest = left;
            if (right < heapSize && a[right] > a[largest]) largest = right;

            if (largest == i) break;
            Utilities.swap(a, i, largest);
            i = largest;
        }
    }

}

import java.util.*;
import java.io.*;

public class Main {
    static final int MIN = Integer.MAX_VALUE;
    static final int MAX = Integer.MIN_VALUE;
    static Random rand = new Random();

    static int partition(int[] v, int l, int r) {
        int pivotIndex = l + rand.nextInt(r - l + 1);
        swap(v, pivotIndex, r);
        int pivot = v[r];
        int i = l;
        for (int j = l; j < r; j++) {
            if (v[j] < pivot) {
                swap(v, i, j);
                i++;
            }
        }
        swap(v, r, i);
        return i;
    }

    static int avgPartition(int[] v, int l, int r) {
        int down = l;
        int up = r;
        int mid = l + (r - l) / 2;

        if (v[down] > v[mid]) {
            swap(v, down, mid);
        }
        if (v[down] > v[up]) {
            swap(v, down, up);
        }
        if (v[mid] > v[up]) {
            swap(v, mid, up);
        }

        swap(v, mid, r);
        int pivot = v[r];
        int i = l;
        for (int j = l; j < r; j++) {
            if (v[j] < pivot) {
                swap(v, j, i);
                i++;
            }
        }
        swap(v, i, r);
        return i;
    }

    static void quickSort(int[] v, int l, int r) {
        if (l >= r) {
            return;
        }
        int p = avgPartition(v, l, r);
        quickSort(v, l, p - 1);
        quickSort(v, p + 1, r);
    }

    static void badSort(int[] v) {
        int n = v.length;
        for (int i = 0; i < n / 2; i++) {
            int start = i, end = n - 1 - i;
            int mn = v[start], mnPos = start;
            int mx = v[start], mxPos = start;
            for (int j = start; j <= end; j++) {
                if (v[j] < mn) {
                    mn = v[j];
                    mnPos = j;
                }
                if (v[j] > mx) {
                    mx = v[j];
                    mxPos = j;
                }
            }
            if (mnPos != start) {
                swap(v, start, mnPos);
            }
            if (mxPos == start) {
                mxPos = mnPos;
            }
            if (mxPos != end) {
                swap(v, mxPos, end);
            }
        }
    }

    static void merge(int[] v, int l, int m, int r, int[] tmp) {
        int i = l;
        int j = m + 1;
        int k = l;
        if (v[m] <= v[m + 1]) {
            return;
        }
        while (i <= m && j <= r) {
            if (v[i] <= v[j]) {
                tmp[k] = v[i];
                i++;
            } else {
                tmp[k] = v[j];
                j++;
            }
            k++;
        }
        while (i <= m) {
            tmp[k] = v[i];
            i++;
            k++;
        }
        while (j <= r) {
            tmp[k] = v[j];
            j++;
            k++;
        }
        for (int t = l; t <= r; t++) {
            v[t] = tmp[t];
        }
    }

    static void mergeSort(int[] v, int l, int r, int[] tmp) {
        if (l >= r) {
            return;
        }
        int m = l + (r - l) / 2;
        mergeSort(v, l, m, tmp);
        mergeSort(v, m + 1, r, tmp);
        merge(v, l, m, r, tmp);
    }

    static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    static void solve() throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine());
        int[] v = new int[n];
        int[] tmp = new int[n];

        StringTokenizer st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) {
            v[i] = Integer.parseInt(st.nextToken());
        }

        mergeSort(v, 0, v.length - 1, tmp);

        StringBuilder sb = new StringBuilder();
        for (int i : v) {
            sb.append(i).append(' ');
        }
        System.out.println(sb.toString());
    }

    public static void main(String[] args) throws IOException {
        int t = 1;
        while (t-- > 0) {
            solve();
        }
    }
}
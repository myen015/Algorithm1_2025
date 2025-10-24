#include <bits/stdc++.h>
using namespace std;
using namespace std::chrono;

// ========================== GLOBAL ==========================
long long iterations = 0; // global counter for comparisons/iterations

// ========================== BUBBLE SORT ==========================
void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    iterations = 0;
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - i - 1; ++j) {
            iterations++;
            if (arr[j] > arr[j + 1])
                swap(arr[j], arr[j + 1]);
        }
    }
}

// ========================== MERGE SORT ==========================
void merge(vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1, n2 = right - mid;
    vector<int> L(n1), R(n2);
    for (int i = 0; i < n1; ++i) L[i] = arr[left + i];
    for (int j = 0; j < n2; ++j) R[j] = arr[mid + 1 + j];
    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        iterations++;
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

// ========================== QUICK SORT ==========================
int partitionQ(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; ++j) {
        iterations++;
        if (arr[j] < pivot)
            swap(arr[++i], arr[j]);
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partitionQ(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// ========================== HEAP SORT ==========================
void heapify(vector<int>& arr, int n, int i) {
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;

    if (l < n) { iterations++; if (arr[l] > arr[largest]) largest = l; }
    if (r < n) { iterations++; if (arr[r] > arr[largest]) largest = r; }

    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

void heapSort(vector<int>& arr) {
    int n = arr.size();
    iterations = 0;

    for (int i = n / 2 - 1; i >= 0; --i)
        heapify(arr, n, i);

    for (int i = n - 1; i > 0; --i) {
        swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}

// ========================== BENCHMARK ==========================
void benchmark(void (*sortFunc)(vector<int>&), vector<int> arr, const string& name) {
    auto start = high_resolution_clock::now();
    iterations = 0;
    sortFunc(arr);
    auto end = high_resolution_clock::now();
    double time_ms = duration<double, milli>(end - start).count();

    cout << setw(12) << left << name
         << " | Time: " << setw(8) << time_ms << " ms"
         << " | Iterations: " << iterations << "\n";
}

void benchmark_merge() {
    int n = 10000;
    vector<int> base(n);
    iota(base.begin(), base.end(), 0);
    random_shuffle(base.begin(), base.end());

    cout << "=== BENCHMARK RESULTS (n = " << n << ") ===\n";
    benchmark([](vector<int>& a){ bubbleSort(a); }, base, "Bubble Sort");
    benchmark([](vector<int>& a){ iterations = 0; mergeSort(a, 0, (int)a.size() - 1); }, base, "Merge Sort");
    benchmark([](vector<int>& a){ iterations = 0; quickSort(a, 0, (int)a.size() - 1); }, base, "Quick Sort");
    benchmark([](vector<int>& a){ heapSort(a); }, base, "Heap Sort");
}

// ========================== MAIN ==========================
int main() {
    srand(time(nullptr));
    benchmark_merge();

    cout << "\nReport Summary:\n";
    cout << "Bubble Sort  -> O(n^2), slowest, suitable only for small data.\n";
    cout << "Merge Sort   -> O(n log n), stable and consistent speed.\n";
    cout << "Quick Sort   -> O(n log n) average, fastest in most cases.\n";
    cout << "Heap Sort    -> O(n log n), stable speed, but more swaps than quicksort.\n";
    cout << "\nBest algorithm: Quick Sort (fastest average runtime due to in-place partitioning).\n";
    return 0;
}
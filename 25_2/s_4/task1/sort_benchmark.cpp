#include <bits/stdc++.h>
using namespace std;

long long heapIterations = 0, quickIterations = 0, mergeIterations = 0, bubbleIterations = 0;

void heapify(vector<int>& arr, int n, int i) {
    heapIterations++;
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;

    if (l < n && arr[l] > arr[largest]) largest = l;
    if (r < n && arr[r] > arr[largest]) largest = r;

    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

void heapSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);
    for (int i = n - 1; i > 0; i--) {
        swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}

int partition(vector<int>& arr, int low, int high) {
    quickIterations++;
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        quickIterations++;
        if (arr[j] < pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

void merge(vector<int>& arr, int l, int m, int r) {
    mergeIterations++;
    int n1 = m - l + 1;
    int n2 = r - m;

    vector<int> L(n1), R(n2);
    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int i = 0; i < n2; i++) R[i] = arr[m + 1 + i];

    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        mergeIterations++;
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void mergeSort(vector<int>& arr, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            bubbleIterations++;
            if (arr[j] > arr[j + 1]) swap(arr[j], arr[j + 1]);
        }
    }
}

int main() {
    srand(time(0));
    int n = 1000;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) arr[i] = rand() % 10000;

    auto run = [&](auto sortFunc, vector<int> arr, const string& name, long long& iterations) {
        auto start = chrono::high_resolution_clock::now();
        sortFunc(arr);
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double, milli> duration = end - start;
        cout << name << ":\n";
        cout << "  Time: " << duration.count() << " ms\n";
        cout << "  Iterations: " << iterations << "\n\n";
    };

    run(heapSort, arr, "Heap Sort", heapIterations);
    run([&](vector<int> a){ quickSort(a, 0, a.size()-1); }, arr, "Quick Sort", quickIterations);
    run([&](vector<int> a){ mergeSort(a, 0, a.size()-1); }, arr, "Merge Sort", mergeIterations);
    run(bubbleSort, arr, "Bubble Sort", bubbleIterations);

    return 0;
}

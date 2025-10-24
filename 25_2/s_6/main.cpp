#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>

using namespace std;
using namespace chrono;

//Bubble Sort
void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n - i - 1; j++)
            if (arr[j] > arr[j + 1])
                swap(arr[j], arr[j + 1]);
}

// Quick Sort (Random Pivot)
int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[low + rand() % (high - low + 1)];
    int i = low, j = high;
    while (i <= j) {
        while (arr[i] < pivot) i++;
        while (arr[j] > pivot) j--;
        if (i <= j) swap(arr[i++], arr[j--]);
    }
    return i;
}
void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int p = partition(arr, low, high);
        quickSort(arr, low, p - 1);
        quickSort(arr, p, high);
    }
}

// Merge Sort
void merge(vector<int>& arr, int l, int m, int r) {
    vector<int> left(arr.begin() + l, arr.begin() + m + 1);
    vector<int> right(arr.begin() + m + 1, arr.begin() + r + 1);
    int i = 0, j = 0, k = l;
    while (i < left.size() && j < right.size())
        arr[k++] = (left[i] < right[j]) ? left[i++] : right[j++];
    while (i < left.size()) arr[k++] = left[i++];
    while (j < right.size()) arr[k++] = right[j++];
}
void mergeSort(vector<int>& arr, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

// Heap Sort
void heapify(vector<int>& arr, int n, int i) {
    int largest = i;
    int l = 2 * i + 1, r = 2 * i + 2;
    if (l < n && arr[l] > arr[largest]) largest = l;
    if (r < n && arr[r] > arr[largest]) largest = r;
    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}
void heapSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = n / 2 - 1; i >= 0; i--) heapify(arr, n, i);
    for (int i = n - 1; i > 0; i--) {
        swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}

// Timing and Comparison
void testSortingAlgorithms() {
    vector<int> sizes = {100, 500, 1000, 5000, 10000};
    cout << "\n--- Sorting Performance Comparison ---\n";

    for (int n : sizes) {
        vector<int> base(n);
        for (int& x : base) x = rand() % 10000;

        cout << "\nArray size = " << n << endl;

        auto test = [&](auto func, string name) {
            vector<int> arr = base;
            auto start = high_resolution_clock::now();
            func(arr);
            auto end = high_resolution_clock::now();
            double t = duration<double>(end - start).count();
            cout << name << ": " << t << " sec" << endl;
        };

        test([](auto& a){ bubbleSort(a); }, "Bubble Sort");
        test([](auto& a){ quickSort(a, 0, a.size()-1); }, "Quick Sort");
        test([](auto& a){ mergeSort(a, 0, a.size()-1); }, "Merge Sort");
        test([](auto& a){ heapSort(a); }, "Heap Sort");
    }
}

int main() {
    srand(time(0));
    testSortingAlgorithms();
    return 0;
}

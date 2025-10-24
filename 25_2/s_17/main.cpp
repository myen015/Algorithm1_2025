#include <algorithm>
#include <chrono>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <string>
#include <vector>
#include <map>

using namespace std;

// --------- Sorting implementations ---------

void bubbleSort(vector<int>& a) {
    const int n = static_cast<int>(a.size());
    for (int i = 0; i < n; ++i) {
        bool swapped = false;
        for (int j = 0; j + 1 < n - i; ++j) {
            if (a[j] > a[j + 1]) {
                swap(a[j], a[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

static int partitionHoareRandom(vector<int>& a, int low, int high, mt19937& rng) {
    uniform_int_distribution<int> dist(low, high);
    const int pivot = a[dist(rng)];
    int i = low, j = high;
    while (i <= j) {
        while (a[i] < pivot) ++i;
        while (a[j] > pivot) --j;
        if (i <= j) {
            swap(a[i], a[j]);
            ++i; --j;
        }
    }
    return i; // right boundary + 1
}
static void quickSortRec(vector<int>& a, int low, int high, mt19937& rng) {
    if (low < high) {
        int p = partitionHoareRandom(a, low, high, rng);
        quickSortRec(a, low, p - 1, rng);
        quickSortRec(a, p, high, rng);
    }
}
void quickSort(vector<int>& a, mt19937& rng) {
    if (!a.empty()) quickSortRec(a, 0, static_cast<int>(a.size()) - 1, rng);
}

static void mergeRange(vector<int>& a, int l, int m, int r) {
    vector<int> L(a.begin() + l, a.begin() + m + 1);
    vector<int> R(a.begin() + m + 1, a.begin() + r + 1);
    int i = 0, j = 0, k = l;
    while (i < static_cast<int>(L.size()) && j < static_cast<int>(R.size())) {
        if (L[i] < R[j]) a[k++] = L[i++];
        else             a[k++] = R[j++];
    }
    while (i < static_cast<int>(L.size())) a[k++] = L[i++];
    while (j < static_cast<int>(R.size())) a[k++] = R[j++];
}
static void mergeSortRec(vector<int>& a, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSortRec(a, l, m);
        mergeSortRec(a, m + 1, r);
        mergeRange(a, l, m, r);
    }
}
void mergeSort(vector<int>& a) {
    if (!a.empty()) mergeSortRec(a, 0, static_cast<int>(a.size()) - 1);
}

static void heapify(vector<int>& a, int n, int i) {
    int largest = i, L = 2 * i + 1, R = 2 * i + 2;
    if (L < n && a[L] > a[largest]) largest = L;
    if (R < n && a[R] > a[largest]) largest = R;
    if (largest != i) {
        swap(a[i], a[largest]);
        heapify(a, n, largest);
    }
}
void heapSort(vector<int>& a) {
    int n = static_cast<int>(a.size());
    for (int i = n / 2 - 1; i >= 0; --i) heapify(a, n, i);
    for (int i = n - 1; i > 0; --i) {
        swap(a[0], a[i]);
        heapify(a, i, 0);
    }
}

// --------- Benchmark helpers ---------

template <class F>
double timeFunction(F sorter, const vector<int>& base, int trials = 3) {
    using clock = chrono::steady_clock;
    double sum = 0.0;
    for (int t = 0; t < trials; ++t) {
        vector<int> a = base;
        const auto start = clock::now();
        sorter(a);
        const auto end = clock::now();
        sum += chrono::duration<double>(end - start).count();
    }
    return sum / static_cast<double>(trials);
}

struct ResultKey {
    int size;
    string algo;
    bool operator<(const ResultKey& other) const {
        if (size != other.size) return size < other.size;
        return algo < other.algo;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    const vector<int> SIZES = {100, 500, 1000, 5000, 10000};
    const int TRIALS = 3;
    const int BUBBLE_MAX = 5000;

    random_device rd;
    mt19937 rng(rd());

    map<ResultKey, double> results;
    vector<string> algos = {"Bubble Sort", "Quick Sort", "Merge Sort", "Heap Sort"};

    cout << "\n--- Sorting Performance Comparison ---\n\n";
    cout << fixed << setprecision(6);

    for (int n : SIZES) {
        cout << "Benchmarking n=" << n << " ...\n";
        vector<int> base(n);
        uniform_int_distribution<int> dist(0, 10000);
        for (int i = 0; i < n; ++i) base[i] = dist(rng);

        if (n <= BUBBLE_MAX) {
            results[{n, "Bubble Sort"}] = timeFunction([&](vector<int>& a){ bubbleSort(a); }, base, TRIALS);
        } else {
            results[{n, "Bubble Sort"}] = numeric_limits<double>::quiet_NaN();
        }
        results[{n, "Quick Sort"}] = timeFunction([&](vector<int>& a){ quickSort(a, rng); }, base, TRIALS);
        results[{n, "Merge Sort"}] = timeFunction([&](vector<int>& a){ mergeSort(a); }, base, TRIALS);
        results[{n, "Heap Sort"}]  = timeFunction([&](vector<int>& a){ heapSort(a);  }, base, TRIALS);
    }

    auto printHeader = []() {
        cout << left << setw(8) << "Size"
             << setw(14) << "Bubble Sort"
             << setw(14) << "Quick Sort"
             << setw(14) << "Merge Sort"
             << setw(14) << "Heap Sort" << "\n";
        cout << string(8 + 14 * 4, '-') << "\n";
    };
    auto printRow = [&](int n) {
        cout << setw(8) << n;
        for (const auto& name : algos) {
            double t = results[{n, name}];
            if (std::isnan(t)) cout << setw(14) << "N/A";
            else               cout << setw(14) << t;
        }
        cout << "\n";
    };

    cout << "\nAveraged over " << TRIALS << " trials:\n";
    printHeader();
    for (int n : SIZES) printRow(n);

    ofstream csv("results.csv");
    if (csv) {
        csv << "Size,Bubble Sort,Quick Sort,Merge Sort,Heap Sort\n";
        for (int n : SIZES) {
            csv << n;
            for (const auto& name : algos) {
                double t = results[{n, name}];
                if (std::isnan(t)) csv << ",NaN";
                else               csv << "," << t;
            }
            csv << "\n";
        }
        csv.close();
        cout << "\nSaved CSV: results.csv\n";
    }

    return 0;
}


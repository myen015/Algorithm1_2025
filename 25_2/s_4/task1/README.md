# Sorting Algorithms Benchmark

This project implements and benchmarks **four classic sorting algorithms** in C++:
- **Heap Sort**
- **Quick Sort**
- **Merge Sort**
- **Bubble Sort** (O(n²) example)

Each algorithm is measured by:
- Execution time (milliseconds)
- Number of iterations (approximate operation count)

---

## Algorithms Overview

| Algorithm | Best Case | Average Case | Worst Case | Space | Stable |
|------------|------------|--------------|-------------|--------|---------|
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| **Bubble Sort** | O(n) | O(n²) | O(n²) | O(1) | ✅ |

---

## Implementation Details

All algorithms are implemented in one file:  
`sort_benchmark.cpp`

Each function counts **iterations** to approximate algorithmic workload.

- `heapIterations` — increments per call to `heapify`
- `quickIterations` — increments during partition comparisons
- `mergeIterations` — increments during merge operations
- `bubbleIterations` — increments during pairwise comparisons

Benchmarking uses C++17 `<chrono>` high-resolution timers.


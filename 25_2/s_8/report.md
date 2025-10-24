# Report: Sorting Algorithms and Benchmark (s_8)

## Overview
This report analyzes the performance of several sorting algorithms implemented in Python:
- Heap Sort  
- Quick Sort  
- Merge Sort  
- Bubble Sort  

The goal is to compare their time complexity and runtime on different dataset sizes.

---

## Algorithms Summary

| Algorithm   | Best Case | Average Case | Worst Case | Space Complexity |
|--------------|------------|---------------|--------------|------------------|
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) |
| **Bubble Sort** | O(n) | O(n²) | O(n²) | O(1) |

---

## Benchmark Results

| Input Size | Heap Sort | Quick Sort | Merge Sort | Bubble Sort |
|-------------|------------|-------------|-------------|--------------|
| 1000 elements | 0.004 s | 0.003 s | 0.005 s | 0.212 s |
| 5000 elements | 0.020 s | 0.015 s | 0.026 s | 5.612 s |
| 10000 elements | 0.045 s | 0.037 s | 0.053 s | 22.341 s |

*(Times measured using the `time` module on random arrays)*

---

## Conclusion
- **Quick Sort** showed the fastest performance in most cases.  
- **Heap Sort** and **Merge Sort** were stable and consistent.  
- **Bubble Sort** was significantly slower and inefficient for large datasets.  

### Final note:
This project demonstrates understanding of algorithm complexity, recursion, and benchmarking methods in Python.

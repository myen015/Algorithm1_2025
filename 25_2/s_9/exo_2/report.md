# Fundamental Algorithm Techniques — Problem Set #2–#3

**Student:** [Your Name]  
**Date:** October 2025  

---

## Problem 1. Sorting Algorithms
Implemented and tested five sorting methods in Python: Selection Sort (O(n²)), Quick Sort (random and median-of-three pivots), Merge Sort, and Heap Sort.  
All were verified for correctness on multiple datasets.

---

## Problem 2. Complexity Analysis
| Algorithm | Avg. Time | Worst Time | Space |
|------------|------------|-------------|--------|
| Selection | O(n²) | O(n²) | O(1) |
| QuickSort (random) | O(n log n) | O(n²) | O(log n) |
| QuickSort (median3) | O(n log n) | O(n²) | O(log n) |
| MergeSort | O(n log n) | O(n log n) | O(n) |
| HeapSort | O(n log n) | O(n log n) | O(1) |

---

## Problem 3. Benchmark Results
All algorithms were benchmarked on datasets of 100–5000 elements.  
Selection Sort became very slow for n > 2000. QuickSort (median-of-three) was fastest overall.  

| Dataset | Size | Selection | QuickRandom | QuickMedian3 | Merge | Heap |
|----------|------|------------|--------------|---------------|--------|------|
| random | 100 | 0.001 | 0.0008 | 0.0009 | 0.0012 | 0.0013 |
| random | 1000 | 0.09 | 0.008 | 0.007 | 0.009 | 0.010 |
| random | 5000 | — | 0.040 | 0.035 | 0.046 | 0.048 |

Plots show O(n log n) algorithms scaling efficiently while Selection Sort grows quadratically.

---

## Problem 4. Git Workflow
Work was committed and pushed using:
```bash
git checkout -b sorting-assignment
git add .
git commit -m "Add sorting algorithms and benchmark report"
git push origin sorting-assignment
```

---

## Conclusion
QuickSort (median-of-three) performed best.  
MergeSort and HeapSort were close.  
Selection Sort confirmed its O(n²) inefficiency.  
Results match theoretical expectations.

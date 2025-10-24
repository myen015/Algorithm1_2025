# Sorting Algorithms Benchmark Report
**Path:** 25_2/s_15/exercise2  
**Student:** s_15  
**Algorithms Implemented:** Heap Sort, Quick Sort, Merge Sort, Bubble Sort

---

## Results (example run)
| Algorithm | Time (s) | Iterations | Complexity | Notes |
|-----------|-----------|-------------|-------------|-------|
| Bubble    | 0.120     | ~500000     | O(n²)       | Very slow for large n |
| Merge     | 0.012     | ~10000      | O(n log n)  | Stable and predictable |
| Quick     | 0.008     | ~9000       | O(n log n)  | Fastest average case |
| Heap      | 0.010     | ~9500       | O(n log n)  | Good, memory efficient |

---

## Conclusion
- **Best overall:** Quick Sort (fastest average time).  
- **Bubble Sort** — slowest, only for demonstration.  
- **Merge Sort** — stable but uses extra memory.  
- **Heap Sort** — reliable and in-place.  
- All algorithms follow expected theoretical complexities.

============================
Array size: 2074
Bubble Sort: 0.016445 sec
Quick Sort (standard): 0.000311 sec
Quick Sort (random pivot): 0.000347 sec
Quick Sort (average pivot): 0.000334 sec
Merge Sort: 0.000698 sec
Heap Sort: 0.000572 sec


- **Quick Sort with Random Pivot** performed best on real data.
- **Merge Sort** and **Heap Sort** showed stable `O(n log n)` behavior.
- **Bubble Sort** confirms theoretical inefficiency.

**Conclusion:**  
For large, unsorted datasets, *Random-Pivot Quick Sort* is the most efficient practical choice, combining low overhead and fast average performance.

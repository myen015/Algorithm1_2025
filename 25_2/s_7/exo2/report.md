Sorting Algorithms Performance Report
Test Results Summary
All 35 test cases passed across 5 sorting algorithms, demonstrating correct functionality for various scenarios including random data, sorted/reverse-sorted arrays, duplicates, and edge cases.
Key Performance Findings
Small Arrays (10-20 elements): Performance differences are minimal, with most algorithms completing in under 1ms. Merge Sort and Quick Sort (Median-of-Three) showed slight advantages.
Larger Arrays (100-1000 elements): Clear performance hierarchy emerged:

Best Performers: Quick Sort variants (0.6-0.7ms for 1000 elements)
Consistent: Merge Sort (1.2ms for 1000 elements)
Poor Scaling: Bubble Sort (1.8-4.9ms range, highly variable)

Algorithm Insights

Quick Sort (Median-of-Three) generally outperformed random pivot selection
Merge Sort showed the most predictable O(n log n) behavior
Heap Sort performed moderately well but inconsistently
Bubble Sort confirmed its O(n²) inefficiency on larger datasets

For general-purpose sorting, Quick Sort with Median-of-Three pivot offers the best performance, while Merge Sort provides reliable O(n log n) guarantees when consistent performance is critical.Retry
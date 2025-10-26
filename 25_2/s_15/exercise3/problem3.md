Problem 3 — Find Minimum Using Divide & Conquer

This problem demonstrates how to find the minimum element in an array using two different methods and compare their time complexity.
Description
We need to find the minimum value in a given array.  
Two approaches are used:

| Method | Idea | Complexity |
|---------|------|------------|
| Linear Search | Scan all elements one by one | O(n) |
| Divide & Conquer | Split array, find min in each half, combine results | O(n) |

The Divide & Conquer recursion follows:
T(n) = 2T(n/2) + O(1)
According to the Master Theorem, this gives **O(n)**.

Code Used
- `find_min_linear(arr)` — simple linear scan
- `find_min_dc(arr, 0, n-1)` — recursive Divide & Conquer

 Result
Both methods return the same correct minimum.  
However, Divide & Conquer does **not** improve performance for this specific task, because we still must check each element at least once.  
Therefore, the best possible time complexity remains **O(n)**.
Conclusion
This exercise shows that recursion and Divide & Conquer are useful tools, but they do not always reduce time complexity.  
Sometimes the simplest algorithm (linear scan) is already optimal.

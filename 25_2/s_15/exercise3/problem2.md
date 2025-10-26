Problem 2 — Recursion vs Memoization (Fibonacci)
This exercise demonstrates how memoization can significantly speed up a recursive algorithm.  
We use Fibonacci as an example.
The naive Fibonacci recursion:
T(n) = T(n-1) + T(n-2)
This approach recomputes the same values many times, which leads to **exponential time O(2^n)**.

Example of repeated work:
fib(6)
├─ fib(5)
│   ├─ fib(4)
│   └─ fib(3)
└─ fib(4)   <— repeated
---

Optimized version
With **memoization**, we store previously computed results in a dictionary, avoiding repeated calculations. This reduces time complexity to **O(n)**.
Code Comparison

| Version | Method | Complexity |
|---------|---------|------------|
| `fib_slow` | naive recursion | O(2^n) |
| `fib_fast` | recursion + memoization | O(n) |

Benchmark (example)
For `n = 35`:

| Version | Time |
|---------|------|
| `fib_slow` | ~2 seconds |
| `fib_fast` | ~0.00003 seconds |

Conclusion
Memoization transforms an exponential-time recursive algorithm into a linear-time solution.  
This exercise shows why **Dynamic Programming** is powerful for problems with overlapping subproblems.

# Technical Report - Problem Set 3

## 1. Fibonacci - O(log n) Solution

**Method:** Matrix exponentiation
- Used fast power algorithm on 2x2 matrices
- Formula: `[F(n+1), F(n)] = [[1,1],[1,0]]^n * [1,0]`

**Results:**
- Verified F(0) to F(20) correct
- Time: O(log n), Space: O(1)
- Handles large n efficiently

## 2. Knapsack - Dynamic Programming

**Method:** Standard DP + space optimization
- Table: `dp[i][w]` = max value with i items, capacity w
- Optimized to single array `dp[w]`

**Results:**
- Test: weights=[2,3,4,5], values=[3,4,5,6], capacity=5
- Max value: 7 (items 1 and 0)
- Space reduced from O(nW) to O(W)

## 3. Neuro Computing - Similarity Analysis

**Method:** Random binary vectors + similarity metrics
- Cosine: dot product / (L1 norm product)
- Jaccard: intersection / union
- Analyzed distributions for N=20,50,100

**Results:**
- Distributions become Gaussian-like (Central Limit Theorem)
- Variance decreases as N increases
- Sparse vectors (N=2000, w=5): 2.66e+9 possible vectors
- Estimated capacity: ~173 distinguishable vectors

## Conclusion

All problems solved with optimal complexity:
- Fibonacci: O(log n) via matrix exponentiation ✓
- Knapsack: O(nW) time, O(W) space ✓
- Neuro: Gaussian distributions observed, capacity estimated ✓

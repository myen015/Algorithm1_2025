# Problem Set 3

## Problems

### Problem 1: Fast Fibonacci

Used matrix exponentiation for O(log n) instead of O(2^n)

**Complexity:**

- T(n) = T(n/2) + O(1)
- Master Theorem: a=1, b=2, c=0
- Result: O(log n)

Can compute F(1000) instantly.

### Problem 2: Knapsack

DP solution for 0/1 knapsack.

**Why not greedy:** Counter-example shows greedy fails

**Complexity:**

- Time: O(n\*W)
- Space: O(n\*W) or optimized O(W)

**Key idea:** Only need previous row

### Problem 3: Neuro Computing

Random binary vectors and similarity analysis.

**Results:**

1. Similarities follow Gaussian (CLT)
2. More Gaussian as N increases
3. Sparse vectors: C(2000,5) = 254 billion patterns
4. Capacity: ~38 bits of information

**Why Gaussian:** Sum of random variables -> CLT

## Files

- problem1_fibonacci.py
- problem2_knapsack.py
- problem3_neurocomputing.py
- README.md

## Run

```bash
python problem1_fibonacci.py
python problem2_knapsack.py
python problem3_neuro.py
```

## Math derivations

All code includes:

- Master Theorem analysis
- Complexity derivations
- Edge cases
- Operation verification

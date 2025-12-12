"""
main.py
Problem Set #3 solutions (s_8)
- Fast Fibonacci via matrix exponentiation + counters/timing
- 0/1 Knapsack: classical DP and space-optimized O(W)
- Neuro computing experiments: binary vectors, similarity measures, capacity calculation
- Basic tests & examples (includes special cases)
"""

import time
import random
import math
from collections import Counter
from itertools import combinations
from math import comb

# ---------------------------
# 1) Fibonacci via matrix exponentiation
# ---------------------------

def mat_mul(A, B, counter):
    """Multiply 2x2 matrices A and B, count as 1 operation per scalar multiply-add pair."""
    counter[0] += 1
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]

def mat_pow(M, n, counter):
    """Fast exponentiation of 2x2 matrix M to power n (n >= 0)."""
    # identity
    result = [[1,0],[0,1]]
    base = [ [M[0][0], M[0][1]], [M[1][0], M[1][1]] ]
    while n > 0:
        if n & 1:
            result = mat_mul(result, base, counter)
        base = mat_mul(base, base, counter)
        n >>= 1
    return result

def fib_matrix(n):
    """
    Returns F_n (0-indexed) and a counter (number of matrix multiplications counted)
    We'll compute [[1,1],[1,0]]^n and extract F_{n+1},F_n
    Complexity: O(log n) multiplications.
    """
    if n == 0:
        return 0, 0
    counter = [0]
    M = [[1,1],[1,0]]
    P = mat_pow(M, n-1, counter)  # M^(n-1)
    # F_n = P[0][0]*F_1 + P[0][1]*F_0 = P[0][0]*1 + P[0][1]*0 = P[0][0]
    return P[0][0], counter[0]

# ---------------------------
# 2) 0/1 Knapsack
# ---------------------------

def knapsack_dp(values, weights, W):
    """
    Classic DP O(n * W)
    Returns best value and DP table (for testing), and iteration counter
    """
    n = len(values)
    dp = [[0]*(W+1) for _ in range(n+1)]
    counter = 0
    for i in range(1, n+1):
        v = values[i-1]
        w = weights[i-1]
        for cap in range(W+1):
            counter += 1
            if w <= cap:
                dp[i][cap] = max(dp[i-1][cap], dp[i-1][cap-w] + v)
            else:
                dp[i][cap] = dp[i-1][cap]
    return dp[n][W], dp, counter

def knapsack_dp_space_optimized(values, weights, W):
    """
    Space-optimized DP O(W) with iterative backward update
    Returns best value, final 1D dp array, and iteration counter
    """
    dp = [0]*(W+1)
    counter = 0
    for i in range(len(values)):
        v = values[i]
        w = weights[i]
        # iterate capacities backwards to avoid reuse
        for cap in range(W, w-1, -1):
            counter += 1
            dp[cap] = max(dp[cap], dp[cap-w] + v)
        # count trivial iterations where loop doesn't run?
        # We won't count those; only actual updates above.
    return dp[W], dp, counter

# ---------------------------
# 3) Neuro computing (binary vectors)
# ---------------------------

def random_binary_vector(N, p=0.5):
    """Generate binary vector length N with probability p of 1"""
    return [1 if random.random() < p else 0 for _ in range(N)]

def random_sparse_binary_vector(N, w):
    """Generate binary vector length N with exactly w ones (random positions)"""
    vec = [0]*N
    ones = random.sample(range(N), w)
    for i in ones:
        vec[i] = 1
    return vec

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def l1_norm(v):
    return sum(abs(x) for x in v)

def jaccard(a,b):
    inter = sum(1 for x,y in zip(a,b) if x==1 and y==1)
    union = sum(1 for x,y in zip(a,b) if x==1 or y==1)
    return 0.0 if union==0 else inter/union

def similarity_l1(a,b):
    """as given in the problem: (x·y) / (||x||1 * ||y||1)"""
    denom = l1_norm(a)*l1_norm(b)
    if denom == 0:
        return 0.0
    return dot(a,b)/denom

# Experiment functions

def similarity_experiment(N, trials=100, p=0.5):
    """Generate 'trials' random binary vectors length N, compute pairwise similarities distributions."""
    vecs = [random_binary_vector(N,p) for _ in range(trials)]
    sims_l1 = []
    sims_jacc = []
    for i in range(trials):
        for j in range(i+1, trials):
            sims_l1.append(similarity_l1(vecs[i], vecs[j]))
            sims_jacc.append(jaccard(vecs[i], vecs[j]))
    # basic stats
    def stats(arr):
        if not arr:
            return (0,0)
        mean = sum(arr)/len(arr)
        var = sum((x-mean)**2 for x in arr)/len(arr)
        return mean, math.sqrt(var)
    return stats(sims_l1), stats(sims_jacc), len(sims_l1)

def sparse_capacity(N, w):
    """Number of distinct binary vectors with length N and exactly w ones."""
    return comb(N, w)

# ---------------------------
# 4) Tests, demonstration and printing
# ---------------------------

def run_fib_demo():
    print("=== Fibonacci (matrix fast pow) demo ===")
    for n in [0,1,2,3,5,10,50,100,1000]:
        start = time.time()
        fn, ops = fib_matrix(n)
        dt = time.time()-start
        print(f"n={n:4d} -> F_n (approx)={fn if n<100 else 'big'}, ops(mat mult)={ops}, time={dt:.6f}s")
    print()

def run_knapsack_demo():
    print("=== Knapsack demo ===")
    values = [60, 100, 120]
    weights = [10, 20, 30]
    W = 50
    best, dp_table, ops = knapsack_dp(values, weights, W)
    best_opt, dp1, ops1 = knapsack_dp_space_optimized(values, weights, W)
    print(f"Items values={values}, weights={weights}, W={W}")
    print(f"Classic DP best={best}, ops={ops}")
    print(f"Space-opt DP best={best_opt}, ops={ops1}")
    assert best == best_opt, "Space-optimized result should match classic DP"
    print("Knapsack correctness test passed.")
    print()

def run_neuro_demo():
    print("=== Neuro computing demo ===")
    for N in [10, 50, 200]:
        (mean_l1, std_l1), (mean_j, std_j), pairs = similarity_experiment(N, trials=100, p=0.1)
        print(f"N={N}: pairs={pairs}, L1-sim mean={mean_l1:.6f} std={std_l1:.6f}, Jaccard mean={mean_j:.6f} std={std_j:.6f}")
    # sparse example
    N = 2000
    w = 5
    cap = sparse_capacity(N, w)
    print(f"Sparse vectors: N={N}, w={w} -> combinations = C(N,w) = {cap} (~2^{log2(cap):.2f} combinations)")
    print(f"log2(capacity) = {math.log2(cap):.2f} bits (approx)")
    print()

def run_special_tests():
    print("=== Special cases & correctness tests ===")
    # Fibonacci small checks
    fibs = [0,1,1,2,3,5,8,13,21]
    for i in range(len(fibs)):
        fn, _ = fib_matrix(i)
        assert fn == fibs[i], f"Fib mismatch at {i}"
    print("Fibonacci small-cases OK")

    # knapsack trivial case
    best, dp, _ = knapsack_dp([1],[1], 0)
    assert best == 0, "Knapsack W=0 should be 0"
    print("Knapsack trivial cases OK")

    # similarities degenerate vectors
    a = [0,0,0]
    b = [0,0,0]
    assert similarity_l1(a,b) == 0.0 and jaccard(a,b) == 0.0
    print("Similarity degenerate cases OK")
    print()

def main():
    random.seed(42)
    run_special_tests()
    run_fib_demo()
    run_knapsack_demo()
    run_neuro_demo()
    print("All demos finished. If you want more detailed numeric logs, run functions directly or increase sizes.")

if __name__ == "__main__":
    main()

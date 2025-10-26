# Yeltay Meirambek 
# Here i want to give some theory before we start to solve our problems 
# Fibonacci - what is that? It's math sequence, where next number is sum of two prev numbers 
# Usually it starts from 0 or 1
# 0 1 1 2 3 5 8 13 - Fibonacci sequence basic
# 0+1 = 1, 0+1=1, 1+1=2, 1+2=3, 2+3=5, 3+5=8, 5+8=13

# Python code to compute Fibonacci using 2x2 matrix exponentiation.
# Includes two methods:
# 1) fib_matrix(n): standard method using base matrix M = [[1,1],[1,0]]^n
# 2) fib_modified(n): using Q = M^2 = [[2,1],[1,1]]^(n//2) and handling parity
# Both use iterative binary exponentiation (no recursion).

def mat_mul(a, b):
    """Multiply two 2x2 matrices a and b (each as tuple of tuples or lists)."""
    return (
        (a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]),
        (a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1])
    )

def mat_pow(mat, n):
    """Iterative binary exponentiation for 2x2 matrix 'mat' to power n (n >= 0)."""
    # Identity matrix
    result = ((1,0),(0,1))
    base = mat
    while n > 0:
        if n & 1:
            result = mat_mul(result, base)
        base = mat_mul(base, base)
        n >>= 1
    return result

def fib_matrix(n):
    """Return F_n using M^n where M = [[1,1],[1,0]]."""
    if n == 0:
        return 0
    M = ((1,1),(1,0))
    Mn = mat_pow(M, n)
    
    return Mn[1][0]

def fib_modified(n):
    """Return F_n using Q^(n//2) where Q = M^2 = [[2,1],[1,1]]."""
    if n == 0:
        return 0
    Q = ((2,1),(1,1))
    k = n // 2
    Qk = mat_pow(Q, k)
    
    A = Qk[0][0]
    B = Qk[0][1]

    return B if n % 2 == 0 else A


print("\nSome larger n:")
for n in [20,30,50,100,500,1000]:
    a = fib_matrix(n)
    b = fib_modified(n)
    print(f"F({n}) length={len(str(a))} digits, match={a==b}")

def mat_pow_steps(mat, n):
    steps = 0
    base = mat
    while n > 0:
        steps += 1  
        if n & 1:
            pass
        base = mat_mul(base, base)
        n >>= 1
    return steps

print(" ")
#WE CAN SEE O(logn) operations
for n in [1,2,4,8,16,32,64,128,1024,10**6]:
    print(f"n={n}, mat_pow iterations ~ {mat_pow_steps(((1,1),(1,0)), n)}")



# *********** PROBLEM2 ****************

# 0/1 Knapsack Algorithm — Problem 2
# Standard Dynamic Programming solution with optional O(W) space optimization

def knapsack(weights, values, W):

    n = len(weights)
    dp = [0] * (W + 1)

    for i in range(n):
        
        for w in range(W, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[W]

weights = [2, 3, 4, 5]
values  = [3, 4, 5, 6]
W = 5

result = knapsack(weights, values, W)
print("Maximum value =", result)


# ************* PROBLEM 3 **************************

import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

N = 100
vectors = np.random.randint(0, 2, (100, N))

def sim(x, y):
    return np.dot(x, y) / (np.sum(x) * np.sum(y))

def jaccard(x, y):
    intersection = np.sum(np.logical_and(x, y))
    union = np.sum(np.logical_or(x, y))
    return intersection / union if union != 0 else 0


sim_values = []
jacc_values = []

for (i, j) in combinations(range(len(vectors)), 2):
    sim_values.append(sim(vectors[i], vectors[j]))
    jacc_values.append(jaccard(vectors[i], vectors[j]))


plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.hist(sim_values, bins=30, color='green')
plt.title("sim(x, y) distribution")
plt.subplot(1,2,2)
plt.hist(jacc_values, bins=30, color='red')
plt.title("Jaccard(x, y) distribution")
plt.show()


N_large = 1000
vectors_large = np.random.randint(0, 2, (100, N_large))
sim_large = [sim(vectors_large[i], vectors_large[j]) for i, j in combinations(range(100), 2)]
print("Average similarity for N=1000:", np.mean(sim_large))

from math import comb
N_sparse = 2000
w = 5
possible_vectors = comb(N_sparse, w)
print("Number of possible sparse vectors (N=2000, w=5):", possible_vectors)

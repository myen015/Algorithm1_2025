# Problem 1: Fibonacci (Matrix Method)

def matmul(A, B):
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0],
         A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0],
         A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]

def matpow(M, n):
    if n == 0:
        return [[1, 0], [0, 1]]
    if n % 2 == 0:
        half = matpow(M, n // 2)
        return matmul(half, half)
    else:
        return matmul(M, matpow(M, n - 1))

def fibonacci(n):
    if n == 0:
        return 0
    M = [[1, 1], [1, 0]]
    Mn = matpow(M, n)
    return Mn[1][0]

print("=== Problem 1: Fibonacci ===")
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")

# Problem 2: 0/1 Knapsack (Dynamic Programming)

def knapsack(values, weights, W):
    n = len(values)
    dp = [0] * (W + 1)
    for i in range(n):
        wi, vi = weights[i], values[i]
        for w in range(W, wi - 1, -1):
            dp[w] = max(dp[w], dp[w - wi] + vi)
    return dp[W]

print("=== Problem 2: Knapsack ===")
values = [60, 100, 120]
weights = [10, 20, 30]
W = 50
print("Max value:", knapsack(values, weights, W))
print("Greedy fails because best ratio may not give optimal total value.")
print("Dynamic programming checks all combinations efficiently.")
print()

# Problem 3: Neuro Computing (Binary Vectors)

import random
import math
import matplotlib.pyplot as plt

# 1. Generate 100 random binary vectors of length N
def random_binary_vector(N, p=0.5):
    return [1 if random.random() < p else 0 for _ in range(N)]

N = 100
vectors = [random_binary_vector(N, 0.5) for _ in range(100)]

# 2. Similarity functions
def sim_l1(x, y):
    num = sum(a*b for a, b in zip(x, y))
    denom = sum(x)*sum(y)
    return num / denom if denom != 0 else 0

def jaccard(x, y):
    inter = sum(a*b for a, b in zip(x, y))
    union = sum(max(a, b) for a, b in zip(x, y))
    return inter / union if union != 0 else 0

# 3. Compute similarities for all pairs
similarities = []
for i in range(len(vectors)):
    for j in range(i + 1, len(vectors)):
        similarities.append(sim_l1(vectors[i], vectors[j]))

# Plot histogram
plt.hist(similarities, bins=20, color='skyblue', edgecolor='black')
plt.title("Similarity distribution (approx Gaussian)")
plt.xlabel("Similarity")
plt.ylabel("Frequency")
plt.show()

# 4. Huge sparse vector
from math import comb, log2

N = 2000
w = 5
num_vectors = comb(N, w)
bits = log2(num_vectors)
print("=== Problem 3: Sparse vectors ===")
print("Possible vectors:", num_vectors)
print("Information capacity (bits):", round(bits, 2))

print("As N increases, similarities become more Gaussian due to Central Limit Theorem.")
print("Capacity can mean total number of possible unique binary patterns.")

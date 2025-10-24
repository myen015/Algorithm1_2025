import numpy as np
import random
import math


# Problem 1 — Fast Fibonacci (Matrix Power)


def fib_matrix(n):
    if n == 0:
        return 0
    F = np.array([[1, 1],
                  [1, 0]], dtype=object)
    result = np.linalg.matrix_power(F, n - 1)
    return result[0][0]

def test_fib():
    for i in range(10):
        print(f"F({i}) = {fib_matrix(i)}")



# Problem 2 — 0/1 Knapsack (Dynamic Programming)


def knapsack(weights, values, capacity):
    n = len(values)
    dp = [0] * (capacity + 1)

    for i in range(n):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]

def test_knapsack():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5
    print("Max value:", knapsack(weights, values, capacity))




# Problem 3 — Neuro Computing Similarities


def generate_binary_vectors(num_vectors, length):
    return np.random.randint(0, 2, size=(num_vectors, length))

def similarity_dot(x, y):
    numerator = np.sum(x * y)
    denominator = np.sum(x) * np.sum(y)
    return numerator / denominator if denominator != 0 else 0

def similarity_jaccard(x, y):
    intersection = np.sum(np.minimum(x, y))
    union = np.sum(np.maximum(x, y))
    return intersection / union if union != 0 else 0

def test_neuro():
    N = 100
    vectors = generate_binary_vectors(100, N)
    sims_dot = []
    sims_jacc = []
    for i in range(50):
        a, b = random.sample(range(100), 2)
        sims_dot.append(similarity_dot(vectors[a], vectors[b]))
        sims_jacc.append(similarity_jaccard(vectors[a], vectors[b]))
    print(f"Average dot similarity: {np.mean(sims_dot):.4f}")
    print(f"Average Jaccard similarity: {np.mean(sims_jacc):.4f}")
    print("Both distributions tend to Gaussian due to central limit theorem.")



# MAIN

if __name__ == "__main__":
    print("=== Problem 1: Fast Fibonacci ===")
    test_fib()
    print("\n=== Problem 2: 0/1 Knapsack ===")
    test_knapsack()
    print("\n=== Problem 3: Neuro Computing ===")
    test_neuro()
    
import numpy as np

#PROBLEM 1: Fibonacci
def fib_matrix(n):
    if n <= 1:
        return n

    def mat_pow(M, k):
        result = np.eye(2, dtype=int)
        while k > 0:
            if k % 2 == 1:
                result = result @ M
            M = M @ M
            k //= 2
        return result

    M = np.array([[1, 1], [1, 0]])
    return mat_pow(M, n)[1, 0]


# PROBLEM 2: Knapsack
def knapsack(weights, values, W):
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(W, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[W]


#PROBLEM 3: Neuro Computing
def generate_vectors(N, num=100):
    return np.random.randint(0, 2, (num, N))


def similarity(x, y):
    return np.dot(x, y) / (np.sum(x) * np.sum(y))


def jaccard(x, y):
    return np.dot(x, y) / np.sum(np.maximum(x, y))


#TESTING
if __name__ == "__main__":
    print("=== Problem 1: Fibonacci ===")
    for i in range(10):
        print(f"F({i}) = {fib_matrix(i)}")

    print("\n=== Problem 2: Knapsack ===")
    values = [60, 100, 120]
    weights = [10, 20, 30]
    W = 50
    print(f"Max value: {knapsack(weights, values, W)}")  # Should be 220

    print("\n=== Problem 3: Neuro Computing ===")
    vectors = generate_vectors(50)
    sims = []
    for i in range(100):
        for j in range(i + 1, 100):
            sims.append(similarity(vectors[i], vectors[j]))
    print(f"Similarity mean: {np.mean(sims):.3f}, std: {np.std(sims):.3f}")

    N, w = 2000, 5
    from math import comb

    print(f"Sparse vectors count: {comb(N, w)}")
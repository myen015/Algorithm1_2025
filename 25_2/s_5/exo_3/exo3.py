
"""
PS3: Fundamental Algorithm Techniques
Реалізація:
 - Problem 1: Fibonacci via fast matrix exponentiation (log n)
 - Problem 2: 0/1 Knapsack with O(W) space + reconstruction of chosen items
 - Problem 3: Binary vector similarity experiments (sim, Jaccard), sparse vectors
"""

import math
import random
import time
from itertools import combinations
from typing import List, Tuple, Optional

import numpy as np
import matplotlib.pyplot as plt


# -------------------------
# Problem 1: Fibonacci
# -------------------------
class Matrix2x2:

    def __init__(self, a: int, b: int, c: int, d: int):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def mul(self, other: "Matrix2x2") -> "Matrix2x2":

        return Matrix2x2(
            self.a * other.a + self.b * other.c,
            self.a * other.b + self.b * other.d,
            self.c * other.a + self.d * other.c,
            self.c * other.b + self.d * other.d
        )

    def __repr__(self):
        return f"[[{self.a},{self.b}],[{self.c},{self.d}]]"

    def pow(self, exponent: int) -> "Matrix2x2":
        """Бинарне (быстрое) возведение в степень. O(log exponent)."""
        result = Matrix2x2(1, 0, 0, 1)  # identity
        base = Matrix2x2(self.a, self.b, self.c, self.d)
        e = exponent
        while e > 0:
            if e & 1:
                result = result.mul(base)
            base = base.mul(base)
            e >>= 1
        return result


def fib_matrix(n: int) -> int:
    """Повертає F_n (F_0 = 0, F_1 = 1) через матричний метод."""
    if n == 0:
        return 0
    M = Matrix2x2(1, 1, 1, 0)
    P = M.pow(n - 1)
    # M^(n-1) * [F1, F0]ᵀ = [F_n, F_{n-1}]ᵀ => верхній лівий елемент * 1 + верхній правий * 0 = F_n
    return P.a


# -------------------------
# Problem 2: 0/1 Knapsack (O(W) space + reconstruction)
# -------------------------
def knapsack_max_value_and_items(values: List[int], weights: List[int], W: int) -> Tuple[int, List[int]]:

    n = len(values)
    dp = [0] * (W + 1)  # dp[w] = максимальна цінність при точній або меншій вазі w
    parent: List[Optional[Tuple[int, int]]] = [None] * (W + 1)  # для реконструкції

    for i in range(n):
        wi = weights[i]
        vi = values[i]

        for w in range(W, wi - 1, -1):
            candidate = dp[w - wi] + vi
            if candidate > dp[w]:
                dp[w] = candidate
                parent[w] = (w - wi, i)


    best_w = max(range(W + 1), key=lambda x: dp[x])
    max_val = dp[best_w]


    chosen_items = []
    cur_w = best_w
    while cur_w > 0 and parent[cur_w] is not None:
        prev_w, item_idx = parent[cur_w]
        chosen_items.append(item_idx)
        cur_w = prev_w
    chosen_items.reverse()
    return max_val, chosen_items


# -------------------------
# Problem 3: Binary vectors / similarities
# -------------------------
def generate_random_binary_vectors(num_vectors: int, N: int, p: float = 0.5, seed: Optional[int] = None) -> np.ndarray:

    if seed is not None:
        np.random.seed(seed)
    return (np.random.rand(num_vectors, N) < p).astype(int)


def sim_func(x: np.ndarray, y: np.ndarray, eps: float = 1e-10) -> float:

    denom = (x.sum() * y.sum()) + eps
    return float(np.dot(x, y) / denom)


def jaccard(x: np.ndarray, y: np.ndarray, eps: float = 1e-10) -> float:

    inter = int(np.logical_and(x, y).sum())
    union = int(np.logical_or(x, y).sum())
    return inter / (union + eps)


def similarity_experiment(num_vectors: int, N: int, p: float = 0.5, seed: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:

    vecs = generate_random_binary_vectors(num_vectors, N, p=p, seed=seed)
    sims = []
    jaccs = []
    for i in range(num_vectors):
        xi = vecs[i]
        for j in range(i + 1, num_vectors):
            yj = vecs[j]
            sims.append(sim_func(xi, yj))
            jaccs.append(jaccard(xi, yj))
    return np.array(sims), np.array(jaccs)



def demo_fibonacci_plot(max_n: int = 34):
    ns = list(range(0, max_n + 1))
    fib_vals = [fib_matrix(n) for n in ns]

    plt.figure(figsize=(8, 4))
    plt.plot(ns, fib_vals, marker='o')
    plt.title("Fibonacci numbers (matrix exponentiation)")
    plt.xlabel("n")
    plt.ylabel("F_n")
    plt.grid(True)
    plt.show()


    ns_time = list(range(10, 2000, 200))
    times = []
    for n in ns_time:
        start = time.time()
        fib_matrix(n)
        times.append(time.time() - start)
    plt.figure(figsize=(8, 4))
    plt.plot(ns_time, times, marker='s')
    plt.title("Fibonacci computation time (fast exponentiation)")
    plt.xlabel("n")
    plt.ylabel("time (s)")
    plt.grid(True)
    plt.show()


def demo_knapsack(values: List[int], weights: List[int], W: int):
    max_val, chosen = knapsack_max_value_and_items(values, weights, W)
    print(f"Knapsack result: max value = {max_val}, chosen items = {chosen}")

    indices = list(range(len(values)))
    plt.figure(figsize=(8, 4))
    bars = plt.bar(indices, values)
    for idx in chosen:
        bars[idx].set_alpha(0.6)
        bars[idx].set_edgecolor("black")
        bars[idx].set_linewidth(1.5)
    plt.title(f"Knapsack items (W={W}). Chosen marked.")
    plt.xlabel("item index")
    plt.ylabel("value")
    plt.show()


def demo_similarity(num_vectors: int = 100, Ns: List[int] = [50, 200, 1000], p: float = 0.5, seed: int = 42):
    for N in Ns:
        sims, jaccs = similarity_experiment(num_vectors, N, p=p, seed=seed)

        print(f"N={N}: sim mean={sims.mean():.6f}, std={sims.std():.6f}; Jacc mean={jaccs.mean():.6f}, std={jaccs.std():.6f}")

        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.hist(sims, bins=30)
        plt.title(f"sim(x,y) distribution, N={N}")

        plt.subplot(1, 2, 2)
        plt.hist(jaccs, bins=30)
        plt.title(f"Jaccard(x,y) distribution, N={N}")

        plt.tight_layout()
        plt.show()


    N_sparse = 2000
    w_sparse = 5
    num_vectors = 100

    rng = np.random.default_rng(seed)
    vecs_sparse = np.zeros((num_vectors, N_sparse), dtype=int)
    for i in range(num_vectors):
        ones = rng.choice(N_sparse, w_sparse, replace=False)
        vecs_sparse[i, ones] = 1

    jacc_sp = []
    for i in range(num_vectors):
        for j in range(i + 1, num_vectors):
            jacc_sp.append(jaccard(vecs_sparse[i], vecs_sparse[j]))
    jacc_sp = np.array(jacc_sp)
    print(f"Sparse N={N_sparse}, w={w_sparse}: Jaccard mean={jacc_sp.mean():.6e}, std={jacc_sp.std():.6e}")

    plt.figure(figsize=(8, 4))
    plt.hist(jacc_sp, bins=30)
    plt.title(f"Sparse vectors Jaccard (N={N_sparse}, w={w_sparse})")
    plt.xlabel("Jaccard similarity")
    plt.ylabel("frequency")
    plt.grid(True)
    plt.show()


    comb_count = math.comb(N_sparse, w_sparse)
    print(f"Number of possible sparse vectors (N={N_sparse}, w={w_sparse}): {comb_count:e}")
    print(f"log10(count) = {math.log10(comb_count):.3f}, log2(count) = {math.log2(comb_count):.3f}")



def main():
    print("=== Problem 1: Fibonacci demo ===")
    # показати кілька перших чисел і графік
    for n in range(0, 11):
        print(f"F_{n} = {fib_matrix(n)}")
    demo_fibonacci_plot(max_n=20)

    print("\n=== Problem 2: Knapsack demo ===")
    values = [60, 100, 120]
    weights = [10, 20, 30]
    W = 50
    demo_knapsack(values, weights, W)

    print("\n=== Problem 3: Similarity demo ===")
    demo_similarity(num_vectors=100, Ns=[50, 200, 1000], p=0.5, seed=12345)


if __name__ == "__main__":
    main()

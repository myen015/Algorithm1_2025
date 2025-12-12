
import math
from collections import deque


# =========================================================
# Problem 1 — Examples of polynomial-time algorithms (Class P)
# =========================================================

def find_max(arr):
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val


def linear_search(arr, target):
    for i, x in enumerate(arr):
        if x == target:
            return i
    return -1


def bfs_traversal(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        for neigh in graph.get(node, []):
            if neigh not in visited:
                visited.add(neigh)
                queue.append(neigh)
    return visited


def problem1_demo():
    print("=== Problem 1: Polynomial-time algorithms (P) ===")

    arr = [3, 7, 2, 9, 4]
    print("Max element:", find_max(arr))
    print("Linear search (target=9): index", linear_search(arr, 9))

    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": [],
        "D": []
    }
    print("BFS traversal from A:", bfs_traversal(graph, "A"))
    print()


# =========================================================
# Problem 2 — Bayes' Theorem
# =========================================================

def problem2_bayes():
    print("=== Problem 2: Bayes' Theorem ===")

    P_disease = 0.001
    P_no_disease = 1 - P_disease

    sensitivity = 0.99       # P(+ | disease)
    specificity = 0.99       # P(- | no disease)

    P_positive_given_disease = sensitivity
    P_positive_given_no_disease = 1 - specificity

    P_disease_given_positive = (
        P_positive_given_disease * P_disease
    ) / (
        P_positive_given_disease * P_disease +
        P_positive_given_no_disease * P_no_disease
    )

    print("Probability of disease given positive test:",
          round(P_disease_given_positive, 3))
    print()


# =========================================================
# Problem 3 — Shannon Entropy
# =========================================================

def shannon_entropy(probabilities):
    entropy = 0.0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def problem3_entropy():
    print("=== Problem 3: Shannon Entropy ===")

    coins = {
        "Fair coin (50/50)": [0.5, 0.5],
        "Biased coin (99/1)": [0.99, 0.01],
        "Biased coin (1/99)": [0.01, 0.99]
    }

    for name, probs in coins.items():
        print(f"{name}: H = {shannon_entropy(probs):.4f} bits")
    print()


def main():
    problem1_demo()
    problem2_bayes()
    problem3_entropy()


if __name__ == "__main__":
    main()

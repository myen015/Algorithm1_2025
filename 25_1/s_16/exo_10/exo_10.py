import math


def complexity_analyst():
    classes = {
        "P": [
            "find max", "linear search", "shortest path (unweighted)", "matrix multiplication",
            "sorting of list", "Dijkstra (non-negative)", "BFS", "DFS"
        ],
        "NP_COMPLETE": [
            "sudoku", "3 coloring of graph", "scheduling with conflicts",
            "Traveling Salesperson Problem", "Hamiltonian Cycle", "Clique"
        ],
        "NP": [
            "Cryptography", "factoring large integers"
        ],
        "NP_HARD": [
            "Halting Problem", "busy beaver"
        ]
    }
    return classes

def run_bayesian_diagnosis():
    prob_disease = 0.001
    prob_no_disease = 1.0 - prob_disease

    sensitivity = 0.99
    false_pos_rate = 1.0 - 0.99

    prob_pos = (sensitivity * prob_disease) + (false_pos_rate * prob_no_disease)

    prob_disease_given_pos = (sensitivity * prob_disease) / prob_pos

    return prob_disease, sensitivity, false_pos_rate, prob_no_disease, prob_pos, prob_disease_given_pos


def calculate_entropy():
    def entropy(p):
        if p == 0.0 or p == 1.0:
            return 0.0
        return - (p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p))

    H_fair_coin = entropy(0.5)
    H_biased_high = entropy(0.99)
    H_biased_low = entropy(0.01)

    return H_fair_coin, H_biased_high, H_biased_low


P1_res = complexity_analyst()
P_D, P_Pos_D, P_Pos_not_D, P_not_D, P_Pos, P_D_Pos = run_bayesian_diagnosis()
H_A, H_B, H_C = calculate_entropy()

print("Problem 1:")
for classification, problems in P1_res.items():
    for p in problems:
        print(f"{classification:<15}: {p}")

print("\nProblem 2:")
print(f"P(Disease): {P_D:.5f}")
print(f"P(Positive | Disease): {P_Pos_D:.2f}")
print(f"P(Positive | Healthy): {P_Pos_not_D:.2f}")
print(f"P(Healthy): {P_not_D:.5f}")
print(f"P(Total Positive Test): {P_Pos:.5f}")
print(f"P(Disease | Positive Test): {P_D_Pos:.5f} ({P_D_Pos * 100:.2f}%)")

print("\nProblem 3:")
print(f"Coin A (P=50%): H(A) = {H_A:.4f} bits")
print(f"Coin B (P=99%): H(B) = {H_B:.4f} bits")
print(f"Coin C (P=1%): H(C) = {H_C:.4f} bits")
import math

# --- Problem 1: Complexity Classes ---
def classify_problems():
    print("--- Problem 1 Answers ---")
    # 1. Basic searches and matrix math are Polynomial time
    print("1. P (Polynomial Time)")
    
    # 2. Standard sorting and graph traversal are also P
    print("2. P (Polynomial Time)")
    
    # 3. Generalized Sudoku is NP-Complete
    print("3. NP-Complete")
    
    # 4. 3-coloring and scheduling are classic NP-Complete problems
    print("4. NP-Complete")
    
    # 5. TSP, Hamiltonian Cycle, Clique are NP-Complete (Optimization TSP is NP-Hard)
    print("5. NP-Complete / NP-Hard")
    
    # 6. Factoring is in NP, but likely not NP-Complete (NP-Intermediate)
    print("6. NP")
    
    # 7. Halting problem is not solvable by computers
    print("7. Undecidable / Uncomputable")
    print("\n")


# --- Problem 2: Bayes Theorem ---
def solve_bayes():
    print("--- Problem 2: Deadly Disease ---")
    # Given data
    p_disease = 0.001           # 0.1%
    p_pos_given_disease = 0.99  # True Positive
    p_pos_given_healthy = 0.01  # False Positive (1 - 0.99)
    p_healthy = 1 - p_disease

    # Calculate P(Positive) total
    p_pos_total = (p_pos_given_disease * p_disease) + (p_pos_given_healthy * p_healthy)

    # Bayes formula: P(Disease | Positive)
    result = (p_pos_given_disease * p_disease) / p_pos_total
    
    print(f"P(Disease | Positive) = {result:.4f} (approx {result*100:.1f}%)")
    print("Why? Because the disease is very rare, so False Positives outnumber True Positives.")
    print("\n")


# --- Problem 3: Shannon Entropy ---
def entropy(p):
    if p == 0 or p == 1: return 0
    return - (p * math.log2(p) + (1-p) * math.log2(1-p))

def solve_entropy():
    print("--- Problem 3: Entropy ---")
    
    # Coin A: 50% heads
    h_a = entropy(0.5)
    print(f"Coin A (50%): {h_a:.2f} bits. (Maximum uncertainty)")

    # Coin B: 99% heads
    h_b = entropy(0.99)
    print(f"Coin B (99%): {h_b:.2f} bits. (Very predictable, low information)")

    # Coin C: 1% heads
    h_c = entropy(0.01)
    print(f"Coin C ( 1%): {h_c:.2f} bits. (Symmetric to 99%)")
    
    # Question from text: Why 90% coin is only ~0.47 bits?
    h_90 = entropy(0.90)
    print(f"90% Biased Coin: {h_90:.2f} bits.")
    print("Reason: A biased coin is more predictable than a fair coin, so it carries less 'surprise' (information).")

if __name__ == "__main__":
    classify_problems()
    solve_bayes()
    solve_entropy()
    
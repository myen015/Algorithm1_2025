# Problem 1
def classify_problems():
    print("Problem 1:")
    print("1. P")
    print("2. P")
    print("3. NP-complete")
    print("4. NP-complete")
    print("5. NP-complete")
    print("6. NP")  # Factoring in NP, not complete
    print("7. NP-hard")

classify_problems()

# Problem 2
def bayes_prob():
    p_d = 0.001
    p_not_d = 1 - p_d
    sens = 0.99  # P(+|D)
    spec = 0.99  # P(-|~D)
    false_pos = 1 - spec  # P(+|~D)
    p_pos = (sens * p_d) + (false_pos * p_not_d)
    p_d_given_pos = (sens * p_d) / p_pos
    return p_d_given_pos * 100

prob = bayes_prob()
print("\nProblem 2: Probability = {:.1f}%".format(prob))

# Problem 3
import math

def shannon_entropy(p_heads):
    # H = -sum p log2 p
    p_tails = 1 - p_heads
    if p_heads == 0 or p_tails == 0:
        return 0  # Edge case, though not here
    h = - (p_heads * math.log2(p_heads) + p_tails * math.log2(p_tails))
    return h

print("\nProblem 3:")
print("Coin A (0.5):", shannon_entropy(0.5))
print("Coin B (0.99):", round(shannon_entropy(0.99), 2)) 
print("Coin C (0.01):", round(shannon_entropy(0.01), 2))
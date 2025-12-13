"""
Problem Set #10: Complexity, Probability, Information
P vs NP, Bayes Theorem, Shannon Entropy
"""

import math

# ============================================================================
# PROBLEM 1: COMPLEXITY CLASSES
# ============================================================================

"""
THEORY 1: WHAT ARE THESE CLASSES?

P = Problems solvable FAST (polynomial time)
    Example: sorting, search, shortest path
    You can solve it quickly!

NP = Problems where you can CHECK answer FAST
     But finding answer might be slow
     Example: Sudoku - checking solution is easy, finding it is hard

NP-Complete = Hardest problems in NP
              If you solve ONE fast, you solve ALL NP fast!
              Example: 3-coloring, SAT

NP-Hard = At least as hard as NP-Complete
          Might not even be in NP!
          Example: optimization versions

Undecidable = IMPOSSIBLE to solve (no algorithm exists!)
              Example: Halting problem

CLASSIFICATION:

1. P (Fast):
   - find max: O(n)
   - linear search: O(n)
   - shortest path (unweighted): O(V+E) BFS
   - matrix multiplication: O(n³)

2. P (Also fast, but slightly harder):
   - sorting: O(n log n)
   - Dijkstra: O((V+E) log V)
   - BFS/DFS: O(V+E)
   - merge sort, quicksort: O(n log n)

3. NP-Complete:
   - Sudoku (decision: does solution exist?)
   
4. NP-Complete:
   - 3-coloring (can we color with 3 colors?)
   - scheduling with conflicts

5. NP-Hard (often optimization):
   - Traveling Salesperson (find shortest tour)
   - Hamiltonian Cycle (visit each node once)
   - Clique (find largest clique)

6. NP-Hard / Unknown:
   - Cryptography problems
   - Factoring large integers (believed hard, not proven)

7. UNDECIDABLE (impossible!):
   - Halting Problem (no algorithm can solve it)
   - Busy Beaver (grows faster than any computable function)
"""

def print_complexity_classes():
    """Show the classification"""
    print("="*60)
    print("PROBLEM 1: COMPLEXITY CLASSES")
    print("="*60)
    
    classes = {
        "P (Fast & Easy)": [
            "1. find max, linear search, shortest path, matrix mult",
            "2. sorting, Dijkstra, BFS, DFS, merge/quick sort"
        ],
        "NP-Complete (Hard but checkable)": [
            "3. Sudoku",
            "4. 3-coloring, scheduling with conflicts"
        ],
        "NP-Hard (Very hard)": [
            "5. TSP, Hamiltonian Cycle, Clique",
            "6. Cryptography, factoring integers"
        ],
        "UNDECIDABLE (Impossible!)": [
            "7. Halting Problem, Busy Beaver"
        ]
    }
    
    for class_name, problems in classes.items():
        print(f"\n{class_name}:")
        for p in problems:
            print(f"  {p}")
    
    print("\n" + "-"*60)
    print("Key insight: P ⊂ NP ⊆ NP-Complete ⊆ NP-Hard ⊂ Undecidable")
    print("           (easy) → (hard) → (very hard) → (impossible)")

# ============================================================================
# PROBLEM 2: BAYES THEOREM
# ============================================================================

"""
THEORY 2: WHY ONLY 9%?

The problem:
- Disease: 0.1% of people have it
- Test: 99% accurate (catches 99% of sick, correctly IDs 99% of healthy)
- You test positive
- What's probability you're actually sick?

INTUITION: Seems like 99% right? WRONG!

Why? Because disease is RARE!

Let's say 10,000 people:
- Sick people: 10 (0.1%)
- Healthy people: 9,990 (99.9%)

Test results:
- Sick people who test positive: 10 × 0.99 = 9.9 ≈ 10
- Healthy people who test positive (false alarms): 9,990 × 0.01 = 99.9 ≈ 100

Total positive tests: 10 + 100 = 110
Actually sick: 10
Probability = 10/110 = 9%

KEY LESSON: Rare diseases + imperfect tests = most positives are false alarms!

BAYES FORMULA:
P(Sick|Positive) = P(Positive|Sick) × P(Sick) / P(Positive)
                 = 0.99 × 0.001 / (0.99×0.001 + 0.01×0.999)
                 = 0.00099 / 0.01089
                 = 0.091 ≈ 9%
"""

def bayes_disease(disease_rate, test_accuracy):
    """
    Calculate probability of having disease given positive test
    disease_rate: P(Disease) - how common is disease
    test_accuracy: both sensitivity and specificity
    """
    # Sensitivity: P(Positive | Sick)
    sensitivity = test_accuracy
    
    # Specificity: P(Negative | Healthy)
    specificity = test_accuracy
    false_positive_rate = 1 - specificity
    
    # Bayes theorem
    numerator = sensitivity * disease_rate
    denominator = (sensitivity * disease_rate + 
                   false_positive_rate * (1 - disease_rate))
    
    return numerator / denominator

def show_bayes():
    """Show the surprising result"""
    print("\n" + "="*60)
    print("PROBLEM 2: BAYES THEOREM (Doctor's Dilemma)")
    print("="*60)
    
    disease_rate = 0.001  # 0.1%
    test_accuracy = 0.99  # 99%
    
    prob_sick = bayes_disease(disease_rate, test_accuracy)
    
    print(f"\nGiven:")
    print(f"  - Disease affects: {disease_rate*100}% of people")
    print(f"  - Test accuracy: {test_accuracy*100}% (both ways)")
    print(f"  - Patient tests POSITIVE")
    
    print(f"\nProbability patient is actually sick: {prob_sick*100:.1f}%")
    
    print("\nWhy so low?")
    print("  - Disease is RARE (0.1%)")
    print("  - Test has 1% false positive rate")
    print("  - In 10,000 people:")
    print("    • 10 are sick → ~10 test positive ✓")
    print("    • 9,990 are healthy → ~100 test positive ✗ (false alarms!)")
    print("    • Total positives: 110")
    print("    • Actually sick: 10")
    print("    • Probability: 10/110 ≈ 9%")
    
    print("\n✓ Most positive tests are FALSE ALARMS when disease is rare!")

# ============================================================================
# PROBLEM 3: SHANNON ENTROPY
# ============================================================================

"""
THEORY 3: WHAT IS ENTROPY?

Entropy = How much "surprise" or "information" in an event
Measured in BITS

Formula: H(X) = -Σ p_i × log₂(p_i)

INTUITION:
- Fair coin (50/50): Always surprising → High entropy (1 bit)
- Biased coin (99/1): Almost never surprising → Low entropy (0.08 bits)

WHY?
- Fair coin: You learn 1 bit each flip (full information)
- Biased coin: You usually guess right, rarely learn anything

EXAMPLES:

Coin A (50% heads):
  H = -0.5×log₂(0.5) - 0.5×log₂(0.5)
    = -0.5×(-1) - 0.5×(-1)
    = 0.5 + 0.5 = 1 bit
  
Coin B (99% heads):
  H = -0.99×log₂(0.99) - 0.01×log₂(0.01)
    ≈ -0.99×(-0.014) - 0.01×(-6.64)
    ≈ 0.014 + 0.066 ≈ 0.08 bits

Coin C (1% heads):
  Same as Coin B by symmetry ≈ 0.08 bits

MEANING:
- 1 bit: Need 1 bit to describe each flip (fair coin)
- 0.08 bits: Need only 0.08 bits per flip on average (very predictable)

If you flip fair coin 100 times: need 100 bits to store
If you flip 99% coin 100 times: need only ~8 bits (can compress!)
"""

def shannon_entropy(probabilities):
    """
    Calculate Shannon entropy
    probabilities: list of probabilities (must sum to 1)
    Returns: entropy in bits
    """
    entropy = 0
    for p in probabilities:
        if p > 0:  # log(0) is undefined
            entropy -= p * math.log2(p)
    return entropy

def show_entropy():
    """Show entropy for different coins"""
    print("\n" + "="*60)
    print("PROBLEM 3: SHANNON ENTROPY (Information Content)")
    print("="*60)
    
    coins = {
        "A (Fair)": [0.5, 0.5],
        "B (99% biased)": [0.99, 0.01],
        "C (1% biased)": [0.01, 0.99]
    }
    
    print("\nCoin Analysis:")
    print("-" * 60)
    
    for name, probs in coins.items():
        entropy = shannon_entropy(probs)
        p_heads = probs[0]
        
        print(f"\n{name}:")
        print(f"  P(Heads) = {p_heads*100:.0f}%")
        print(f"  Entropy = {entropy:.3f} bits")
        
        if entropy > 0.9:
            print(f"  → High surprise! Each flip gives ~1 bit of info")
        else:
            print(f"  → Low surprise! Very predictable, little info")
    
    print("\n" + "-"*60)
    print("WHY THE DIFFERENCE?")
    print("-" * 60)
    
    print("\nFair coin (50/50):")
    print("  - Always uncertain about result")
    print("  - Each flip gives 1 full bit of information")
    print("  - Can't compress: need 1 bit per flip")
    
    print("\n99% biased coin:")
    print("  - Almost always get same result")
    print("  - Rarely surprised → little information")
    print("  - Can compress: 100 flips ≈ 8 bits")
    print("  - Just mark the rare exceptions!")
    
    print("\nREAL WORLD:")
    print("  - English text: ~1-2 bits per letter (predictable)")
    print("  - Random data: 8 bits per byte (unpredictable)")
    print("  - Compression works by exploiting low entropy!")

# ============================================================================
# BONUS: VISUALIZE ENTROPY
# ============================================================================

def plot_entropy_curve():
    """Show how entropy changes with bias"""
    import matplotlib.pyplot as plt
    
    # Try different coin biases
    biases = [i/100 for i in range(1, 100)]
    entropies = [shannon_entropy([p, 1-p]) for p in biases]
    
    plt.figure(figsize=(10, 6))
    plt.plot(biases, entropies, 'b-', linewidth=2)
    plt.axhline(y=1.0, color='r', linestyle='--', label='Max entropy (1 bit)')
    plt.axvline(x=0.5, color='g', linestyle='--', label='Fair coin (50%)')
    
    # Mark special points
    plt.plot([0.5], [1.0], 'ro', markersize=10, label='Fair (1.0 bit)')
    plt.plot([0.99], [shannon_entropy([0.99, 0.01])], 'go', 
             markersize=10, label='99% biased (0.08 bits)')
    
    plt.xlabel('P(Heads)', fontsize=12)
    plt.ylabel('Entropy (bits)', fontsize=12)
    plt.title('Shannon Entropy vs Coin Bias', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('entropy_curve.png', dpi=150)
    print("\n[Saved: entropy_curve.png]")

# ============================================================================
# RUN EVERYTHING
# ============================================================================

if __name__ == "__main__":
    print_complexity_classes()
    show_bayes()
    show_entropy()
    
    try:
        plot_entropy_curve()
    except:
        print("\n(Matplotlib not available for plotting)")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("1. Complexity:")
    print("   P < NP ≤ NP-Complete ≤ NP-Hard < Undecidable")
    print("   (easy → hard → very hard → impossible)")
    print("\n2. Bayes:")
    print("   Rare disease + imperfect test = mostly false alarms")
    print("   9% chance of actually being sick despite positive test!")
    print("\n3. Entropy:")
    print("   Fair coin = 1 bit (max info)")
    print("   Biased coin = 0.08 bits (little info)")
    print("   More predictable = less information = more compressible")
    print("\n✓ All problems solved! 🎉")
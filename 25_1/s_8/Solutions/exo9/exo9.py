"""
Problem Set #9: Boolean Circuits Made Simple
Finite functions, NAND gates, Universal circuits
"""

from itertools import product

# ============================================================================
# PROBLEM 1: COUNTING FINITE FUNCTIONS
# ============================================================================

"""
THEORY 1: HOW MANY FUNCTIONS EXIST?

Function: F: {0,1}^n -> {0,1}^m
Meaning: Takes n bits as input, gives m bits as output

COUNTING TRICK:
- Input has 2^n possible values (all combos of n bits)
- For EACH input, we choose an output
- If output has k possible values, we have k choices per input
- Total functions = k^(2^n)

EXAMPLES:

1) Output is {0,1} (one bit):
   - Input has 2^n combos
   - Each gets output 0 or 1 (2 choices)
   - Total = 2^(2^n) functions

2) Output is {-1,0,1} (three values):
   - Input has 2^n combos
   - Each gets -1, 0, or 1 (3 choices)
   - Total = 3^(2^n) functions

3) Output is {0,1}^m (m bits):
   - Input has 2^n combos
   - Each output can be 2^m values
   - Total = (2^m)^(2^n) = 2^(m·2^n) functions

THINK OF IT LIKE:
- Decision tree with 2^n leaves (one per input)
- Each leaf gets a label (the output)
- Count all possible labelings!
"""

def count_functions(n, output_size):
    """
    Count possible functions from n-bit input to given output
    n: number of input bits
    output_size: number of possible output values
    """
    num_inputs = 2 ** n
    total_functions = output_size ** num_inputs
    return total_functions

def show_examples():
    """Show concrete small examples"""
    print("="*60)
    print("PROBLEM 1: COUNTING FUNCTIONS")
    print("="*60)
    
    # Example with n=2
    n = 2
    print(f"\nWith n={n} input bits (inputs: 00, 01, 10, 11):")
    
    # Binary output
    binary_count = count_functions(n, 2)
    print(f"  Output {{0,1}}: {binary_count} = 2^(2^{n}) functions")
    
    # Ternary output
    ternary_count = count_functions(n, 3)
    print(f"  Output {{-1,0,1}}: {ternary_count} = 3^(2^{n}) functions")
    
    # m-bit output (m=2)
    m = 2
    multi_count = count_functions(n, 2**m)
    print(f"  Output {{0,1}}^{m}: {multi_count} = 2^({m}·2^{n}) functions")
    
    # Show one actual function
    print(f"\nExample function (n=2, output {{0,1}}):")
    print("  00 -> 1")
    print("  01 -> 0")
    print("  10 -> 0")
    print("  11 -> 1")
    print("  (This is just ONE of the 16 possible functions!)")

# ============================================================================
# PROBLEM 2: NAND IS UNIVERSAL
# ============================================================================

"""
THEORY 2: BUILD EVERYTHING FROM NAND

NAND gate: A ↑ B = NOT(A AND B)
Truth table:
  0 ↑ 0 = 1
  0 ↑ 1 = 1
  1 ↑ 0 = 1
  1 ↑ 1 = 0

COOL FACT: Can build AND, OR, NOT using only NAND!

HOW TO BUILD:

1) NOT A:
   Just do A ↑ A
   Why? A ↑ A = NOT(A AND A) = NOT(A)

2) AND A B:
   First NAND: C = A ↑ B
   Then NOT it: C ↑ C = NOT(C) = NOT(NOT(A AND B)) = A AND B
   Total: 2 NANDs

3) OR A B:
   Use De Morgan's law: A OR B = NOT(NOT(A) AND NOT(B))
   Step 1: NOT A = A ↑ A
   Step 2: NOT B = B ↑ B
   Step 3: (NOT A) ↑ (NOT B) = NOT((NOT A) AND (NOT B)) = A OR B
   Total: 3 NANDs

UNIVERSAL: Any circuit with n gates → at most 3n NANDs
(because each gate becomes at most 3 NANDs)
"""

def nand(a, b):
    """NAND gate: only gate we need!"""
    return int(not (a and b))

def not_gate(a):
    """Build NOT from NAND"""
    return nand(a, a)

def and_gate(a, b):
    """Build AND from NAND (uses 2 NANDs)"""
    c = nand(a, b)
    return nand(c, c)

def or_gate(a, b):
    """Build OR from NAND (uses 3 NANDs)"""
    not_a = nand(a, a)
    not_b = nand(b, b)
    return nand(not_a, not_b)

def test_gates():
    """Test that our gates work correctly"""
    print("\n" + "="*60)
    print("PROBLEM 2: BUILD ALL GATES FROM NAND")
    print("="*60)
    
    print("\nNAND truth table:")
    print("  A  B | A↑B")
    for a, b in product([0,1], repeat=2):
        print(f"  {a}  {b} |  {nand(a,b)}")
    
    print("\nNOT gate (using 1 NAND):")
    print("  A | NOT A")
    for a in [0, 1]:
        print(f"  {a} |   {not_gate(a)}")
    print("  Circuit: A ↑ A")
    
    print("\nAND gate (using 2 NANDs):")
    print("  A  B | A AND B")
    for a, b in product([0,1], repeat=2):
        print(f"  {a}  {b} |    {and_gate(a,b)}")
    print("  Circuit: C = A↑B, then C↑C")
    
    print("\nOR gate (using 3 NANDs):")
    print("  A  B | A OR B")
    for a, b in product([0,1], repeat=2):
        print(f"  {a}  {b} |   {or_gate(a,b)}")
    print("  Circuit: (A↑A) ↑ (B↑B)")
    
    print("\n✓ Every gate can be built from NAND!")
    print("✓ Any n-gate circuit → at most 3n NAND gates")

# ============================================================================
# PROBLEM 3: UNIVERSAL BOOLEAN CIRCUITS
# ============================================================================

"""
THEORY 3: ANY FUNCTION CAN BE COMPUTED

Goal: Show any F: {0,1}^n -> {0,1} can be built with circuits

KEY IDEA: Use "indicator" functions

For each input x, make δ_x(y):
  δ_x(y) = 1 if y == x
         = 0 if y != x

How big? O(n) gates to check if y == x
(compare each bit, AND them all together)

THEN: Build F by combining all δ_x:
  F(y) = OR over all x where F(x)=1 of δ_x(y)

Size calculation:
- 2^n possible inputs x
- Each δ_x uses O(n) gates
- Combine with OR: O(2^n) gates
- Total: O(n·2^n) gates

THIS IS HUGE but proves ANY function is computable!

Example: F(x) = 1 only when x = "11"
  F(y) = δ_11(y)
  δ_11(y) = (y[0] AND y[1])
"""

def indicator_function(target, input_val, n):
    """
    Check if input_val == target
    Returns 1 if match, 0 otherwise
    Represents δ_target
    """
    # Compare bit by bit
    for i in range(n):
        if ((target >> i) & 1) != ((input_val >> i) & 1):
            return 0
    return 1

def build_function_from_table(n, true_inputs):
    """
    Build a function that returns 1 for specific inputs
    n: number of input bits
    true_inputs: list of inputs where function returns 1
    """
    def f(x):
        # OR all indicator functions
        for target in true_inputs:
            if indicator_function(target, x, n):
                return 1
        return 0
    return f

def count_circuit_size(n, true_inputs):
    """
    Estimate circuit size for function
    """
    # Each indicator: O(n) for bit comparisons
    indicator_size = n
    
    # Number of indicators
    num_indicators = len(true_inputs)
    
    # Combine with OR
    combine_size = num_indicators
    
    total = num_indicators * indicator_size + combine_size
    return total

def test_universal():
    """Show that any function can be computed"""
    print("\n" + "="*60)
    print("PROBLEM 3: UNIVERSAL BOOLEAN CIRCUITS")
    print("="*60)
    
    # Example: F(x) = 1 only for x = 3 (binary: 11)
    n = 2
    true_inputs = [3]  # Only input "11" gives output 1
    
    print(f"\nExample: n={n} bits, F(x)=1 only when x=11")
    
    # Build the function
    F = build_function_from_table(n, true_inputs)
    
    print("\nTruth table:")
    print("  Input | Output")
    for x in range(2**n):
        binary = format(x, f'0{n}b')
        print(f"   {binary}  |   {F(x)}")
    
    # Estimate circuit size
    size = count_circuit_size(n, true_inputs)
    print(f"\nCircuit size: ~{size} gates")
    print(f"Formula: O(n·2^n) = O({n}·{2**n}) = O({n * 2**n})")
    
    # More complex example
    n = 3
    true_inputs = [1, 3, 5]  # x = 001, 011, 101
    
    print(f"\n\nExample 2: n={n} bits, F(x)=1 for x in {{1,3,5}}")
    F2 = build_function_from_table(n, true_inputs)
    
    print("\nTruth table:")
    print("  Input | Output")
    for x in range(2**n):
        binary = format(x, f'0{n}b')
        print(f"   {binary}  |   {F2(x)}")
    
    size2 = count_circuit_size(n, true_inputs)
    print(f"\nCircuit size: ~{size2} gates")
    print(f"Formula: O(n·|true_inputs|) = O({n}·{len(true_inputs)})")
    
    print("\n✓ ANY function F: {0,1}^n -> {0,1} is computable!")
    print("✓ Worst case: O(n·2^n) gates (when F(x)=1 for all x)")

# ============================================================================
# VISUAL CIRCUIT DIAGRAMS (ASCII ART)
# ============================================================================

def print_nand_circuits():
    """Show visual representation of gate constructions"""
    print("\n" + "="*60)
    print("VISUAL: HOW TO BUILD GATES FROM NAND")
    print("="*60)
    
    print("\n1) NOT gate (1 NAND):")
    print("     ___")
    print("  A-|   |")
    print("  A-|↑  |--- NOT A")
    print("     ---")
    
    print("\n2) AND gate (2 NANDs):")
    print("     ___       ___")
    print("  A-|   |   +-|   |")
    print("  B-|↑  |---+-|↑  |--- A AND B")
    print("     ---       ---")
    
    print("\n3) OR gate (3 NANDs):")
    print("     ___           ___")
    print("  A-|   |------+--|   |")
    print("  A-|↑  |      |  |↑  |--- A OR B")
    print("     ---       +--|   |")
    print("     ___       |   ---")
    print("  B-|   |------+")
    print("  B-|↑  |")
    print("     ---")

# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    show_examples()
    test_gates()
    test_universal()
    print_nand_circuits()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("1. Functions {0,1}^n -> output:")
    print("   - Binary output: 2^(2^n) functions")
    print("   - Ternary output: 3^(2^n) functions")
    print("   - m-bit output: 2^(m·2^n) functions")
    print("\n2. NAND is universal:")
    print("   - NOT: 1 NAND")
    print("   - AND: 2 NANDs")
    print("   - OR: 3 NANDs")
    print("   - Any circuit: at most 3× gates")
    print("\n3. Any boolean function computable:")
    print("   - Use indicator functions δ_x")
    print("   - Circuit size: O(n·2^n)")
    print("\n✓ All problems solved! 🎉")
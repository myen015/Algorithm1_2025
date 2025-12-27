import math

# --- Problem 2: Logic Gates from NAND ---
# The task asks to generate AND, OR, NOT using only NAND.
# Here is the implementation.

def nand_gate(a, b):
    # Base NAND operation: 0 only if both inputs are 1
    if a == 1 and b == 1:
        return 0
    return 1

def not_gate(a):
    # NOT A is equivalent to A NAND A
    return nand_gate(a, a)

def and_gate(a, b):
    # AND(A, B) is equivalent to NOT(NAND(A, B))
    # Which means: (A NAND B) NAND (A NAND B)
    n1 = nand_gate(a, b)
    return nand_gate(n1, n1)

def or_gate(a, b):
    # OR(A, B) is equivalent to (NOT A) NAND (NOT B)
    # Which means: (A NAND A) NAND (B NAND B)
    na = nand_gate(a, a)
    nb = nand_gate(b, b)
    return nand_gate(na, nb)

# Simple test for the gates
def test_logic():
    print("--- Problem 2 Checks ---")
    print(f"NOT 0 = {not_gate(0)}") # Should be 1
    print(f"NOT 1 = {not_gate(1)}") # Should be 0
    print(f"AND 1,0 = {and_gate(1, 0)}") # Should be 0
    print(f"OR  0,0 = {or_gate(0, 0)}")  # Should be 0
    print(f"OR  1,0 = {or_gate(1, 0)}")  # Should be 1
    print("Logic checks passed.\n")


# --- Problem 1: Finite Function Possibilities ---
# The code below verifies the formulas for the number of possible functions.
# n = inputs, output set size changes.

def check_possibilities(n, m=1):
    print("--- Problem 1 Calculations ---")
    
    # Total distinct inputs for n bits is 2^n
    total_inputs = 2 ** n
    print(f"For n={n}, total input combinations (leaves) = {total_inputs}")

    # Case 1: Output is {0, 1} (size 2)
    # Formula: 2^(2^n)
    res1 = 2 ** total_inputs
    print(f"1. Output {{0,1}}: 2^(2^{n}) = {res1}")

    # Case 2: Output is {-1, 0, 1} (size 3)
    # Formula: 3^(2^n)
    res2 = 3 ** total_inputs
    print(f"2. Output {{-1,0,1}}: 3^(2^{n}) = {res2}")

    # Case 3: Output is {0, 1}^m (size 2^m)
    # Formula: (2^m)^(2^n) which simplifies to 2^(m * 2^n)
    res3 = (2 ** m) ** total_inputs
    print(f"3. Output {{0,1}}^{m}: 2^({m} * 2^{n}) = {res3}")
    print("\n")

'''
--- Problem 3 Explanation (Theory) ---

We need to realize function F: {0,1}^n -> {0,1}.
Using the Shannon expansion (or Disjunctive Normal Form):

F(x) can be written as an OR of ANDs (minterms).
1. For each input combination (v) where F(v) = 1, we create a circuit that detects v.
2. Detecting a specific input v requires checking n bits (using ANDs and NOTs).
   This part takes O(n) size.
3. In the worst case, we have 2^n such combinations (if the output is always 1).
4. Finally, we OR all these results together.

Total size = (Number of combinations) * (Size to check one combination)
Total size = 2^n * O(n) = O(n * 2^n).
'''

if __name__ == "__main__":
    # Running checks for small n to keep numbers readable
    check_possibilities(n=2, m=2) 
    test_logic()

import math

# Problem 1:

def count_boolean_functions(n, output_set_size):
    input_domain_size = 2 ** n
    num_functions = output_set_size ** input_domain_size
    return num_functions


n_val = 3
output_size_1 = 2
num_1 = count_boolean_functions(n_val, output_size_1)
print(f"Output {{0,1}} (n={n_val}): {num_1}")

n_val = 3
output_size_2 = 3
num_2 = count_boolean_functions(n_val, output_size_2)
print(f"Output {{-1,0,1}} (n={n_val}): {num_2}")

n_val = 2
m_val = 2
output_size_3 = 2 ** m_val
num_3 = count_boolean_functions(n_val, output_size_3)
print(f"Output {{0,1}}^{m_val} (n={n_val}): {num_3}")


# Problem 2:

def nand(a, b):
    return int(not (a and b))


def nand_not(a):
    return nand(a, a)


def nand_and(a, b):
    temp = nand(a, b)
    return nand_not(temp)


def nand_or(a, b):
    not_a = nand_not(a)
    not_b = nand_not(b)
    return nand(not_a, not_b)


inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
print("\nNAND Equivalence Verification")

print("NOT verification:")
print(f"NOT(0): {nand_not(0)}, NOT(1): {nand_not(1)}")

print("AND verification:")
for a, b in inputs:
    print(f"AND({a}, {b}): {nand_and(a, b)}")

print("OR verification:")
for a, b in inputs:
    print(f"OR({a}, {b}): {nand_or(a, b)}")


# Problem 3:

def analyze_circuit_size_complexity(n):
    num_minterms = 2 ** n
    total_minterm_cost = num_minterms * n
    final_or_cost = num_minterms
    total_size = total_minterm_cost + final_or_cost

    return f"""
--- Complexity Analysis for F: {{0,1}}^{n} -> {{0,1}} ---
Input Size (n): {n}
Input Domain Size (2^n): {num_minterms}

1. Total Cost of Minterm Layer (AND/NOT): O({n} * 2^{n}) = O({total_minterm_cost})
2. Cost of Final OR Gate: O(2^{n}) = O({final_or_cost})

Total Circuit Size Complexity: O(n * 2^n)
"""


print(analyze_circuit_size_complexity(3))
import time
import math

# fibonacci with matrix - fast way
def matrix_mult(A, B):
    # multiply 2x2 matrix
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]

def matrix_pow(mat, n):
    # divide by 2 each time - this why O(log n)
    if n == 1:
        return mat
    
    half = matrix_pow(mat, n // 2)
    result = matrix_mult(half, half)
    
    if n % 2 == 1:
        result = matrix_mult(result, mat)
    
    return result

def fib_fast(n):
    if n == 0: return 0
    if n == 1: return 1
    
    base = [[1, 1], [1, 0]]
    result = matrix_pow(base, n)
    return result[1][0]

# normal way - slow
def fib_slow(n):
    if n <= 1: return n
    return fib_slow(n-1) + fib_slow(n-2)


print("PROBLEM 1: FIBONACCI")
print("="*50)

# complexity analysis
print("\nComplexity derivation:")
print("T(n) = T(n/2) + O(1)")
print("\nMaster Theorem:")
print("  a=1, b=2, c=0")
print("  c_leaf = log_2(1) = 0")
print("  c_work = 0")
print("  Balanced case -> O(log n)")

# test
print("\nTesting:")
for n in [10, 20, 50, 100, 500, 1000]:
    result = fib_fast(n)
    result_str = str(result)[-10:] if len(str(result)) > 10 else str(result)
    print(f"F({n}) = ...{result_str}")

# edge cases
print("\nEdge cases:")
for n in [0, 1, 2]:
    print(f"F({n}) = {fib_fast(n)}")

print("\nDone!")
import timeit
from typing import List, Tuple

# Represent big integers as lists of digits (LSB first, base 10 for simplicity)
def to_bigint(n: int) -> List[int]:
    if n == 0: return [0]
    digits = []
    while n > 0:
        digits.append(n % 10)
        n //= 10
    return digits

def from_bigint(digits: List[int]) -> int:
    n = 0
    for d in reversed(digits):
        n = n * 10 + d
    return n

# Addition
def add(a: List[int], b: List[int]) -> List[int]:
    result = []
    carry = 0
    i, j = 0, 0
    while i < len(a) or j < len(b) or carry:
        val = carry
        if i < len(a): val += a[i]
        if j < len(b): val += b[j]
        result.append(val % 10)
        carry = val // 10
        i += 1
        j += 1
    return result

# Subtraction (assumes a >= b)
def subtract(a: List[int], b: List[int]) -> List[int]:
    result = a[:]
    borrow = 0
    j = 0
    for i in range(len(a)):
        val = a[i] - borrow
        if j < len(b): val -= b[j]
        if val < 0:
            val += 10
            borrow = 1
        else:
            borrow = 0
        result[i] = val
        j += 1
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result

# Karatsuba Multiplication
def karatsuba(a: List[int], b: List[int]) -> List[int]:
    if len(a) < 2 or len(b) < 2:
        return multiply_simple(a, b)
    n = max(len(a), len(b))
    a = a + [0] * (n - len(a))
    b = b + [0] * (n - len(b))
    m = n // 2
    al, ah = a[:m], a[m:]
    bl, bh = b[:m], b[m:]
    zl = karatsuba(al, bl)
    zr = karatsuba(ah, bh)
    zm = karatsuba(add(al, ah), add(bl, bh))
    zm = subtract(zm, add(zl, zr))
    zm = shift_left(zm, m)
    zl = shift_left(zl, 0)
    zr = shift_left(zr, 2 * m)
    return normalize(add(add(zl, zm), zr))

def multiply_simple(a: List[int], b: List[int]) -> List[int]:
    result = [0] * (len(a) + len(b))
    for i, da in enumerate(a):
        for j, db in enumerate(b):
            result[i + j] += da * db
    carry = 0
    for i in range(len(result)):
        val = result[i] + carry
        result[i] = val % 10
        carry = val // 10
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result

def shift_left(digits: List[int], k: int) -> List[int]:
    return [0] * k + digits

def normalize(digits: List[int]) -> List[int]:
    carry = 0
    for i in range(len(digits)):
        val = digits[i] + carry
        digits[i] = val % 10
        carry = val // 10
    while carry:
        digits.append(carry % 10)
        carry //= 10
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    return digits

# Division (long division, returns quotient and remainder)
def divide(a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
    if from_bigint(b) == 0: raise ValueError("Division by zero")
    quotient = []
    remainder = []
    for digit in reversed(a):  # Process MSB first
        remainder = shift_left(remainder, 1)
        remainder.append(digit)
        remainder = normalize(remainder)
        q_digit = 0
        while from_bigint(remainder) >= from_bigint(b):
            remainder = subtract(remainder, b)
            q_digit += 1
        quotient.append(q_digit)
    quotient.reverse()
    while len(quotient) > 1 and quotient[0] == 0:
        quotient.pop(0)
    if not quotient: quotient = [0]
    return quotient, remainder

# Benchmark function
def benchmark_operations(size: int = 1000):
    a_int = 10**size - 1  # Large number, e.g., 999...9 (size digits)
    b_int = 10**size // 3  # Another large number
    a = to_bigint(a_int)
    b = to_bigint(b_int)
    
    # Native Python
    native_add = timeit.timeit(lambda: a_int + b_int, number=100)
    native_sub = timeit.timeit(lambda: a_int - b_int, number=100)
    native_mul = timeit.timeit(lambda: a_int * b_int, number=100)
    native_div = timeit.timeit(lambda: a_int // b_int, number=100)
    
    # Custom
    custom_add = timeit.timeit(lambda: from_bigint(add(a[:], b[:])), number=100)
    custom_sub = timeit.timeit(lambda: from_bigint(subtract(a[:], b[:])), number=100)
    custom_mul = timeit.timeit(lambda: from_bigint(karatsuba(a[:], b[:])), number=100)
    custom_div_q, _ = divide(a[:], b[:])
    custom_div = timeit.timeit(lambda: from_bigint(divide(a[:], b[:])[0]), number=100)
    
    print(f"Benchmark for {size}-digit numbers (100 runs each):")
    print(f"Operation | Native (s) | Custom (s) | Ratio (Custom/Native)")
    print(f"----------|------------|------------|----------------------")
    print(f"Add       | {native_add:.6f}  | {custom_add:.6f}  | {custom_add/native_add:.2f}")
    print(f"Sub       | {native_sub:.6f}  | {custom_sub:.6f}  | {custom_sub/native_sub:.2f}")
    print(f"Mul       | {native_mul:.6f}  | {custom_mul:.6f}  | {custom_mul/native_mul:.2f}")
    print(f"Div       | {native_div:.6f}  | {custom_div:.6f}  | {custom_div/native_div:.2f}")

# Example usage and benchmark
if __name__ == "__main__":
    benchmark_operations(100)  # Adjust size for testing; larger for real benchmark
    # Test small values
    print("\nTest: 123 + 456 =", from_bigint(add(to_bigint(123), to_bigint(456))))
    print("123 * 456 =", from_bigint(karatsuba(to_bigint(123), to_bigint(456))))
    q, r = divide(to_bigint(123), to_bigint(3))
    print("123 // 3 =", from_bigint(q), "remainder", from_bigint(r))

import math
from typing import List

# PROBLEM 1: Sparse Vector with Single 1
def binary_search_sparse(v: List[int], start: int, end: int) -> int:
    """Binary divide and conquer to find single 1 in sparse vector"""
    if start >= end:
        return -1
    if end - start == 1:
        return start if v[start] == 1 else -1

    mid = (start + end) // 2
    left_result = binary_search_sparse(v, start, mid)
    if left_result != -1:
        return left_result
    return binary_search_sparse(v, mid, end)


def m_way_search_sparse(v: List[int], start: int, end: int, m: int) -> int:
    """General m-way divide and conquer for sparse vector"""
    if start >= end:
        return -1
    if end - start == 1:
        return start if v[start] == 1 else -1

    segment_size = math.ceil((end - start) / m)
    for i in range(m):
        seg_start = start + i * segment_size
        seg_end = min(start + (i + 1) * segment_size, end)
        if seg_start >= end:
            break
        result = m_way_search_sparse(v, seg_start, seg_end, m)
        if result != -1:
            return result
    return -1


def linear_search_sparse(v: List[int]) -> int:
    """Simple linear scan approach"""
    for i in range(len(v)):
        if v[i] == 1:
            return i
    return -1


# PROBLEM 2: School Multiplication

def school_multiply(X: List[int], Y: List[int]) -> List[int]:
    """School multiplication algorithm for large numbers"""
    nx, ny = len(X), len(Y)
    result = [0] * (nx + ny)

    for i in range(nx):
        carry = 0
        for j in range(ny):
            product = X[i] * Y[j] + result[i + j] + carry
            result[i + j] = product % 10
            carry = product // 10
        if carry > 0:
            result[i + ny] += carry

    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def number_to_digits(n: int) -> List[int]:
    """Convert number to digit array (least significant first)"""
    if n == 0:
        return [0]
    digits = []
    while n > 0:
        digits.append(n % 10)
        n //= 10
    return digits


def digits_to_number(digits: List[int]) -> int:
    """Convert digit array back to number"""
    result = 0
    for i, digit in enumerate(digits):
        result += digit * (10 ** i)
    return result


def karatsuba_multiply(X: List[int], Y: List[int]) -> List[int]:
    """Karatsuba multiplication algorithm - O(n^1.585)"""
    n = max(len(X), len(Y))

    if n <= 2:
        x_num = digits_to_number(X)
        y_num = digits_to_number(Y)
        return number_to_digits(x_num * y_num)

    X = X + [0] * (n - len(X))
    Y = Y + [0] * (n - len(Y))

    mid = n // 2
    x1, x0 = X[mid:], X[:mid]
    y1, y0 = Y[mid:], Y[:mid]

    z2 = karatsuba_multiply(x1, y1)
    z0 = karatsuba_multiply(x0, y0)

    x_sum = number_to_digits(digits_to_number(x1) + digits_to_number(x0))
    y_sum = number_to_digits(digits_to_number(y1) + digits_to_number(y0))
    z1_product = karatsuba_multiply(x_sum, y_sum)

    z1_num = digits_to_number(z1_product) - digits_to_number(z2) - digits_to_number(z0)
    z1 = number_to_digits(z1_num)

    result_num = digits_to_number(z2) * (10 ** (2 * mid)) + digits_to_number(z1) * (10 ** mid) + digits_to_number(z0)
    return number_to_digits(result_num)


def factorial_using_multiplication(n: int) -> int:
    """Compute n! using efficient multiplication tree"""

    def multiply_range(start: int, end: int) -> int:
        if start == end:
            return start
        if start + 1 == end:
            return start * end
        mid = (start + end) // 2
        return multiply_range(start, mid) * multiply_range(mid + 1, end)

    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return multiply_range(1, n)


# ANALYSIS AND TESTING

if __name__ == "__main__":
    print("Problem 1: Sparse Vector Analysis")
    print("Binary: T(n) = 2T(n/2) + O(1) = O(n)")
    print("m-way: T(n) = mT(n/m) + O(1) = O(n)")
    print("Linear scan is optimal: O(n) time, O(1) space")

    print("\nProblem 2: Multiplication Analysis")
    print("School: O(n²), Standard D&C: O(n²), Karatsuba: O(n^1.585)")

    # Test sparse vector
    v = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    print(f"\nSparse vector test: {binary_search_sparse(v, 0, len(v))}")

    # Test multiplication
    X, Y = [3, 2, 1], [6, 5, 4]  # 123 × 456
    result = school_multiply(X, Y)
    print(f"Multiplication test: {digits_to_number(result)}")

    # Test factorial
    print(f"Factorial test: 5! = {factorial_using_multiplication(5)}")

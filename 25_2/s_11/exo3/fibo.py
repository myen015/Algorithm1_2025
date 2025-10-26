import numpy as np

def fibonacci_matrix(n):
    """
    Compute nth Fibonacci number using matrix exponentiation
    Time complexity: O(log n)
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    # Base matrix for Fibonacci sequence
    base_matrix = np.array([[1, 1], [1, 0]], dtype=object)
    
    def matrix_power(matrix, power):
        """Fast matrix exponentiation"""
        result = np.eye(2, dtype=object)
        while power > 0:
            if power % 2 == 1:
                result = np.dot(result, matrix)
            matrix = np.dot(matrix, matrix)
            power //= 2
        return result
    
    # Raise matrix to power (n-1)
    powered_matrix = matrix_power(base_matrix, n - 1)
    
    # Multiply by initial vector [F1, F0] = [1, 0]
    result_vector = np.dot(powered_matrix, np.array([1, 0]))
    return result_vector[0]

# Test the implementation
print("Fibonacci numbers using matrix method:")
for i in range(15):
    fib_num = fibonacci_matrix(i)
    print(f"F({i}) = {fib_num}")

# Verification with classical approach
def fibonacci_classic(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print("\nMethod verification:")
for i in [10, 15, 20]:
    matrix_result = fibonacci_matrix(i)
    classic_result = fibonacci_classic(i)
    print(f"F({i}): matrix = {matrix_result}, classic = {classic_result}")
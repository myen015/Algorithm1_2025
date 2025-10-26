def matrix_mult(A, B):
    c00 = A[0][0]*B[0][0] + A[0][1]*B[1][0]
    c01 = A[0][0]*B[0][1] + A[0][1]*B[1][1]
    c10 = A[1][0]*B[0][0] + A[1][1]*B[1][0]
    c11 = A[1][0]*B[0][1] + A[1][1]*B[1][1]
    return [[c00, c01],
            [c10, c11]]

def matrix_power(M, n):
    if n == 1:
        return M
    if n % 2 == 0:
        half = matrix_power(M, n // 2)
        return matrix_mult(half, half)
    else:
        return matrix_mult(M, matrix_power(M, n - 1))

def fib(n):
    if n == 0:
        return 0
    F = [[1, 1],
         [1, 0]]
    Fn = matrix_power(F, n)
    return Fn[0][1]   # F(n) лежит в позиции (0,1)



if __name__ == "__main__":
    print("F(10) =", fib(10))
    print("F(20) =", fib(20))
    print("F(50) =", fib(50))

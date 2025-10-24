import time
import math

def mult(a, b, ops):
    ops[0] += 1
    r = [[0,0],[0,0]]
    r[0][0] = a[0][0]*b[0][0] + a[0][1]*b[1][0]
    r[0][1] = a[0][0]*b[0][1] + a[0][1]*b[1][1]
    r[1][0] = a[1][0]*b[0][0] + a[1][1]*b[1][0]
    r[1][1] = a[1][0]*b[0][1] + a[1][1]*b[1][1]
    return r

def power(m, n, ops):
    ops[0] += 1
    if n == 1:
        return m
    
    temp = power(m, n//2, ops)
    temp = mult(temp, temp, ops)
    
    if n % 2 == 1:
        temp = mult(temp, m, ops)
    return temp

def fib(n):
    if n == 0: return 0, 0
    if n == 1: return 1, 0
    ops = [0]
    m = [[1,1],[1,0]]
    res = power(m, n, ops)
    return res[1][0], ops[0]


print("Problem 1: Fibonacci")
print("="*50)

print("\nComplexity:")
print("T(n) = T(n/2) + O(1)")
print("Master Theorem: a=1, b=2, c=0")
print("c_leaf = log_2(1) = 0 = c_work")
print("Result: O(log n)")

print("\nVerification:")
print(f"{'n':<10} {'ops':<10} {'log2(n)':<10} {'ratio'}")
for n in [10, 20, 50, 100, 500]:
    r, ops = fib(n)
    log_n = math.log2(n)
    print(f"{n:<10} {ops:<10} {log_n:<10.2f} {ops/log_n:.2f}")

print("\nEdge cases:")
for n in [0, 1, 2, 5]:
    r, ops = fib(n)
    print(f"fib({n}) = {r}")

print("\nLarge test:")
for n in [1000, 10000, 50000]:
    t1 = time.time()
    r, ops = fib(n)
    t2 = time.time()
    print(f"n={n}: time={t2-t1:.5f}s")
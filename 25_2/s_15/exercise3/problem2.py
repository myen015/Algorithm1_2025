import time

def fib_slow(n):
    if n <= 1:
        return n
    return fib_slow(n-1) + fib_slow(n-2)

memo = {}
def fib_fast(n):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_fast(n-1) + fib_fast(n-2)
    return memo[n]

n = 35

start = time.time()
slow_value = fib_slow(n)
slow_time = time.time() - start

start = time.time()
fast_value = fib_fast(n)
fast_time = time.time() - start

print("n =", n)
print("Slow result:", slow_value, "| Time:", slow_time)
print("Fast result:", fast_value, "| Time:", fast_time)

import random

def knapsack(w, v, cap):
    n = len(w)
    dp = [[0]*(cap+1) for _ in range(n+1)]
    ops = 0
    
    for i in range(1, n+1):
        for c in range(1, cap+1):
            ops += 1
            if w[i-1] > c:
                dp[i][c] = dp[i-1][c]
            else:
                dp[i][c] = max(dp[i-1][c], v[i-1] + dp[i-1][c-w[i-1]])
    
    # find items
    items = []
    c = cap
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i-1][c]:
            items.append(i-1)
            c -= w[i-1]
    items.reverse()
    
    return dp[n][cap], items, ops

def greedy(w, v, cap):
    n = len(w)
    items = [(v[i]/w[i], i) for i in range(n)]
    items.sort(reverse=True)
    
    val = 0
    weight = 0
    selected = []
    for r, i in items:
        if weight + w[i] <= cap:
            val += v[i]
            weight += w[i]
            selected.append(i)
    return val, selected


print("Problem 2: Knapsack")
print("="*50)

print("\n1. Greedy fails:")
w = [6, 5, 5]
v = [30, 25, 25]
cap = 10

g_val, g_items = greedy(w, v, cap)
d_val, d_items, _ = knapsack(w, v, cap)

print(f"weights: {w}, values: {v}, cap: {cap}")
print(f"Greedy: val={g_val}, items={g_items}")
print(f"DP: val={d_val}, items={d_items}")
print(f"Difference: {d_val - g_val}")

print("\n2. Complexity:")
print("Time: O(n*W)")
print("Space: O(n*W)")

print("\n3. Verification:")
print(f"{'n':<8} {'W':<8} {'n*W':<10} {'ops':<10} {'ratio'}")
for n, W in [(5,10), (10,20), (20,50), (50,100)]:
    random.seed(42)
    wt = [random.randint(1,10) for _ in range(n)]
    vl = [random.randint(1,20) for _ in range(n)]
    _, _, ops = knapsack(wt, vl, W)
    print(f"{n:<8} {W:<8} {n*W:<10} {ops:<10} {ops/(n*W):.2f}")

print("\n4. Test case:")
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 8

val, items, ops = knapsack(weights, values, capacity)
print(f"w={weights}, v={values}, cap={capacity}")
print(f"value: {val}")
print(f"items: {items}")
print(f"weights: {[weights[i] for i in items]}")
print(f"total weight: {sum(weights[i] for i in items)}")

print("\n5. Edge cases:")
tests = [
    ([1], [10], 0, "no cap"),
    ([1], [10], 5, "one item"),
    ([1,1,1,1], [1,1,1,1], 2, "same items"),
    ([5,5,5], [10,20,30], 10, "same weights"),
    ([1,2,3,4,5], [5,4,3,2,1], 10, "sorted"),
    ([5,4,3,2,1], [1,2,3,4,5], 10, "reverse"),
]

for w, v, c, name in tests:
    val, items, _ = knapsack(w, v, c)
    print(f"{name}: val={val}, items={items}")
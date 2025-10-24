import random

# knapsack DP
def knapsack(weights, values, capacity):
    n = len(weights)
    
    # make table
    dp = [[0]*(capacity+1) for _ in range(n+1)]
    
    # fill table
    for i in range(1, n+1):
        for w in range(1, capacity+1):
            wt = weights[i-1]
            val = values[i-1]
            
            if wt > w:
                dp[i][w] = dp[i-1][w]
            else:
                # max of take or dont take
                dp[i][w] = max(dp[i-1][w], val + dp[i-1][w-wt])
    
    # find which items
    result = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            result.append(i-1)
            w -= weights[i-1]
    
    return dp[n][capacity], result[::-1]

# space optimized - O(W) not O(n*W)
def knapsack_opt(weights, values, capacity):
    n = len(weights)
    prev = [0]*(capacity+1)
    curr = [0]*(capacity+1)
    
    for i in range(1, n+1):
        for w in range(1, capacity+1):
            wt = weights[i-1]
            val = values[i-1]
            
            if wt > w:
                curr[w] = prev[w]
            else:
                curr[w] = max(prev[w], val + prev[w-wt])
        
        prev, curr = curr, prev
    
    return prev[capacity]

# greedy - WRONG
def knapsack_greedy(weights, values, capacity):
    n = len(weights)
    items = [(values[i]/weights[i], i) for i in range(n)]
    items.sort(reverse=True)
    
    total = 0
    selected = []
    weight = 0
    
    for ratio, i in items:
        if weight + weights[i] <= capacity:
            selected.append(i)
            total += values[i]
            weight += weights[i]
    
    return total, selected


print("PROBLEM 2: KNAPSACK")
print("="*50)

# why not greedy
print("\n1. Why greedy fail:")
w = [6, 5, 5]
v = [30, 25, 25]
cap = 10

greedy_val, greedy_items = knapsack_greedy(w, v, cap)
optimal_val, optimal_items = knapsack(w, v, cap)

print(f"Greedy: value={greedy_val}, items={greedy_items}")
print(f"Optimal: value={optimal_val}, items={optimal_items}")
print(f"Greedy is wrong! Difference: {optimal_val - greedy_val}")

# complexity
print("\n2. Complexity:")
print("Time: O(n*W)")
print("  Two loops: n and W")
print("  Work per iteration: O(1)")
print("  Total: n*W")
print("\nSpace: O(n*W) or optimized O(W)")

# course example
print("\n3. Course example:")
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 8

max_val, selected = knapsack(weights, values, capacity)
print(f"Items: w={weights}, v={values}")
print(f"Capacity: {capacity}")
print(f"Solution: items={selected}, value={max_val}")
print(f"Total weight: {sum(weights[i] for i in selected)}")

# space optimization
print("\n4. Space optimization:")
opt_val = knapsack_opt(weights, values, capacity)
print(f"Standard DP: O(n*W) = O({len(weights)}*{capacity}) space")
print(f"Optimized: O(W) = O({capacity}) space")
print(f"Result same: {max_val == opt_val}")

# edge cases
print("\n5. Edge cases:")
test_cases = [
    ([1], [1], 0, "no capacity"),
    ([1], [1], 1, "one item"),
    ([5,5,5], [1,1,1], 10, "same weights"),
]

for w, v, c, desc in test_cases:
    val, items = knapsack(w, v, c)
    print(f"{desc}: value={val}, items={items}")

print("\nDone!")
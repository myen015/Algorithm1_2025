def knapsack_01(weights, values, capacity):
    """
    Solve 0/1 knapsack problem using dynamic programming
    Returns: max_value, selected_items
    """
    n = len(weights)
    # DP table initialization
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # Fill DP table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                # Maximum of: take item or skip item
                dp[i][w] = max(dp[i-1][w], 
                              values[i-1] + dp[i-1][w - weights[i-1]])
            else:
                dp[i][w] = dp[i-1][w]
    
    # Backtrack to find selected items
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)
            w -= weights[i-1]
    
    return dp[n][capacity], selected_items

def knapsack_optimized(weights, values, capacity):
    """
    Space-optimized version using O(capacity) memory
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # Iterate backwards to avoid overwriting
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    
    return dp[capacity]

# Example usage
if __name__ == "__main__":
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5
    
    max_value, items = knapsack_01(weights, values, capacity)
    max_value_opt = knapsack_optimized(weights, values, capacity)
    
    print("0/1 Knapsack Problem Solution")
    print(f"Weights: {weights}")
    print(f"Values: {values}")
    print(f"Capacity: {capacity}")
    print(f"Maximum value: {max_value}")
    print(f"Selected items: {items}")
    print(f"Optimized version result: {max_value_opt}")
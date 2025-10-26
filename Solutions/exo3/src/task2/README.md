0/1 KNAPSACK ALGORITHM

1. WHY NOT GREEDY, WHY DYNAMIC PROGRAMMING

Greedy approach fails because it makes locally optimal choices without considering global optimality.

Example: Items with (weight, value) = (5, 10), (3, 9), (4, 8) and capacity 8

Greedy by value/weight ratio:

- Ratio: (10/5=2), (9/3=3), (8/4=2)
- Takes item 2 (w=3, v=9), then item 3 (w=4, v=8) = total value 17
- Remaining capacity 1, cannot fit item 1

Optimal solution:

- Take items 1 and 3 (w=5+3=8, v=10+9=19) = total value 19

Greedy gives 17, optimal is 19. Greedy fails.

Dynamic Programming works because:

- It considers all possible combinations systematically
- Builds up solutions by storing results of subproblems
- Ensures optimal substructure: optimal solution uses optimal solutions to smaller problems
- No greedy choice is made; instead all choices are evaluated

2. SOLVE KNAPSACK EXAMPLE

Standard recurrence:
dp[i][w] = maximum value using first i items with capacity w

Transition:
dp[i][w] = max(dp[i-1][w], dp[i-1]w-weight[i]] + value[i])

Either exclude item i or include it if it fits.

Time complexity: O(n × W) where n = number of items, W = capacity

3. SPACE COMPLEXITY TO O(W)

Standard DP uses O(n × W) space for 2D table.

Optimization: Use 1D array of size W+1

Key insight: When computing dp[i][w], we only need values from dp[i-1][*]

Algorithm:

- Maintain single 1D array: dp[w] = max value with capacity w
- Iterate items i from 1 to n
- For each item, iterate capacity w from W down to weight[i]
- Update: dp[w] = max(dp[w], dp[w-weight[i]] + value[i])

Iterate backwards to prevent using updated values from current item

Result: Space complexity becomes O(W) instead of O(n × W)

Time complexity remains O(n × W)

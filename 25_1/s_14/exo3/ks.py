print("Problem 2")

# Knapsack is not a greedy algorithm because choosing items based only on the best local ratio (value / weight) does not guarantee the best total result
# and we use dynamic programming to find the optimal combination

def ks(W, wt, val, n):
	tbl = [[0 for _ in range(W+1)] for _ in range(n+1)]
	for i in range(1, n+1):
		for w in range(1, W+1):

# dynprog[i][w] = max(dynprog[i-1][w], value[i-1] + dynprog[i-1][w - weight[i-1]]) if weight[i-1] <= w
# else dynprog[i][w] = dynprog[i-1][w]
# time complexity: O(n * W)

			if wt[i-1] <= w:
				a = val[i-1] + tbl[i-1][w-wt[i-1]]
				b = tbl[i-1][w]
				if a > b:
					tbl[i][w] = a
				else:
					tbl[i][w] = b
			else:
				tbl[i][w] = tbl[i-1][w]
	return tbl[n][W]


# we can reduce space to O(W) by using a single 1D list and iterating backward over capacities, the trick is to go from W down to weight[i] so we don’t overwrite data we need
# dp[w] = max(dp[w], val[i] + dp[w - wt[i]]), this keeps time O(n*W) but reduces memory to O(W)


# example
vals = [10, 100, 1000, 5, 20, 80, 6, 66, 666]
wts = [11, 13, 50, 22, 11, 5, 9, 6, 20]
Wmax = 56
print("Max value =", ks(Wmax, wts, vals, len(vals)))
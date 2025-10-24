def knapsack(W, weights, values):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i - 1] > w:
                dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])

    for i in range(n + 1):
        for j in range(W + 1):
            print(dp[i][j], end=' ')
        print()


    return dp[n][W]


def knapsack_optim(W, weights, values):
    n = len(weights)
    dp = [0] * (W + 1)

    for i in range(n):
        for w in range(W, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    for i in dp:
        print(i, end=" ")
    print()

    return dp[W]


n, W = map(int, input().split())
weights = [int(input()) for _ in range(n)]
values = [int(input()) for _ in range(n)]

print(knapsack(W, weights, values))
print(knapsack_optim(W, weights, values))


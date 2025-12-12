#include <stdio.h>

int max(int a, int b)
{
    return (a > b) ? a : b;
}

int knapSack(int W, int wt[], int val[], int n)
{
    int dp[W + 1];
    for (int w = 0; w <= W; w++)
        dp[w] = 0;

    for (int i = 0; i < n; i++)
    {
        for (int w = W; w >= wt[i]; w--)
        {
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]]);
        }
    }
    return dp[W];
}

int main()
{
    int values[] = {60, 100, 120};
    int weights[] = {10, 20, 30};
    int W = 50;
    int n = 3;

    printf("Maximum value = %d\n", knapSack(W, weights, values, n));
    return 0;
}

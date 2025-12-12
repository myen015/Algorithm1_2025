#include <bits/stdc++.h>
using namespace std;

int knapsack(int W, vector<int> &weights, vector<int> &values){
	int n = weights.size();
	
	vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
	for(int i = 1; i <= n; i++){
		for(int w = 0; w <= W; w++){
			if (weights[i - 1] > w) {
				dp[i][w] = dp[i - 1][w];
			} else {
				dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1]);	
			}
		}
	}
	return dp;
}
/*
why it's optimized
1) Instead of 2D array we use 1D array
2) We start indexing from right to left so we're sure that we made computation to each weight only 1 time
*/
int knapsack_optimized(int W, vector<int> &weights, vector<int> &values){
	int n = weights.size();
	vector<int> dp(W + 1,0);
	for(int i = 0; i < n; i++){
		for(int w = W; w >= weights[i]; w--){
			dp[w] = max(dp[w], dp[w - weights[i]] + values[i]);
		}
	}
	for(int i : dp){
		cout << i << ' ';
	}
	cout << '\n';
	return dp[W];
}

void solve() {
	int n, W;
	cin >> n >> W;
	vector<int> weights(n + 1);
	vector<int> values(n + 1);
	for(int i = 0; i < n; i++){
		cin >> weights[i];
	}
	for(int i = 0; i < n; i++){
		cin >> values[i];
	}
	cout << knapsack_optimized(W, weights, values);
}


int main(){
	int t = 1;
	while(t--){
		solve();
	}
}

	
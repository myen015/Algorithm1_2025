function knapsack01(weights, values, capacity) {
  const n = weights.length;
  const dp = Array(n + 1)
    .fill(null)
    .map(() => Array(capacity + 1).fill(0));

  for (let i = 1; i <= n; i++) {
    for (let w = 0; w <= capacity; w++) {
      dp[i][w] = dp[i - 1][w];

      if (weights[i - 1] <= w) {
        dp[i][w] = Math.max(
          dp[i][w],
          dp[i - 1][w - weights[i - 1]] + values[i - 1]
        );
      }
    }
  }

  const selected = [];
  let w = capacity;
  for (let i = n; i > 0; i--) {
    if (dp[i][w] !== dp[i - 1][w]) {
      selected.push(i - 1);
      w -= weights[i - 1];
    }
  }

  selected.reverse();
  return { maxValue: dp[n][capacity], selectedItems: selected };
}

function knapsack01Optimized(weights, values, capacity) {
  const n = weights.length;
  const dp = Array(capacity + 1).fill(0);

  for (let i = 0; i < n; i++) {
    for (let w = capacity; w >= weights[i]; w--) {
      dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
    }
  }

  return dp[capacity];
}

const weights = [2, 3, 4, 5];
const values = [3, 4, 5, 6];
const capacity = 8;

const result = knapsack01(weights, values, capacity);
console.log("Maximum value:", result.maxValue);
console.log("Selected items (indices):", result.selectedItems);
console.log(
  "Selected weights:",
  result.selectedItems.map((i) => weights[i])
);
console.log(
  "Selected values:",
  result.selectedItems.map((i) => values[i])
);
console.log(
  "Total weight:",
  result.selectedItems.reduce((sum, i) => sum + weights[i], 0)
);

console.log(
  "\nOptimized space solution max value:",
  knapsack01Optimized(weights, values, capacity)
);

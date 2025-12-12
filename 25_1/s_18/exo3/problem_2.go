package main

import (
	"fmt"
)

type Item struct {
	weight int
	value  int
	name   string
}

func knapsackDP(items []Item, capacity int) (int, []Item) {
	n := len(items)

	dp := make([][]int, n+1)
	for i := range dp {
		dp[i] = make([]int, capacity+1)
	}

	for i := 1; i <= n; i++ {
		for w := 0; w <= capacity; w++ {
			dp[i][w] = dp[i-1][w]

			if items[i-1].weight <= w {
				valueWithItem := dp[i-1][w-items[i-1].weight] + items[i-1].value
				if valueWithItem > dp[i][w] {
					dp[i][w] = valueWithItem
				}
			}
		}
	}

	selected := []Item{}
	w := capacity
	for i := n; i > 0; i-- {
		if dp[i][w] != dp[i-1][w] {
			selected = append(selected, items[i-1])
			w -= items[i-1].weight
		}
	}

	return dp[n][capacity], selected
}

func knapsackSpaceOptimized(items []Item, capacity int) int {
	dp := make([]int, capacity+1)

	for _, item := range items {
		for w := capacity; w >= item.weight; w-- {
			valueWithItem := dp[w-item.weight] + item.value
			if valueWithItem > dp[w] {
				dp[w] = valueWithItem
			}
		}
	}

	return dp[capacity]
}

func main() {
	items := []Item{
		{weight: 2, value: 3, name: "Item 1"},
		{weight: 3, value: 4, name: "Item 2"},
		{weight: 4, value: 5, name: "Item 3"},
		{weight: 5, value: 6, name: "Item 4"},
	}
	capacity := 8

	fmt.Println("0/1 Knapsack Problem")
	fmt.Printf("Capacity: %d\n\n", capacity)

	fmt.Println("Items:")
	for i, item := range items {
		fmt.Printf("%d. %s: weight=%d, value=%d, ratio=%.2f\n",
			i+1, item.name, item.weight, item.value,
			float64(item.value)/float64(item.weight))
	}

	// Solve using DP
	maxValue, selected := knapsackDP(items, capacity)

	fmt.Printf("\nDP Table (Course Example)\n")
	fmt.Println("Building table ks[i][w]:")

	n := len(items)
	dp := make([][]int, n+1)
	for i := range dp {
		dp[i] = make([]int, capacity+1)
	}

	for i := 1; i <= n; i++ {
		for w := 0; w <= capacity; w++ {
			dp[i][w] = dp[i-1][w]
			if items[i-1].weight <= w {
				valueWithItem := dp[i-1][w-items[i-1].weight] + items[i-1].value
				if valueWithItem > dp[i][w] {
					dp[i][w] = valueWithItem
				}
			}
		}
	}

	fmt.Print("i\\w ")
	for w := 0; w <= capacity; w++ {
		fmt.Printf("%3d", w)
	}
	fmt.Println()

	for i := 0; i <= n; i++ {
		fmt.Printf("%3d ", i)
		for w := 0; w <= capacity; w++ {
			fmt.Printf("%3d", dp[i][w])
		}
		fmt.Println()
	}

	fmt.Printf("\nSolution\n")
	fmt.Printf("Optimal value: ks[4][8] = %d\n", maxValue)
	totalWeight := 0
	for _, item := range selected {
		totalWeight += item.weight
	}
	fmt.Printf("Selected items: %s and %s\n", selected[1].name, selected[0].name)
	fmt.Printf("(weight: %d + %d = %d, value: %d + %d = %d)\n",
		selected[1].weight, selected[0].weight, totalWeight,
		selected[1].value, selected[0].value, maxValue)

	maxValueOptimized := knapsackSpaceOptimized(items, capacity)
	fmt.Printf("\nSpace-optimized result: %d (matches: %v)\n",
		maxValueOptimized, maxValue == maxValueOptimized)

	fmt.Println("\nWhy Greedy Fails?")
	fmt.Println("If we sort by value/weight ratio and take greedily:")

	greedyItems := make([]Item, len(items))
	copy(greedyItems, items)

	for i := 0; i < len(greedyItems); i++ {
		for j := i + 1; j < len(greedyItems); j++ {
			ratioI := float64(greedyItems[i].value) / float64(greedyItems[i].weight)
			ratioJ := float64(greedyItems[j].value) / float64(greedyItems[j].weight)
			if ratioJ > ratioI {
				greedyItems[i], greedyItems[j] = greedyItems[j], greedyItems[i]
			}
		}
	}

	greedyValue := 0
	greedyWeight := 0
	fmt.Println("Taking items by ratio:")
	for _, item := range greedyItems {
		if greedyWeight+item.weight <= capacity {
			fmt.Printf("  Take %s (w=%d, v=%d)\n", item.name, item.weight, item.value)
			greedyWeight += item.weight
			greedyValue += item.value
		} else {
			fmt.Printf("  Skip %s (doesn't fit)\n", item.name)
		}
	}
	fmt.Printf("Greedy value: %d (vs optimal: %d)\n", greedyValue, maxValue)
}

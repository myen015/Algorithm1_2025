package main

import "fmt"

type Graph map[int][]int

func EulerTour(g Graph, start int) []int {
	adj := make(map[int][]int, len(g))
	for v, neigh := range g {
		tmp := make([]int, len(neigh))
		copy(tmp, neigh)
		adj[v] = tmp
	}

	var stack []int
	var tour []int

	stack = append(stack, start)

	for len(stack) > 0 {
		v := stack[len(stack)-1]
		if len(adj[v]) == 0 {
			tour = append(tour, v)
			stack = stack[:len(stack)-1]
		} else {
			lastIdx := len(adj[v]) - 1
			u := adj[v][lastIdx]
			adj[v] = adj[v][:lastIdx]
			stack = append(stack, u)
		}
	}

	for i, j := 0, len(tour)-1; i < j; i, j = i+1, j-1 {
		tour[i], tour[j] = tour[j], tour[i]
	}

	return tour
}

func main() {
	g := Graph{
		0: {1, 3},
		1: {2},
		2: {0},
		3: {0},
	}

	tour := EulerTour(g, 0)
	fmt.Println("Euler tour:", tour)
}

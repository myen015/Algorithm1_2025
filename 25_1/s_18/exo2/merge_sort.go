package main

import (
	"exo2/sorts"
	"fmt"
)

func main() {
	a := []int{10, 6, 2, 1, 5, 8, 3, 4, 7, 9}
	sorted := sorts.MergeSort(a)
	fmt.Println("Result (MergeSort):", sorted)
}

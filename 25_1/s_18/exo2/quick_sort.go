package main

import (
	"exo2/sorts"
	"fmt"
)

func main() {
	a := []int{10, 6, 2, 1, 5, 8, 3, 4, 7, 9}

	fmt.Println("Result (QuickSort - random):     ", sorts.QuickSortRandom(a))
	fmt.Println("Result (QuickSort - median3):    ", sorts.QuickSortMedian3(a))
}

package main

import (
	"fmt"
)

type Matrix [2][2]int64

func multiply(a, b Matrix) Matrix {
	return Matrix{
		{a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]},
		{a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]},
	}
}

func matrixPower(mat Matrix, n int) Matrix {
	if n == 0 {
		return Matrix{{1, 0}, {0, 1}} // Identity matrix
	}
	if n == 1 {
		return mat
	}

	half := matrixPower(mat, n/2)
	result := multiply(half, half)

	if n%2 == 1 {
		result = multiply(result, mat)
	}

	return result
}

func fibonacciMatrix(n int) int64 {
	if n == 0 {
		return 0
	}
	if n == 1 {
		return 1
	}

	baseMat := Matrix{{1, 1}, {1, 0}}
	result := matrixPower(baseMat, n)

	return result[1][0]
}

func fibonacciModifiedMatrix(n int) int64 {
	if n == 0 {
		return 0
	}
	if n == 1 {
		return 1
	}

	modMat := Matrix{{2, 1}, {1, 1}}

	result := matrixPower(modMat, n/2)

	fn1 := result[0][0]*1 + result[0][1]*0
	fn := result[1][0]*1 + result[1][1]*0

	if n%2 == 0 {
		return fn
	}
	return fn1
}

func main() {
	fmt.Println("Method 1: Standard Matrix [[1,1],[1,0]]^n")
	fmt.Println("n\tF(n)")
	for i := 0; i <= 15; i++ {
		fmt.Printf("%d\t%d\n", i, fibonacciMatrix(i))
	}

	fmt.Println("\nMethod 2: Modified Matrix [[2,1],[1,1]]^(n/2)")
	fmt.Println("n\tF(n)")
	for i := 0; i <= 15; i++ {
		fmt.Printf("%d\t%d\n", i, fibonacciModifiedMatrix(i))
	}

	fmt.Println("\nResult: Both methods produce same results")
	testCases := []int{20, 30, 40, 50}
	for _, n := range testCases {
		method1 := fibonacciMatrix(n)
		method2 := fibonacciModifiedMatrix(n)
		match := "✓"
		if method1 != method2 {
			match = "✗"
		}
		fmt.Printf("F(%d): Method1=%d, Method2=%d %s\n", n, method1, method2, match)
	}
}

package main

import (
	"fmt"
	"math"
)

type Node struct {
	Weight   float64
	Children []*Node
}

func NewNode(weight float64, n int) *Node {
	node := &Node{
		Weight:   weight,
		Children: make([]*Node, n),
	}
	childWeight := weight / float64(n)
	for i := 0; i < n; i++ {
		node.Children[i] = &Node{
			Weight:   childWeight,
			Children: nil,
		}
	}
	return node
}

func GenerateTree(depth int, n int, initialWeight float64) *Node {
	if depth == 0 {
		return &Node{Weight: initialWeight, Children: nil}
	}

	node := &Node{
		Weight:   initialWeight,
		Children: make([]*Node, n),
	}

	childWeight := initialWeight / float64(n)
	for i := 0; i < n; i++ {
		node.Children[i] = GenerateTree(depth-1, n, childWeight)
	}

	return node
}

func DFSRecursive(node *Node) float64 {
	if node == nil {
		return 0
	}

	sum := node.Weight
	for _, child := range node.Children {
		sum += DFSRecursive(child)
	}

	return sum
}

func BFSRecursive(root *Node) float64 {
	if root == nil {
		return 0
	}

	queue := []*Node{root}
	return bfsRecursiveHelper(queue, 0)
}

func bfsRecursiveHelper(queue []*Node, sum float64) float64 {
	if len(queue) == 0 {
		return sum
	}

	node := queue[0]
	queue = queue[1:]

	sum += node.Weight

	for _, child := range node.Children {
		if child != nil {
			queue = append(queue, child)
		}
	}

	return bfsRecursiveHelper(queue, sum)
}

func BFSIterative(root *Node) float64 {
	if root == nil {
		return 0
	}

	sum := 0.0
	queue := []*Node{root}

	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]

		sum += node.Weight

		for _, child := range node.Children {
			if child != nil {
				queue = append(queue, child)
			}
		}
	}

	return sum
}

func DFSFlipSign(node *Node) float64 {
	if node == nil {
		return 0
	}

	node.Weight = -node.Weight
	sum := node.Weight

	for _, child := range node.Children {
		sum += DFSFlipSign(child)
	}

	return sum
}

func BFSFlipSign(root *Node) float64 {
	if root == nil {
		return 0
	}

	sum := 0.0
	queue := []*Node{root}

	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]

		node.Weight = -node.Weight
		sum += node.Weight

		for _, child := range node.Children {
			if child != nil {
				queue = append(queue, child)
			}
		}
	}

	return sum
}

func PrintTree(node *Node, prefix string, isLast bool) {
	if node == nil {
		return
	}

	connector := "├──"
	if isLast {
		connector = "└──"
	}

	fmt.Printf("%s%s %.6f\n", prefix, connector, node.Weight)

	newPrefix := prefix
	if isLast {
		newPrefix += "    "
	} else {
		newPrefix += "│   "
	}

	for i, child := range node.Children {
		PrintTree(child, newPrefix, i == len(node.Children)-1)
	}
}

func main() {
	fmt.Println("PROBLEM 1: N-ary Tree with Weight Distribution")
	fmt.Println("=" + "=" + "=" + "=" + "=" + "=" + "=" + "=" + "=" + "=")
	fmt.Println()

	testCases := []int{2, 3, 4, 5}

	for _, n := range testCases {
		fmt.Printf("\n--- Test Case: n = %d (depth = 3) ---\n", n)

		tree := GenerateTree(3, n, 1.0)

		fmt.Println("\nTree Structure:")
		PrintTree(tree, "", true)

		dfsSum := DFSRecursive(tree)
		fmt.Printf("\n3. DFS Recursive Sum: %.10f\n", dfsSum)
		if math.Abs(dfsSum-1.0) < 1e-9 {
			fmt.Println("   ✓ Correct! Sum equals 1")
		} else {
			fmt.Printf("   ✗ Error! Expected 1, got %.10f\n", dfsSum)
		}

		bfsIterSum := BFSIterative(tree)
		fmt.Printf("\n4. BFS Iterative Sum: %.10f\n", bfsIterSum)
		if math.Abs(bfsIterSum-1.0) < 1e-9 {
			fmt.Println("   ✓ Correct! Sum equals 1")
		} else {
			fmt.Printf("   ✗ Error! Expected 1, got %.10f\n", bfsIterSum)
		}

		bfsRecSum := BFSRecursive(tree)
		fmt.Printf("\n6. BFS Recursive Sum: %.10f\n", bfsRecSum)
		if math.Abs(bfsRecSum-1.0) < 1e-9 {
			fmt.Println("   ✓ Correct! Sum equals 1")
		} else {
			fmt.Printf("   ✗ Error! Expected 1, got %.10f\n", bfsRecSum)
		}

		tree2 := GenerateTree(3, n, 1.0)

		fmt.Println("\n5. Testing Sign Flip:")
		dfsFlip1 := DFSFlipSign(tree2)
		fmt.Printf("   First DFS (flip signs): %.10f\n", dfsFlip1)
		if math.Abs(dfsFlip1+1.0) < 1e-9 {
			fmt.Println("   ✓ Correct! Sum equals -1")
		} else {
			fmt.Printf("   ✗ Error! Expected -1, got %.10f\n", dfsFlip1)
		}

		dfsFlip2 := DFSFlipSign(tree2)
		fmt.Printf("   Second DFS (flip again): %.10f\n", dfsFlip2)
		if math.Abs(dfsFlip2-1.0) < 1e-9 {
			fmt.Println("   ✓ Correct! Sum equals 1")
		} else {
			fmt.Printf("   ✗ Error! Expected 1, got %.10f\n", dfsFlip2)
		}

		tree3 := GenerateTree(3, n, 1.0)

		bfsFlip1 := BFSFlipSign(tree3)
		fmt.Printf("   First BFS (flip signs): %.10f\n", bfsFlip1)
		if math.Abs(bfsFlip1+1.0) < 1e-9 {
			fmt.Println("   ✓ Correct! Sum equals -1")
		} else {
			fmt.Printf("   ✗ Error! Expected -1, got %.10f\n", bfsFlip1)
		}

		bfsFlip2 := BFSFlipSign(tree3)
		fmt.Printf("   Second BFS (flip again): %.10f\n", bfsFlip2)
		if math.Abs(bfsFlip2-1.0) < 1e-9 {
			fmt.Println("   ✓ Correct! Sum equals 1")
		} else {
			fmt.Printf("   ✗ Error! Expected 1, got %.10f\n", bfsFlip2)
		}

		fmt.Println()
	}

	fmt.Println("\n" + "=" + "=" + "=" + "=" + "=" + "=" + "=" + "=" + "=" + "=")
	fmt.Println("7. Why BFS Recursive is NOT Recommended:")
	fmt.Println("=" + "=" + "=" + "=" + "=" + "=" + "=" + "=" + "=" + "=")
	fmt.Println(`
DFS (Depth-First Search):
- Naturally recursive: goes deep before backtracking
- Call stack mirrors the tree structure
- Stack depth = O(height of tree)
- Recursive implementation is clean and intuitive

BFS (Breadth-First Search):
- Naturally iterative: explores level by level
- Requires a QUEUE (FIFO) data structure
- Recursive implementation is AWKWARD because:
  1. Recursion uses a STACK (LIFO), not a queue
  2. Must pass queue as parameter in each recursive call
  3. No natural "level-order" in recursion
  4. Less efficient: queue copying overhead
  5. Stack depth = O(max nodes in a level) = O(n)
  
Memory Analysis:
- DFS recursive: O(height) stack space
- BFS iterative: O(width) queue space
- BFS recursive: O(width) queue + O(levels) stack = WORSE!

Conclusion:
Use recursive DFS, but iterative BFS for efficiency and clarity.
BFS recursive version exists but is pedagogical only - not practical.
	`)
}

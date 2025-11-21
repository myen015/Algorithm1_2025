package main

import (
	"fmt"
	"strings"
)

type CSCGraph struct {
	ColPointers []int
	RowIndices  []int
	Values      []int
	Vertices    []string
	IsDirected  bool
}

func NewCSCGraph(colPtr, rowIdx, vals []int, vertices []string, directed bool) *CSCGraph {
	return &CSCGraph{
		ColPointers: colPtr,
		RowIndices:  rowIdx,
		Values:      vals,
		Vertices:    vertices,
		IsDirected:  directed,
	}
}

func (csc *CSCGraph) ToAdjacencyMatrix() [][]int {
	n := len(csc.Vertices)
	matrix := make([][]int, n)
	for i := range matrix {
		matrix[i] = make([]int, n)
	}

	for col := 0; col < n; col++ {
		start := csc.ColPointers[col]
		end := csc.ColPointers[col+1]
		for i := start; i < end; i++ {
			row := csc.RowIndices[i]
			val := csc.Values[i]
			matrix[row][col] = val
		}
	}

	return matrix
}

func (csc *CSCGraph) PrintAdjacencyMatrix() {
	matrix := csc.ToAdjacencyMatrix()
	n := len(csc.Vertices)

	fmt.Println("\nAdjacency Matrix:")
	fmt.Print("   ")
	for _, v := range csc.Vertices {
		fmt.Printf("%2s ", v)
	}
	fmt.Println()

	for i := 0; i < n; i++ {
		fmt.Printf("%s: ", csc.Vertices[i])
		for j := 0; j < n; j++ {
			fmt.Printf("%2d ", matrix[i][j])
		}
		fmt.Println()
	}
}

func (csc *CSCGraph) GetAdjacencyList() map[string][]string {
	adjList := make(map[string][]string)
	matrix := csc.ToAdjacencyMatrix()
	n := len(csc.Vertices)

	for i := 0; i < n; i++ {
		adjList[csc.Vertices[i]] = []string{}
		for j := 0; j < n; j++ {
			if matrix[i][j] > 0 {
				adjList[csc.Vertices[i]] = append(adjList[csc.Vertices[i]], csc.Vertices[j])
			}
		}
	}

	return adjList
}

func (csc *CSCGraph) PrintGraphDiagram() {
	adjList := csc.GetAdjacencyList()

	fmt.Println("\nGraph Diagram (Adjacency List):")
	if csc.IsDirected {
		fmt.Println("(Directed Graph)")
	} else {
		fmt.Println("(Undirected Graph)")
	}

	for _, v := range csc.Vertices {
		neighbors := adjList[v]
		if len(neighbors) > 0 {
			if csc.IsDirected {
				fmt.Printf("%s → %s\n", v, strings.Join(neighbors, ", "))
			} else {
				fmt.Printf("%s — %s\n", v, strings.Join(neighbors, ", "))
			}
		} else {
			fmt.Printf("%s (isolated)\n", v)
		}
	}
}

func (csc *CSCGraph) FindCycle() []string {
	if !csc.IsDirected {
		return nil
	}

	adjList := csc.GetAdjacencyList()
	visited := make(map[string]bool)
	recStack := make(map[string]bool)
	parent := make(map[string]string)

	var dfs func(string) []string
	dfs = func(v string) []string {
		visited[v] = true
		recStack[v] = true

		for _, u := range adjList[v] {
			if !visited[u] {
				parent[u] = v
				if cycle := dfs(u); cycle != nil {
					return cycle
				}
			} else if recStack[u] {
				cycle := []string{u}
				curr := v
				for curr != u {
					cycle = append([]string{curr}, cycle...)
					curr = parent[curr]
				}
				cycle = append(cycle, u)
				return cycle
			}
		}

		recStack[v] = false
		return nil
	}

	for _, v := range csc.Vertices {
		if !visited[v] {
			if cycle := dfs(v); cycle != nil {
				return cycle
			}
		}
	}

	return nil
}

func (csc *CSCGraph) PrintCycle() {
	cycle := csc.FindCycle()
	if cycle == nil {
		fmt.Println("\nNo cycle found in the graph.")
	} else {
		fmt.Println("\nCycle found:")
		fmt.Println(strings.Join(cycle, " → "))
	}
}

func (csc *CSCGraph) PrintVisualDiagram() {
	fmt.Println("\nVisual Representation:")
	adjList := csc.GetAdjacencyList()

	if csc.IsDirected {
		fmt.Println("Directed Graph:")
		fmt.Println()
		for _, v := range csc.Vertices {
			if len(adjList[v]) > 0 {
				for _, u := range adjList[v] {
					fmt.Printf("    %s ──→ %s\n", v, u)
				}
			}
		}
	} else {
		fmt.Println("Undirected Graph:")
		fmt.Println()
		printed := make(map[string]bool)
		for _, v := range csc.Vertices {
			for _, u := range adjList[v] {
				edge := v + "-" + u
				revEdge := u + "-" + v
				if !printed[edge] && !printed[revEdge] {
					fmt.Printf("    %s ──── %s\n", v, u)
					printed[edge] = true
					printed[revEdge] = true
				}
			}
		}
	}
}

func main() {
	fmt.Println("PROBLEM 2: Sparse Representation of Graphs (CSC Format)")
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println()

	vertices := []string{"A", "B", "C", "D", "E"}

	fmt.Println("╔" + strings.Repeat("═", 58) + "╗")
	fmt.Println("║ GRAPH 1: UNDIRECTED GRAPH                               ║")
	fmt.Println("╚" + strings.Repeat("═", 58) + "╝")

	colPtr1 := []int{0, 2, 5, 8, 11, 12}
	rowIdx1 := []int{1, 2, 0, 2, 3, 0, 1, 3, 1, 2, 4, 3}
	vals1 := []int{1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}

	graph1 := NewCSCGraph(colPtr1, rowIdx1, vals1, vertices, false)

	fmt.Println("\nCSC Representation:")
	fmt.Printf("col_pointers = %v\n", colPtr1)
	fmt.Printf("row_indices  = %v\n", rowIdx1)
	fmt.Printf("values       = %v\n", vals1)

	graph1.PrintAdjacencyMatrix()
	graph1.PrintGraphDiagram()
	graph1.PrintVisualDiagram()

	fmt.Println("\n" + strings.Repeat("─", 60))

	fmt.Println("\n╔" + strings.Repeat("═", 58) + "╗")
	fmt.Println("║ GRAPH 2: DIRECTED GRAPH                                 ║")
	fmt.Println("╚" + strings.Repeat("═", 58) + "╝")

	colPtr2 := []int{0, 0, 2, 4, 5, 7}
	rowIdx2 := []int{0, 3, 0, 1, 2, 1, 3}
	vals2 := []int{1, 1, 1, 1, 1, 1, 1}

	graph2 := NewCSCGraph(colPtr2, rowIdx2, vals2, vertices, true)

	fmt.Println("\nCSC Representation:")
	fmt.Printf("col_pointers = %v\n", colPtr2)
	fmt.Printf("row_indices  = %v\n", rowIdx2)
	fmt.Printf("values       = %v\n", vals2)

	graph2.PrintAdjacencyMatrix()
	graph2.PrintGraphDiagram()
	graph2.PrintVisualDiagram()
	graph2.PrintCycle()

	fmt.Println("\n" + strings.Repeat("═", 60))
	fmt.Println("SUMMARY")
	fmt.Println(strings.Repeat("═", 60))
	fmt.Println("\nGraph 1 (Undirected):")
	fmt.Println("  - 5 vertices: A, B, C, D, E")
	fmt.Println("  - Edges: A-B, A-C, B-C, B-D, C-D, D-E")
	fmt.Println("  - Properties: Connected, Has cycles")

	fmt.Println("\nGraph 2 (Directed):")
	fmt.Println("  - 5 vertices: A, B, C, D, E")
	fmt.Println("  - Edges: B→A, B→D, C→A, C→B, D→C, E→B, E→D")
	fmt.Println("  - Properties: Strongly connected component exists")
	cycle := graph2.FindCycle()
	if cycle != nil {
		fmt.Printf("  - Unique cycle: %s\n", strings.Join(cycle, " → "))
	}
}

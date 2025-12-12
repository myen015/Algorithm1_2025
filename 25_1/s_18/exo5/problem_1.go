package main

import (
	"fmt"
	"strings"
)

type Graph struct {
	V     int
	Edges []Edge
	Adj   map[int][]int
}

type Edge struct {
	U, V int
}

func NewGraph(v int) *Graph {
	return &Graph{
		V:     v,
		Edges: []Edge{},
		Adj:   make(map[int][]int),
	}
}

func (g *Graph) AddEdge(u, v int) {
	g.Edges = append(g.Edges, Edge{u, v})
	g.Adj[u] = append(g.Adj[u], v)
	g.Adj[v] = append(g.Adj[v], u)
}

func (g *Graph) IsConnectedAcyclic() bool {
	return g.IsConnected() && g.IsAcyclic()
}

func (g *Graph) IsForestComponent() bool {
	return g.IsAcyclic() && g.IsConnected()
}

func (g *Graph) IsConnectedWithVMinus1Edges() bool {
	return g.IsConnected() && len(g.Edges) == g.V-1
}

func (g *Graph) IsMinimallyConnected() bool {
	if !g.IsConnected() {
		return false
	}
	for i := range g.Edges {
		if !g.DisconnectsWhenEdgeRemoved(i) {
			return false
		}
	}
	return true
}

func (g *Graph) IsAcyclicWithVMinus1Edges() bool {
	return g.IsAcyclic() && len(g.Edges) >= g.V-1
}

func (g *Graph) IsMaximallyAcyclic() bool {
	if !g.IsAcyclic() {
		return false
	}
	for u := 0; u < g.V; u++ {
		for v := u + 1; v < g.V; v++ {
			if !g.HasEdge(u, v) {
				if !g.CreatesACycleWhenEdgeAdded(u, v) {
					return false
				}
			}
		}
	}
	return true
}

func (g *Graph) HasUniquePathBetweenAllPairs() bool {
	for u := 0; u < g.V; u++ {
		for v := u + 1; v < g.V; v++ {
			paths := g.CountPaths(u, v)
			if paths != 1 {
				return false
			}
		}
	}
	return true
}

func (g *Graph) IsConnected() bool {
	if g.V == 0 {
		return true
	}
	visited := make([]bool, g.V)
	g.dfs(0, visited)
	for _, v := range visited {
		if !v {
			return false
		}
	}
	return true
}

func (g *Graph) dfs(v int, visited []bool) {
	visited[v] = true
	for _, u := range g.Adj[v] {
		if !visited[u] {
			g.dfs(u, visited)
		}
	}
}

func (g *Graph) IsAcyclic() bool {
	visited := make([]bool, g.V)
	for v := 0; v < g.V; v++ {
		if !visited[v] {
			if g.hasCycleDFS(v, -1, visited) {
				return false
			}
		}
	}
	return true
}

func (g *Graph) hasCycleDFS(v, parent int, visited []bool) bool {
	visited[v] = true
	for _, u := range g.Adj[v] {
		if !visited[u] {
			if g.hasCycleDFS(u, v, visited) {
				return true
			}
		} else if u != parent {
			return true
		}
	}
	return false
}

func (g *Graph) HasEdge(u, v int) bool {
	for _, neighbor := range g.Adj[u] {
		if neighbor == v {
			return true
		}
	}
	return false
}

func (g *Graph) DisconnectsWhenEdgeRemoved(edgeIdx int) bool {
	tempG := NewGraph(g.V)
	for i, e := range g.Edges {
		if i != edgeIdx {
			tempG.AddEdge(e.U, e.V)
		}
	}
	return !tempG.IsConnected()
}

func (g *Graph) CreatesACycleWhenEdgeAdded(u, v int) bool {
	visited := make([]bool, g.V)
	return g.hasPath(u, v, visited)
}

func (g *Graph) hasPath(u, v int, visited []bool) bool {
	if u == v {
		return true
	}
	visited[u] = true
	for _, neighbor := range g.Adj[u] {
		if !visited[neighbor] {
			if g.hasPath(neighbor, v, visited) {
				return true
			}
		}
	}
	return false
}

func (g *Graph) CountPaths(u, v int) int {
	visited := make([]bool, g.V)
	return g.countPathsDFS(u, v, visited)
}

func (g *Graph) countPathsDFS(u, v int, visited []bool) int {
	if u == v {
		return 1
	}
	visited[u] = true
	count := 0
	for _, neighbor := range g.Adj[u] {
		if !visited[neighbor] {
			count += g.countPathsDFS(neighbor, v, visited)
		}
	}
	visited[u] = false
	return count
}

func VerifyTreeProperties(g *Graph) {
	fmt.Println("=== Verifying Tree Properties ===")
	fmt.Printf("Graph: V=%d, E=%d\n\n", g.V, len(g.Edges))

	p1 := g.IsConnectedAcyclic()
	p2 := g.IsForestComponent()
	p3 := g.IsConnectedWithVMinus1Edges()
	p4 := g.IsMinimallyConnected()
	p5 := g.IsAcyclicWithVMinus1Edges()
	p6 := g.IsMaximallyAcyclic()
	p7 := g.HasUniquePathBetweenAllPairs()

	fmt.Printf("Property 1 (Connected & Acyclic):           %v\n", p1)
	fmt.Printf("Property 2 (Forest Component):              %v\n", p2)
	fmt.Printf("Property 3 (Connected with V-1 edges):      %v\n", p3)
	fmt.Printf("Property 4 (Minimally Connected):           %v\n", p4)
	fmt.Printf("Property 5 (Acyclic with ≥V-1 edges):       %v\n", p5)
	fmt.Printf("Property 6 (Maximally Acyclic):             %v\n", p6)
	fmt.Printf("Property 7 (Unique Path between pairs):     %v\n", p7)

	allEqual := p1 == p2 && p2 == p3 && p3 == p4 && p4 == p5 && p5 == p6 && p6 == p7
	fmt.Printf("\nAll properties equivalent: %v\n", allEqual)
	if allEqual && p1 {
		fmt.Println("✓ This is a TREE - all definitions satisfied!")
	} else if allEqual && !p1 {
		fmt.Println("✗ This is NOT a tree - all definitions agree it's not a tree")
	}
	fmt.Println()
}

func main() {
	fmt.Println("PROBLEM 1: Graph and Tree Definitions Equivalence")
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println()

	fmt.Println("Test Case 1: Valid Tree")
	tree := NewGraph(5)
	tree.AddEdge(0, 1)
	tree.AddEdge(0, 2)
	tree.AddEdge(1, 3)
	tree.AddEdge(1, 4)
	VerifyTreeProperties(tree)

	fmt.Println("Test Case 2: Graph with Cycle (NOT a tree)")
	cycle := NewGraph(4)
	cycle.AddEdge(0, 1)
	cycle.AddEdge(1, 2)
	cycle.AddEdge(2, 3)
	cycle.AddEdge(3, 0)
	VerifyTreeProperties(cycle)

	fmt.Println("Test Case 3: Disconnected Graph (NOT a tree)")
	disconnected := NewGraph(4)
	disconnected.AddEdge(0, 1)
	disconnected.AddEdge(2, 3)
	VerifyTreeProperties(disconnected)

	fmt.Println("Test Case 4: Too Many Edges (NOT a tree)")
	tooMany := NewGraph(4)
	tooMany.AddEdge(0, 1)
	tooMany.AddEdge(0, 2)
	tooMany.AddEdge(1, 2)
	tooMany.AddEdge(1, 3)
	VerifyTreeProperties(tooMany)

	fmt.Println("\n" + strings.Repeat("=", 60))
	fmt.Println("MATHEMATICAL PROOF SUMMARY:")
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println(`
Equivalence Proof (Circular proof: 1→2→3→4→5→6→7→1):

(1 → 2): Connected acyclic ⇒ Forest component
   - If G is connected and acyclic, it forms one component of a forest.

(2 → 3): Forest component ⇒ Connected with V-1 edges
   - A tree with V vertices has exactly V-1 edges (proven by induction).

(3 → 4): Connected with V-1 edges ⇒ Minimally connected
   - With V-1 edges, removing any edge must disconnect (otherwise redundant).

(4 → 5): Minimally connected ⇒ Acyclic with ≥V-1 edges
   - If minimally connected, must be acyclic (cycle = redundant edge).
   - Connected graph needs at least V-1 edges.

(5 → 6): Acyclic with ≥V-1 edges ⇒ Maximally acyclic
   - Acyclic connected graph with V vertices has exactly V-1 edges.
   - Adding any edge creates a cycle (path already exists).

(6 → 7): Maximally acyclic ⇒ Unique path between pairs
   - If adding edge creates cycle, path already exists.
   - Path must be unique (otherwise already has cycle).

(7 → 1): Unique path ⇒ Connected and acyclic
   - Unique path between all pairs ⇒ connected.
   - Unique path ⇒ no cycles (cycle = multiple paths).

∴ All seven definitions are equivalent. QED.
	`)
}

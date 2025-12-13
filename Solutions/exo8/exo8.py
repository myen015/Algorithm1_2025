"""
Fundamental Algorithm Techniques - Problem Set #7
Graph operations and Bron-Kerbosch algorithm
"""

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch

# ============================================================================
# PROBLEM 1: GRAPH OPERATIONS
# ============================================================================

"""
THEORY PART 1: TRANSPOSE OF DIRECTED GRAPHS

What is transpose?
- Flip all arrows around
- If there's an arrow A->B, transpose has B->A
- Used in algorithms like finding strongly connected parts

Example:
Original:  A -> B -> C
Transpose: A <- B <- C  (or written as: C -> B -> A)
"""

def transpose_directed(graph):
    """
    Flip all arrows in a directed graph
    Input: graph as dict {node: [neighbors]}
    Output: transposed graph
    """
    transposed = {node: [] for node in graph}
    
    for node in graph:
        for neighbor in graph[node]:
            # If A->B exists, add B->A in transpose
            transposed[neighbor].append(node)
    
    return transposed

"""
THEORY PART 2: INVERSE/COMPLEMENT OF UNDIRECTED GRAPHS

What is inverse/complement?
- Flip what edges exist
- If edge exists, remove it
- If edge doesn't exist, add it
- Note: we don't add self-loops (node to itself)

Example with 3 nodes {A, B, C}:
Original:  A-B, B-C  (A and C not connected)
Inverse:   A-C       (A and C now connected, A-B and B-C gone)
"""

def inverse_undirected(graph, all_nodes):
    """
    Flip which edges exist in an undirected graph
    graph: dict {node: [neighbors]}
    all_nodes: list of all nodes in graph
    """
    inverse = {node: [] for node in all_nodes}
    
    for node in all_nodes:
        for other in all_nodes:
            if node != other:  # No self-loops
                # If edge doesn't exist, add it to inverse
                if other not in graph.get(node, []):
                    inverse[node].append(other)
    
    return inverse

"""
THEORY PART 3: WHAT HAPPENS WITH DENSE GRAPHS?

Dense graph = lots of edges (almost all possible connections)
Inverse of dense graph = sparse graph (very few edges)

Why? 
- Dense has many edges, inverse removes them
- Dense has few missing edges, inverse only keeps those few

Example:
Complete graph (all nodes connected): 4 nodes, 6 edges
Inverse of complete graph: 4 nodes, 0 edges (empty!)
"""

"""
THEORY PART 4: DUAL GRAPHS (for planar graphs)

What is a dual graph?
- Draw the original graph on paper (no edges crossing)
- Put a new node inside each face/region
- If two faces share an edge, connect their dual nodes

Example: Triangle
Original: 3 nodes A,B,C in triangle, 3 edges
Dual: 2 nodes (inside triangle, outside triangle), 3 edges

The dual basically swaps faces and vertices!
"""

"""
THEORY PART 5: WHY ONLY PLANAR GRAPHS HAVE DUALS?

Planar graph = can draw on paper with no edges crossing
Non-planar graph = edges MUST cross when drawn on paper

Why non-planar has no dual?
- Dual needs well-defined faces (regions)
- When edges cross, faces are ambiguous
- Can't tell which regions are separate

Example of non-planar: K5 (5 nodes all connected to each other)
- Has 5 nodes and 10 edges
- Can't draw on paper without crossings
- No clear faces, so no dual!

Another example: K3,3 (3 nodes on left, 3 on right, all connected)
- Called "utility graph" (3 houses, 3 utilities)
- Can't connect all without crossings
- Famous puzzle: impossible to solve!
"""

# ============================================================================
# EXAMPLES FOR PROBLEM 1
# ============================================================================

def show_transpose_example():
    """Show example of directed graph and its transpose"""
    print("="*70)
    print("EXAMPLE 1: TRANSPOSE OF DIRECTED GRAPH")
    print("="*70)
    
    # Original directed graph
    original = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }
    
    print("\nOriginal Graph (arrows show direction):")
    for node, neighbors in original.items():
        if neighbors:
            print(f"  {node} -> {neighbors}")
        else:
            print(f"  {node} -> (no outgoing edges)")
    
    # Get transpose
    trans = transpose_directed(original)
    
    print("\nTranspose Graph (all arrows flipped):")
    for node, neighbors in trans.items():
        if neighbors:
            print(f"  {node} -> {neighbors}")
        else:
            print(f"  {node} -> (no outgoing edges)")
    
    print("\nNotice: If A->B in original, then B->A in transpose!")

def show_inverse_example():
    """Show example of undirected graph and its inverse"""
    print("\n" + "="*70)
    print("EXAMPLE 2: INVERSE OF UNDIRECTED GRAPH")
    print("="*70)
    
    all_nodes = ['A', 'B', 'C', 'D']
    
    # Original undirected graph (sparse)
    original = {
        'A': ['B'],
        'B': ['A', 'C'],
        'C': ['B'],
        'D': []
    }
    
    print("\nOriginal Graph (undirected, so A-B means both ways):")
    edges = set()
    for node, neighbors in original.items():
        for neighbor in neighbors:
            edge = tuple(sorted([node, neighbor]))
            edges.add(edge)
    for edge in sorted(edges):
        print(f"  {edge[0]}-{edge[1]}")
    
    # Get inverse
    inv = inverse_undirected(original, all_nodes)
    
    print("\nInverse Graph (edges that didn't exist before):")
    edges = set()
    for node, neighbors in inv.items():
        for neighbor in neighbors:
            edge = tuple(sorted([node, neighbor]))
            edges.add(edge)
    for edge in sorted(edges):
        print(f"  {edge[0]}-{edge[1]}")
    
    print("\nNotice: Original was sparse (few edges), inverse is denser!")

def show_dense_inverse():
    """Show what happens with dense graph"""
    print("\n" + "="*70)
    print("EXAMPLE 3: INVERSE OF DENSE GRAPH")
    print("="*70)
    
    all_nodes = ['A', 'B', 'C']
    
    # Dense graph (almost complete)
    dense = {
        'A': ['B', 'C'],
        'B': ['A', 'C'],
        'C': ['A', 'B']
    }
    
    print("\nDense Graph (almost all possible edges):")
    print("  A-B, A-C, B-C  (complete triangle!)")
    
    inv = inverse_undirected(dense, all_nodes)
    
    print("\nInverse Graph:")
    has_edges = False
    for node, neighbors in inv.items():
        if neighbors:
            has_edges = True
            print(f"  {node}-{neighbors}")
    
    if not has_edges:
        print("  (EMPTY! No edges at all!)")
    
    print("\nLesson: Dense graph -> Sparse inverse")
    print("        Complete graph -> Empty inverse")

# ============================================================================
# PROBLEM 2: BRON-KERBOSCH ALGORITHM
# ============================================================================

"""
THEORY: WHAT IS BRON-KERBOSCH?

Goal: Find all "cliques" in a graph
Clique = group of nodes where everyone is connected to everyone else
Maximal clique = can't add any more nodes to it

The algorithm uses 3 sets:
- R: nodes we've picked so far (building the clique)
- P: nodes we can still pick from (candidates)
- X: nodes we already checked (to avoid duplicates)

How it works:
1. Start with R empty, P has all nodes, X empty
2. Pick a node from P
3. Try adding it to R (our clique)
4. Update P and X to only keep that node's neighbors
5. If P and X are both empty, we found a maximal clique!
6. Move node from P to X when done with it

It's like trying all combinations, but smart about pruning bad ones!
"""

def bron_kerbosch(R, P, X, graph, cliques, trace=False, level=0):
    """
    Find all maximal cliques in a graph
    
    R: current clique being built (set)
    P: candidate nodes we can add (set)
    X: nodes already processed (set)
    graph: adjacency list {node: [neighbors]}
    cliques: list to store found cliques
    trace: if True, print each step
    level: recursion depth (for pretty printing)
    """
    indent = "  " * level
    
    if trace:
        print(f"{indent}Call level {level}:")
        print(f"{indent}  R = {sorted(R) if R else 'empty'}")
        print(f"{indent}  P = {sorted(P) if P else 'empty'}")
        print(f"{indent}  X = {sorted(X) if X else 'empty'}")
    
    # Base case: if P and X are both empty, R is maximal clique
    if not P and not X:
        cliques.append(sorted(R))
        if trace:
            print(f"{indent}  *** FOUND MAXIMAL CLIQUE: {sorted(R)} ***")
        return
    
    # Try each node in P
    P_copy = P.copy()
    for node in P_copy:
        if trace:
            print(f"{indent}  -> Trying node {node}")
        
        # Get neighbors of this node
        neighbors = set(graph.get(node, []))
        
        # Recurse with:
        # - R + this node
        # - P filtered to neighbors
        # - X filtered to neighbors
        bron_kerbosch(
            R | {node},
            P & neighbors,
            X & neighbors,
            graph,
            cliques,
            trace,
            level + 1
        )
        
        # Move node from P to X
        P.remove(node)
        X.add(node)

def solve_bron_kerbosch():
    """Solve the given problem"""
    print("="*70)
    print("PROBLEM 2: BRON-KERBOSCH ALGORITHM")
    print("="*70)
    
    # Given graph
    graph = {
        "A": ["B", "C"],
        "B": ["A", "C"],
        "C": ["A", "B", "D"],
        "D": ["C"]
    }
    
    print("\nGraph structure:")
    print("  A-B, A-C, B-C, C-D")
    print("\nVisualization:")
    print("    A --- B")
    print("     \\   /")
    print("      \\ /")
    print("       C --- D")
    
    # Step 1: Initial call
    print("\n" + "-"*70)
    print("STEP 1: INITIAL CALL")
    print("-"*70)
    print("R = {} (empty - no nodes picked yet)")
    print("P = {A, B, C, D} (all nodes are candidates)")
    print("X = {} (empty - haven't processed any yet)")
    
    # Step 2: Trace first two recursive calls
    print("\n" + "-"*70)
    print("STEP 2: TRACE FIRST FEW CALLS (until first clique found)")
    print("-"*70)
    
    all_nodes = set(graph.keys())
    cliques_traced = []
    
    # We'll do a limited trace manually for clarity
    print("\nStarting algorithm...\n")
    bron_kerbosch(set(), all_nodes, set(), graph, cliques_traced, trace=True)
    
    # Step 3: List all maximal cliques
    print("\n" + "-"*70)
    print("STEP 3: ALL MAXIMAL CLIQUES")
    print("-"*70)
    
    cliques_full = []
    bron_kerbosch(set(), all_nodes, set(), graph, cliques_full, trace=False)
    
    print(f"\nFound {len(cliques_full)} maximal cliques:")
    for i, clique in enumerate(cliques_full, 1):
        print(f"  {i}. {clique} (size {len(clique)})")
    
    # Find maximum cliques (largest size)
    max_size = max(len(c) for c in cliques_full)
    max_cliques = [c for c in cliques_full if len(c) == max_size]
    
    print(f"\nMaximum cliques (largest size = {max_size}):")
    for clique in max_cliques:
        print(f"  {clique}")
    
    print("\nExplanation:")
    print("  - {A, B, C} is a clique: all 3 are connected to each other")
    print("  - {C, D} is a clique: both are connected")
    print("  - {A, B, C} is MAXIMUM because it's the biggest (size 3)")

# ============================================================================
# VISUALIZATION HELPERS
# ============================================================================

def draw_directed_and_transpose():
    """Draw directed graph and its transpose side by side"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Original
    G = nx.DiGraph()
    G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'D')])
    pos = nx.spring_layout(G, seed=42)
    
    ax1.set_title("Original Directed Graph", fontsize=14, fontweight='bold')
    nx.draw(G, pos, ax=ax1, with_labels=True, node_color='lightblue',
            node_size=1500, font_size=16, font_weight='bold',
            arrows=True, arrowsize=20, edge_color='gray', width=2)
    
    # Transpose
    G_trans = G.reverse()
    ax2.set_title("Transpose (Arrows Flipped)", fontsize=14, fontweight='bold')
    nx.draw(G_trans, pos, ax=ax2, with_labels=True, node_color='lightcoral',
            node_size=1500, font_size=16, font_weight='bold',
            arrows=True, arrowsize=20, edge_color='gray', width=2)
    
    plt.tight_layout()
    plt.savefig('transpose_example.png', dpi=150, bbox_inches='tight')
    print("\n[Saved: transpose_example.png]")

def draw_problem2_graph():
    """Draw the graph for problem 2"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    G = nx.Graph()
    G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'D')])
    
    pos = {
        'A': (0, 1),
        'B': (1, 1),
        'C': (0.5, 0),
        'D': (0.5, -1)
    }
    
    ax.set_title("Problem 2 Graph\nFind all maximal cliques", 
                 fontsize=14, fontweight='bold')
    
    # Draw the triangle (clique) with special color
    triangle = [('A', 'B'), ('B', 'C'), ('A', 'C')]
    nx.draw_networkx_edges(G, pos, edgelist=triangle, width=4, 
                          edge_color='green', alpha=0.6, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=[('C', 'D')], width=2,
                          edge_color='gray', ax=ax)
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue',
                          node_size=2000, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=18, font_weight='bold', ax=ax)
    
    # Add annotation
    ax.text(0.5, 0.5, 'Triangle = Clique!', fontsize=12,
            ha='center', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('problem2_graph.png', dpi=150, bbox_inches='tight')
    print("[Saved: problem2_graph.png]")

# ============================================================================
# RUN EVERYTHING
# ============================================================================

if __name__ == "__main__":
    # Problem 1 examples
    show_transpose_example()
    show_inverse_example()
    show_dense_inverse()
    
    print("\n" + "="*70)
    print("VISUALIZING GRAPHS...")
    print("="*70)
    draw_directed_and_transpose()
    
    # Problem 2
    print("\n")
    solve_bron_kerbosch()
    draw_problem2_graph()
    
    print("\n" + "="*70)
    print("ALL DONE! ✓")
    print("="*70)
    print("\nKey takeaways:")
    print("  1. Transpose = flip all arrows (directed graphs)")
    print("  2. Inverse = flip which edges exist (undirected graphs)")
    print("  3. Dense -> sparse when inversed")
    print("  4. Dual only works for planar graphs (no edge crossings)")
    print("  5. Bron-Kerbosch finds all maximal cliques")
    print("  6. A clique = everyone connected to everyone")
    
    plt.show()
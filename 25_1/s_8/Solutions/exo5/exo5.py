"""
Fundamental Algorithm Techniques - Problem Set #5 Solutions

Problem 1: Show that 7 tree definitions mean the same thing
Problem 2: Build graphs from CSC data
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# ============================================================================
# PROBLEM 1: WHY ALL 7 TREE DEFINITIONS ARE THE SAME
# ============================================================================

"""
EXPLANATION IN SIMPLE WORDS:

We have 7 ways to describe a tree. Let's show they all mean the same thing.

Definition 1: A tree is connected (all nodes linked) and has no loops.
Definition 2: A tree is a piece of a forest (forest = graph with no loops).
Definition 3: A tree is connected and has at most V-1 edges (V = number of nodes).
Definition 4: A tree is barely connected - cut any edge and it falls apart.
Definition 5: A tree has no loops and has at least V-1 edges.
Definition 6: A tree has no loops but adding any edge makes a loop.
Definition 7: A tree has exactly one path between any two nodes.

Let's show: 1→2→3→4→5→6→7→1 (each one leads to the next)

(1 → 2): Connected + no loops → One piece of forest
- If it's connected and has no loops, it's already a forest
- Being connected means it's all in one piece
- So it's one piece of a forest ✓

(2 → 3): One piece of forest → Connected with ≤V-1 edges
- A forest with V nodes and k pieces has V-k edges
- One piece means k=1, so we have V-1 edges
- One piece also means connected
- So: connected with V-1 edges (which is ≤V-1) ✓

(3 → 4): Connected with ≤V-1 edges → Barely connected
- To connect V nodes, you need at least V-1 edges
- If we have exactly V-1 and are connected, we can't lose any edge
- Why? Because V-1 is the minimum to stay connected
- Cut any edge and it breaks into pieces ✓

(4 → 5): Barely connected → No loops + at least V-1 edges
- If cutting any edge breaks it, there are no loops
  (loops would give alternate paths)
- Being connected means we need at least V-1 edges
- So: no loops + at least V-1 edges ✓

(5 → 6): No loops + at least V-1 edges → Maximally loop-free
- With no loops and V nodes, we can have at most V-1 edges
- We said "at least V-1", so we have exactly V-1 edges
- With V-1 edges and no loops, adding any new edge creates a loop
- Why? Because V-1 edges already connect everything barely ✓

(6 → 7): Maximally loop-free → Unique path between any pair
- If adding any edge makes a loop, we're already connected
- With no loops, there's only one way to go between any two nodes
- If there were two paths, that would be a loop ✓

(7 → 1): Unique path between any pair → Connected + no loops
- Unique path between all pairs means connected
- Only one path means no loops (loops give multiple paths)
- So: connected and no loops ✓

ALL DEFINITIONS ARE THE SAME! ✓
"""

# ============================================================================
# PROBLEM 2: REBUILD GRAPHS FROM CSC FORMAT
# ============================================================================

def csc_to_adjacency_matrix(col_pointers, row_indices, values, n_vertices):
    """
    Build adjacency matrix from CSC (Compressed Sparse Column) format
    
    CSC stores a matrix by columns:
    - col_pointers[i] tells where column i starts in row_indices
    - row_indices has the row numbers of non-zero entries
    - values has the actual numbers (all 1s here = edge exists)
    """
    # Start with all zeros
    matrix = np.zeros((n_vertices, n_vertices), dtype=int)
    
    # Go through each column
    for col in range(n_vertices):
        start = col_pointers[col]
        end = col_pointers[col + 1]
        
        # Fill in the non-zero entries for this column
        for idx in range(start, end):
            row = row_indices[idx]
            value = values[idx]
            matrix[row, col] = value
    
    return matrix

def print_adjacency_matrix(matrix, labels):
    """Pretty print the adjacency matrix with labels"""
    print("    " + "  ".join(labels))
    for i, row in enumerate(matrix):
        print(f"{labels[i]}   " + "  ".join(map(str, row)))

def find_cycle_in_directed_graph(adj_matrix, labels):
    """
    Find a cycle in a directed graph using DFS
    Returns the cycle as a list of node labels
    """
    n = len(adj_matrix)
    visited = [False] * n
    rec_stack = [False] * n  # Keeps track of nodes in current path
    parent = [-1] * n
    
    def dfs(node, path):
        visited[node] = True
        rec_stack[node] = True
        path.append(node)
        
        # Check all neighbors
        for neighbor in range(n):
            if adj_matrix[node][neighbor] == 1:  # Edge exists
                if not visited[neighbor]:
                    parent[neighbor] = node
                    result = dfs(neighbor, path)
                    if result:
                        return result
                elif rec_stack[neighbor]:
                    # Found a cycle! Build it
                    cycle = [neighbor]
                    idx = path.index(neighbor)
                    cycle.extend(path[idx+1:])
                    cycle.append(neighbor)
                    return cycle
        
        rec_stack[node] = False
        path.pop()
        return None
    
    # Try starting from each node
    for start in range(n):
        if not visited[start]:
            cycle = dfs(start, [])
            if cycle:
                return [labels[i] for i in cycle]
    
    return None

def draw_graph(adj_matrix, labels, directed=False, title="Graph"):
    """Draw the graph using networkx"""
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    
    # Add edges
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix)):
            if adj_matrix[i][j] == 1:
                G.add_edge(labels[i], labels[j])
    
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=1500, font_size=16, font_weight='bold',
            arrows=directed, arrowsize=20, edge_color='gray',
            arrowstyle='->', connectionstyle='arc3,rad=0.1')
    plt.title(title, fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    return G

# ============================================================================
# SOLVE GRAPH 1 (UNDIRECTED)
# ============================================================================

print("=" * 60)
print("GRAPH 1 (UNDIRECTED)")
print("=" * 60)

# Given data
col_pointers_1 = [0, 2, 5, 8, 11, 12]
row_indices_1 = [1, 2, 0, 2, 3, 0, 1, 3, 1, 2, 4, 3]
values_1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
labels = ['A', 'B', 'C', 'D', 'E']

# (a) Build adjacency matrix
adj_matrix_1 = csc_to_adjacency_matrix(col_pointers_1, row_indices_1, values_1, 5)

print("\n(a) Adjacency Matrix:")
print_adjacency_matrix(adj_matrix_1, labels)

# (b) Draw the graph
print("\n(b) Graph diagram (displayed in plot)")
G1 = draw_graph(adj_matrix_1, labels, directed=False, title="Graph 1 (Undirected)")

# ============================================================================
# SOLVE GRAPH 2 (DIRECTED)
# ============================================================================

print("\n" + "=" * 60)
print("GRAPH 2 (DIRECTED)")
print("=" * 60)

# Given data
col_pointers_2 = [0, 0, 2, 4, 5, 7]
row_indices_2 = [0, 3, 0, 1, 2, 1, 3]
values_2 = [1, 1, 1, 1, 1, 1, 1]

# (a) Build adjacency matrix
adj_matrix_2 = csc_to_adjacency_matrix(col_pointers_2, row_indices_2, values_2, 5)

print("\n(a) Adjacency Matrix:")
print_adjacency_matrix(adj_matrix_2, labels)

# (b) Draw the graph
print("\n(b) Graph diagram (displayed in plot)")
G2 = draw_graph(adj_matrix_2, labels, directed=True, title="Graph 2 (Directed)")

# (c) Find the cycle
print("\n(c) Finding the unique cycle:")
cycle = find_cycle_in_directed_graph(adj_matrix_2, labels)
if cycle:
    cycle_str = " -> ".join(cycle)
    print(f"Cycle found: {cycle_str}")
else:
    print("No cycle found")

plt.show()

print("\n" + "=" * 60)
print("DONE!")
print("=" * 60)
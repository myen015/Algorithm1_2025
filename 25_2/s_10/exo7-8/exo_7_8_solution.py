import networkx as nx
import matplotlib.pyplot as plt
from collections import deque, defaultdict


# ============================================================================
# Problem Set #7: Graph Play & Bron-Kerbosch
# ============================================================================

def transpose_graph(graph):
    """Transpose directed graph (reverse edges)."""
    transposed = {v: [] for v in graph}
    for u in graph:
        for v in graph[u]:
            transposed[v].append(u)
    return transposed


def inverse_graph(graph):
    """Inverse of undirected graph (complement)."""
    all_vertices = set(graph.keys())
    inverse = {v: [] for v in graph}
    for u in graph:
        neighbors = set(graph[u])
        inverse[u] = sorted(list(all_vertices - neighbors - {u}))
    return inverse


def bron_kerbosch(R, P, X, graph, cliques):
    """Bron-Kerbosch algorithm to find all maximal cliques."""
    if len(P) == 0 and len(X) == 0:
        cliques.append(set(R))
        return
    
    P_list = list(P)
    for v in P_list:
        N_v = set(graph.get(v, []))
        bron_kerbosch(R | {v}, P & N_v, X & N_v, graph, cliques)
        P.remove(v)
        X.add(v)


def problem7():
    """Problem Set #7 solutions."""
    print("=" * 70)
    print("Problem Set #7: Graph Play & Bron-Kerbosch")
    print("=" * 70)
    
    # 1. Directed graphs and transposed
    print("\n1. Directed Graphs and Transposed")
    G1 = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    G1_t = transpose_graph(G1)
    print(f"Original: {G1}")
    print(f"Transposed: {G1_t}")
    
    # 2. Undirected graphs and inverse
    print("\n2. Undirected Graphs and Inverse")
    U1 = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B", "D"], "D": ["C"]}
    U1_i = inverse_graph(U1)
    print(f"Original: {U1}")
    print(f"Inverse: {U1_i}")
    
    # 3. Dense vs sparse
    print("\n3. Dense Graph → Sparse Inverse")
    dense = {"A": ["B", "C", "D"], "B": ["A", "C", "D"], 
             "C": ["A", "B", "D"], "D": ["A", "B", "C"]}
    dense_i = inverse_graph(dense)
    print(f"Dense (K4): {dense}")
    print(f"Inverse: {dense_i} (empty)")
    
    # 4. Dual graphs
    print("\n4. Dual Graphs: Only for planar graphs")
    print("Dual has one vertex per face, one edge per original edge")
    
    # 5. Why only planar?
    print("\n5. Why Dual Only for Planar Graphs?")
    print("Dual requires planar embedding to define faces.")
    print("Non-planar graphs (e.g., K5) have no well-defined faces.")
    
    # Bron-Kerbosch
    print("\nBron-Kerbosch Algorithm:")
    graph = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B", "D"], "D": ["C"]}
    print(f"Graph: {graph}")
    
    R, P, X = set(), set(graph.keys()), set()
    print(f"Initial: R={sorted(R)}, P={sorted(P)}, X={sorted(X)}")
    
    cliques = []
    bron_kerbosch(R, P.copy(), X.copy(), graph, cliques)
    
    unique = []
    seen = set()
    for c in cliques:
        t = tuple(sorted(c))
        if t not in seen:
            seen.add(t)
            unique.append(c)
    
    print("Maximal cliques:")
    for c in unique:
        print(f"  {sorted(c)}")
    
    max_size = max(len(c) for c in unique)
    max_cliques = [c for c in unique if len(c) == max_size]
    print(f"Maximum clique(s) (size {max_size}): {[sorted(c) for c in max_cliques]}")


# ============================================================================
# Problem Set #8: SCC, Euler Tour, Topological Sort
# ============================================================================

def reverse_graph(graph):
    """Compute reversal of directed graph in O(V+E) time."""
    rev = {v: [] for v in graph}
    for u in graph:
        for v in graph[u]:
            rev[v].append(u)
    return rev


def kosaraju_scc(graph):
    """Find strongly connected components using Kosaraju's algorithm."""
    def dfs1(v, visited, stack):
        visited.add(v)
        for u in graph.get(v, []):
            if u not in visited:
                dfs1(u, visited, stack)
        stack.append(v)
    
    def dfs2(v, visited, component, rev_graph):
        visited.add(v)
        component.add(v)
        for u in rev_graph.get(v, []):
            if u not in visited:
                dfs2(u, visited, component, rev_graph)
    
    # First DFS: fill stack
    visited = set()
    stack = []
    for v in graph:
        if v not in visited:
            dfs1(v, visited, stack)
    
    # Reverse graph
    rev_graph = reverse_graph(graph)
    
    # Second DFS: find SCCs
    visited = set()
    sccs = []
    while stack:
        v = stack.pop()
        if v not in visited:
            component = set()
            dfs2(v, visited, component, rev_graph)
            sccs.append(component)
    
    return sccs


def build_scc_graph(graph, sccs):
    """Build strong component graph from SCCs."""
    scc_map = {}
    for i, scc in enumerate(sccs):
        for v in scc:
            scc_map[v] = i
    
    scc_graph = {i: set() for i in range(len(sccs))}
    for u in graph:
        for v in graph[u]:
            u_scc = scc_map[u]
            v_scc = scc_map[v]
            if u_scc != v_scc:
                scc_graph[u_scc].add(v_scc)
    
    return scc_graph, scc_map


def euler_tour(graph):
    """Find Euler tour if it exists (O(E) time)."""
    # Check if Euler tour exists
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    for u in graph:
        for v in graph[u]:
            out_degree[u] += 1
            in_degree[v] += 1
    
    # All vertices must have in_degree == out_degree
    for v in set(list(graph.keys()) + [v for u in graph for v in graph[u]]):
        if in_degree[v] != out_degree[v]:
            return None
    
    # Find Euler tour using Hierholzer's algorithm
    def find_cycle(start, graph_copy):
        cycle = [start]
        current = start
        while graph_copy.get(current):
            next_v = graph_copy[current].pop(0)
            cycle.append(next_v)
            current = next_v
        return cycle
    
    # Make copy of graph
    graph_copy = {u: list(neighbors) for u, neighbors in graph.items()}
    
    # Find initial cycle
    start = next(iter(graph))
    tour = find_cycle(start, graph_copy)
    
    # Merge remaining cycles
    i = 0
    while i < len(tour):
        v = tour[i]
        if graph_copy.get(v):
            cycle = find_cycle(v, graph_copy)
            tour = tour[:i] + cycle + tour[i+1:]
        else:
            i += 1
    
    return tour


def topological_sort(graph, start=None):
    """Topological sort using Kahn's algorithm."""
    in_degree = defaultdict(int)
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
    
    # Initialize with all vertices
    for v in graph:
        if v not in in_degree:
            in_degree[v] = 0
    
    queue = deque([v for v in graph if in_degree[v] == 0])
    result = []
    
    while queue:
        u = queue.popleft()
        result.append(u)
        for v in graph.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    if len(result) != len(graph):
        return None
    
    # If start specified, reorder to start from that node
    if start and start in result:
        idx = result.index(start)
        return result[idx:] + result[:idx]
    
    return result


def problem8():
    """Problem Set #8 solutions."""
    print("\n" + "=" * 70)
    print("Problem Set #8: SCC, Euler Tour, Topological Sort")
    print("=" * 70)
    
    # Problem 1: SCC
    print("\nProblem 1: Strongly Connected Components")
    print("-" * 70)
    
    # Example graph
    G = {"A": ["B"], "B": ["C", "D"], "C": ["A"], "D": ["E"], "E": []}
    print(f"Graph G: {G}")
    
    rev_G = reverse_graph(G)
    print(f"Reversal rev(G): {rev_G}")
    print("Algorithm: O(V+E) - iterate through all vertices and edges once")
    
    sccs = kosaraju_scc(G)
    print(f"\nStrongly Connected Components: {[sorted(scc) for scc in sccs]}")
    
    scc_graph, scc_map = build_scc_graph(G, sccs)
    print(f"SCC Graph: {scc_graph}")
    print("Proof: SCC graph is acyclic (each SCC is a single vertex)")
    
    # Problem 2: Euler Tour
    print("\nProblem 2: Euler Tour")
    print("-" * 70)
    
    # Example: Eulerian graph
    euler_graph = {"A": ["B"], "B": ["C"], "C": ["A"]}
    print(f"Graph: {euler_graph}")
    
    in_deg = {v: 0 for v in euler_graph}
    out_deg = {v: 0 for v in euler_graph}
    for u in euler_graph:
        for v in euler_graph[u]:
            out_deg[u] += 1
            in_deg[v] += 1
    
    print("Condition: in-degree(v) = out-degree(v) for all v")
    for v in euler_graph:
        print(f"  {v}: in={in_deg[v]}, out={out_deg[v]}")
    
    tour = euler_tour(euler_graph)
    print(f"Euler tour: {tour}")
    print("Algorithm: O(E) - Hierholzer's algorithm (merge cycles)")
    
    # Problem 3: Topological Sort
    print("\nProblem 3: Topological Sort")
    print("-" * 70)
    
    courses = {
        "A": ["B", "C"],
        "B": ["C", "D"],
        "C": ["E"],
        "D": ["E", "F"],
        "E": [],
        "F": [],
        "G": ["F", "E"]
    }
    
    print("Course dependencies:")
    for u, deps in courses.items():
        for v in deps:
            print(f"  {u} → {v}")
    
    print("\nStarting from A:")
    topo_A = topological_sort(courses, start="A")
    print(f"  Order: {' → '.join(topo_A)}")
    
    # Start from another node
    print("\nStarting from G:")
    topo_G = topological_sort(courses, start="G")
    print(f"  Order: {' → '.join(topo_G)}")


if __name__ == "__main__":
    problem7()
    problem8()
    print("\n" + "=" * 70)
    print("All problems solved!")
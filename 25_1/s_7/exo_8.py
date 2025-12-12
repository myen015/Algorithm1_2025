import collections

# --- Problem 1: SCC and Reversal / Problem 3: Topological Sort ---

# Directed Graph representing the courses (Problem 3)
# Dependencies: A->B, A->C, B->C, B->D, C->E, D->E, D->F, G->F, G->E
COURSE_GRAPH = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['E'],
    'D': ['E', 'F'],
    'E': [],
    'F': [],
    'G': ['F', 'E']
}

def get_reversed_graph(graph):
    """
    Computes the reversal of a directed graph G. O(V + E) time.
    """
    rev_g = {node: [] for node in graph}
    
    for u in graph:
        for v in graph[u]:
            rev_g[v].append(u)
            
    return rev_g

def get_topological_sort(graph):
    """
    Kahn's algorithm for topological sorting (Problem 3).
    Returns one valid sorting.
    """
    in_degree = {u: 0 for u in graph}
    
    # Calculate in-degrees
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
            
    # Initialize queue with zero-degree nodes
    zero_in_degree = collections.deque(
        sorted([u for u in graph if in_degree[u] == 0])
    )
    
    sorted_order = []
    
    while zero_in_degree:
        u = zero_in_degree.popleft() 
        sorted_order.append(u)
        
        # 'Remove' edges by decrementing degree of neighbors
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                zero_in_degree.append(v)
                
    if len(sorted_order) == len(graph):
        return sorted_order
    else:
        # A cycle exists
        return "Graph has a cycle, no topological order exists."

# --- Problem 2: Euler Tour (Hierholzer's Algorithm) ---

# Example Graph for Euler Tour (in/out-degree is balanced)
# Edges: 0->1, 1->2, 2->0, 2->3, 3->2
EULER_GRAPH = {
    0: [1],
    1: [2],
    2: [0, 3],
    3: [2]      
}

def find_euler_tour(graph):
    """
    Hierholzer's algorithm to find an Euler tour. O(E) time.
    Assumes graph is strongly connected and degrees are balanced.
    """
    
    # Quick check for degree balance (essential condition)
    out_degree = {u: len(graph.get(u, [])) for u in graph}
    in_degree = collections.defaultdict(int)
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
            
    for v in graph:
        if out_degree.get(v, 0) != in_degree.get(v, 0):
            # The condition from Problem 2.1 is violated.
            return f"Degrees unbalanced at {v}. Cannot find an Euler tour."

    if not graph:
        return []
    
    # Working copy of the graph to remove edges
    working_graph = {k: list(v) for k, v in graph.items()}
    
    start = list(graph.keys())[0]
    curr_path = [start]
    tour = []
    
    # Main loop: find cycles and splice them into the tour
    while curr_path:
        u = curr_path[-1]
        
        if working_graph.get(u):
            # If there are unused edges from u, extend the current path
            v = working_graph[u].pop(0) 
            curr_path.append(v)
        else:
            # Current path segment is a cycle, splice it into the main tour
            tour.append(curr_path.pop())
            
    tour.reverse()
    
    return tour

# --- Execution ---

print("--- Problem 1 & 3 Results ---")
print("Original Course Graph:", COURSE_GRAPH)
print("\nReversed Graph (rev(G)):")
print(get_reversed_graph(COURSE_GRAPH))

print("\nTopological Sort (One valid order for Problem 3):")
print(get_topological_sort(COURSE_GRAPH))


print("\n--- Problem 2 Results ---")
print("Euler Graph Edges:", EULER_GRAPH)
print("\nEuler Tour:")
print(find_euler_tour(EULER_GRAPH))
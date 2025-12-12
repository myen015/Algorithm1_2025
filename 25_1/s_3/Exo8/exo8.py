from collections import defaultdict, deque

# Problem 1
def reverse_graph(graph):
    rev = defaultdict(list)
    for u in graph:
        for v in graph[u]:
            rev[v].append(u)
    return rev
# Example graph
vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
edges = [('A','B'), ('A','C'), ('B','C'), ('B','D'), ('C','E'), ('D','E'), ('D','F'), ('G','F'), ('G','E')]

graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)

rev_graph = reverse_graph(graph)
print("Reversed edges:")
for u in sorted(rev_graph):
    for v in rev_graph[u]:
        print(u, "->", v)

# ----------------------------------
# Problem 2: Euler Tour
def has_euler_tour(graph, vertices):
    in_deg = {v: 0 for v in vertices}
    for u in graph:
        for v in graph[u]:
            in_deg[v] += 1
    for v in vertices:
        if len(graph[v]) != in_deg[v]:
            return False
    return True

def find_euler_tour(graph, start):
    # Hierholzer's algorithm-ish
    stack = [start]
    tour = []
    while stack:
        u = stack[-1]
        if graph[u]:
            stack.append(graph[u].pop())
        else:
            tour.append(stack.pop())
    return tour[::-1]

# Simple example graph
euler_vertices = ['A', 'B', 'C']
euler_graph = defaultdict(list)
euler_graph['A'].append('B')
euler_graph['B'].append('C')
euler_graph['C'].append('A')

if has_euler_tour(euler_graph, euler_vertices):
    tour = find_euler_tour(euler_graph, 'A')
    print("\nEuler tour:", ' -> '.join(tour))
else:
    print("\nNo Euler tour")

# ----------------------------------
# Problem 3
def dfs_topo(graph, node, visited, stack):
    # DFS visit
    visited.append(node)
    for neigh in graph[node]:
        if neigh not in visited:
            dfs_topo(graph, neigh, visited, stack)
    stack.append(node)

def topological_sort(graph, vertices, start):
    visited = []
    stack = []
    if start in vertices:
        dfs_topo(graph, start, visited, stack)
    for v in vertices:
        if v not in visited:
            dfs_topo(graph, v, visited, stack)
    return stack[::-1]

# Example graph for topological sort
topo_a = topological_sort(graph, vertices, 'A')
print("\nTopo from A:", ' '.join(topo_a))

topo_g = topological_sort(graph, vertices, 'G')
print("Topo from G:", ' '.join(topo_g))

topo_random = topological_sort(graph, vertices, 'D')  # Random start
print("Topo from D:", ' '.join(topo_random))
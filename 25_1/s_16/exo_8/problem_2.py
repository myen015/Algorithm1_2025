from collections import defaultdict


def euler_tour(graph_adj_list, start_node):

    in_degree = defaultdict(int)
    out_degree = {}

    all_vertices = set(graph_adj_list.keys())

    for u, neighbors in graph_adj_list.items():
        out_degree[u] = len(neighbors)
        all_vertices.add(u)
        for v in neighbors:
            in_degree[v] += 1
            all_vertices.add(v)

    for v in all_vertices:
        if out_degree.get(v, 0) != in_degree.get(v, 0):
            return "Condition failed: in-degree must equal out-degree for all vertices. No Euler Tour exists."

    adj = {v: list(neighbors) for v, neighbors in graph_adj_list.items()}

    stack = []
    tour = []

    stack.append(start_node)

    while stack:
        v = stack[-1]
        if adj.get(v) and len(adj[v]) > 0:
            u = adj[v].pop()
            stack.append(u)
        else:
            tour.append(stack.pop())
    tour.reverse()

    total_edges = sum(len(neighbors) for neighbors in graph_adj_list.values())
    if len(tour) != total_edges + 1:
        return "Failed to construct full tour"

    return tour

g = {
    'A': ['B', 'D'],
    'B': ['C'],
    'C': ['A'],
    'D': ['A'],
}

tour = euler_tour(g, 'A')
print(f"Euler tour: {tour}")
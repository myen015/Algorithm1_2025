from collections import defaultdict, deque

graph = {
    "A": ["B", "C"],
    "B": ["C", "D"],
    "C": ["E"],
    "D": ["E", "F"],
    "E": [],
    "F": [],
    "G": ["F", "E"]
}

def topo_sort(g):
    indeg = defaultdict(int)
    
    for u in g:
        for v in g[u]:
            indeg[v] += 1
        if u not in indeg:
            indeg[u] = 0

    q = deque([v for v in indeg if indeg[v] == 0])
    order = []

    while q:
        u = q.popleft()
        order.append(u)

        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    return order

print("Topological order:", topo_sort(graph))



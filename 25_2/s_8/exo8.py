
from collections import defaultdict, deque

# -------- Graph Reversal --------
def reverse_graph(adj):
    rev = {v: [] for v in adj}
    for u in adj:
        for v in adj[u]:
            rev[v].append(u)
    return rev


# -------- Kosaraju SCC --------
def dfs_order(u, adj, visited, order):
    visited.add(u)
    for v in adj.get(u, []):
        if v not in visited:
            dfs_order(v, adj, visited, order)
    order.append(u)


def dfs_collect(u, adj, visited, comp):
    visited.add(u)
    comp.add(u)
    for v in adj.get(u, []):
        if v not in visited:
            dfs_collect(v, adj, visited, comp)


def kosaraju_scc(adj):
    visited = set()
    order = []

    for u in adj:
        if u not in visited:
            dfs_order(u, adj, visited, order)

    rev = reverse_graph(adj)

    visited.clear()
    comps = []

    for u in reversed(order):
        if u not in visited:
            comp = set()
            dfs_collect(u, rev, visited, comp)
            comps.append(comp)

    return comps


# -------- Condensation Graph --------
def condensation_graph(adj):
    comps = kosaraju_scc(adj)
    comp_id = {}

    for i, c in enumerate(comps):
        for v in c:
            comp_id[v] = i

    c_adj = {i: set() for i in range(len(comps))}

    for u in adj:
        for v in adj[u]:
            if comp_id[u] != comp_id[v]:
                c_adj[comp_id[u]].add(comp_id[v])

    return {i: list(neigh) for i, neigh in c_adj.items()}, comps


# -------- Euler Tour (Hierholzer) --------
def euler_tour(adj):
    indeg = defaultdict(int)
    outdeg = defaultdict(int)

    for u in adj:
        outdeg[u] += len(adj[u])
        for v in adj[u]:
            indeg[v] += 1

    for v in set(list(adj.keys()) + list(indeg.keys())):
        if indeg[v] != outdeg[v]:
            return None

    local = {u: adj[u][:] for u in adj}

    start = next(iter(adj))
    stack = [start]
    path = []

    while stack:
        u = stack[-1]
        if local.get(u):
            v = local[u].pop()
            stack.append(v)
        else:
            path.append(stack.pop())

    return list(reversed(path))


# -------- Kahn’s Topological Sort --------
def kahn_toposort(adj, prefer_first=None):
    nodes = set(adj.keys()) | {v for nbrs in adj.values() for v in nbrs}

    indeg = {u: 0 for u in nodes}
    for u in adj:
        for v in adj[u]:
            indeg[v] += 1

    zero = sorted([u for u in nodes if indeg[u] == 0])
    q = deque(zero)

    if prefer_first and prefer_first in q:
        q.remove(prefer_first)
        q.appendleft(prefer_first)

    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in sorted(adj.get(u, [])):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(order) != len(nodes):
        return None

    return order


# -------- Example (Problem 3) --------
if __name__ == "__main__":
    example = {
        "A": ["B", "C"],
        "B": ["C", "D"],
        "C": ["E"],
        "D": ["E", "F"],
        "E": [],
        "F": [],
        "G": ["F", "E"]
    }

    print("Reverse:", reverse_graph(example))
    print("SCC:", kosaraju_scc(example))
    cg, comps = condensation_graph(example)
    print("Condensation:", cg)
    print("Euler tour (expected None):", euler_tour(example))
    print("Topo (A first):", kahn_toposort(example, "A"))
    print("Topo (G first):", kahn_toposort(example, "G"))

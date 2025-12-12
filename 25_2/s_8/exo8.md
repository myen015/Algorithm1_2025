

## Problem 1 — SCC and Reversal (4/10 pts)

### 1. Algorithm to compute `rev(G)` in `O(V + E)`

To reverse a directed graph, create a new adjacency list and for each edge `u → v`, insert an edge `v → u` in the reversed graph.

Pseudocode:
```
for each vertex u:
    rev[u] = empty list
for each vertex u:
    for each v in G[u]:
        rev[v].append(u)
```
This touches each vertex once and each edge once → `O(V + E)`.

---

### 2. Prove that `scc(G)` is acyclic

Each SCC collapses into a single node.  
If there were a cycle between SCCs, those SCCs would actually be reachable from each other, contradicting maximality.  
Therefore, the condensation graph is always a DAG.

---

### 3. Prove that `scc(rev(G)) = rev(scc(G))`

Reversing edges of `G` does not change which vertices mutually reach each other.  
Every SCC stays the same set of vertices.  
Only the direction of edges between SCCs flips, so the condensation graph is reversed.  
Thus:
```
scc(rev(G)) and rev(scc(G)) have identical components.
```

---

### 4. Characterization of reachability using SCCs

Let `S(v)` be the SCC containing `v`.  
Vertices `u` and `v` satisfy:

```
u reaches v   <=>   S(u) reaches S(v) in the condensation graph
```

This holds because the condensation graph is a DAG and each SCC is maximally strongly connected.

---

## Problem 2 — Euler Tour (2/10 pts)

### 1. Existence condition

A directed graph has an Euler tour **iff**:

```
in-degree(v) == out-degree(v)   for all v
and the graph is strongly connected
```

This is the classical Euler criterion.

---

### 2. `O(E)` algorithm to find an Euler tour

Use **Hierholzer’s algorithm**:

1. Pick any start vertex.  
2. Follow unused outgoing edges until returning to the start.  
3. Whenever you reach a vertex with unused outgoing edges, start a new cycle there.  
4. Merge all cycles into one Euler tour.

The algorithm uses each edge exactly once → `O(E)`.

---

## Problem 3 — Topological Search (4/10 pts)

Given the course graph:

```
A → B
A → C
B → C
B → D
C → E
D → E
D → F
G → F
G → E
```

### Topological Sort starting from A

One valid ordering:
```
A, B, C, D, G, F, E
```

### Another topological order (start from random node)

For example starting from `G`:
```
G, A, B, C, D, F, E
```

Both satisfy all prerequisite constraints.

---

## Code

Full code used for SCC, reversal, Euler tour, and topological sort:

```python
from collections import defaultdict, deque

def reverse_graph(adj):
    rev = {v: [] for v in adj}
    for u in adj:
        for v in adj[u]:
            rev[v].append(u)
    return rev

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
```


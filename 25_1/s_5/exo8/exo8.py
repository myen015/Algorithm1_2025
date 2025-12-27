from collections import deque
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Set


@dataclass
class DirectedGraph:
    V: int = 0
    adj: List[List[int]] = field(default_factory=list)
    indeg: List[int] = field(default_factory=list)
    outdeg: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.init(self.V)

    def init(self, n: int) -> None:
        self.V = n
        self.adj = [[] for _ in range(n)]
        self.indeg = [0] * n
        self.outdeg = [0] * n

    def add_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)
        self.outdeg[u] += 1
        self.indeg[v] += 1


def reverse_graph(g: DirectedGraph) -> DirectedGraph:
    rg = DirectedGraph(g.V)
    for u in range(g.V):
        for v in g.adj[u]:
            rg.add_edge(v, u)
    return rg


# Kosaraju SCC
def dfs1(g: DirectedGraph, u: int, used: List[bool], order: List[int]) -> None:
    used[u] = True
    for v in g.adj[u]:
        if not used[v]:
            dfs1(g, v, used, order)
    order.append(u)


def dfs2(rg: DirectedGraph, u: int, comp_id: int, comp: List[int]) -> None:
    comp[u] = comp_id
    for v in rg.adj[u]:
        if comp[v] == -1:
            dfs2(rg, v, comp_id, comp)


def kosaraju_scc(g: DirectedGraph) -> Tuple[List[int], int]:
    n = g.V
    used = [False] * n
    order: List[int] = []

    for i in range(n):
        if not used[i]:
            dfs1(g, i, used, order)

    rg = reverse_graph(g)

    comp = [-1] * n
    comp_id = 0
    for v in reversed(order):
        if comp[v] == -1:
            dfs2(rg, v, comp_id, comp)
            comp_id += 1

    return comp, comp_id


def build_condensation(g: DirectedGraph, comp: List[int], comp_count: int) -> DirectedGraph:
    dag = DirectedGraph(comp_count)
    used_edges: Set[Tuple[int, int]] = set()

    for u in range(g.V):
        cu = comp[u]
        for v in g.adj[u]:
            cv = comp[v]
            if cu != cv and (cu, cv) not in used_edges:
                used_edges.add((cu, cv))
                dag.add_edge(cu, cv)
    return dag


def is_acyclic(g: DirectedGraph) -> bool:
    n = g.V
    indeg = g.indeg[:]  # copy
    q = deque([i for i in range(n) if indeg[i] == 0])

    cnt = 0
    while q:
        u = q.popleft()
        cnt += 1
        for v in g.adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return cnt == n


def can_reach(g: DirectedGraph, u: int, v: int) -> bool:
    used = [False] * g.V
    q = deque([u])
    used[u] = True

    while q:
        x = q.popleft()
        if x == v:
            return True
        for y in g.adj[x]:
            if not used[y]:
                used[y] = True
                q.append(y)
    return False


def can_reach_scc(dag: DirectedGraph, cu: int, cv: int) -> bool:
    used = [False] * dag.V
    q = deque([cu])
    used[cu] = True

    while q:
        x = q.popleft()
        if x == cv:
            return True
        for y in dag.adj[x]:
            if not used[y]:
                used[y] = True
                q.append(y)
    return False


# Euler tour (directed)
def check_euler_condition(g: DirectedGraph) -> bool:
    return all(g.indeg[v] == g.outdeg[v] for v in range(g.V))


def is_strongly_connected_by_edges(g: DirectedGraph) -> bool:
    n = g.V
    start = -1
    for i in range(n):
        if g.outdeg[i] > 0 or g.indeg[i] > 0:
            start = i
            break
    if start == -1:
        return True  # no edges at all

    # DFS/stack on original graph
    used = [False] * n
    st = [start]
    used[start] = True
    while st:
        u = st.pop()
        for v in g.adj[u]:
            if not used[v]:
                used[v] = True
                st.append(v)

    for i in range(n):
        if (g.outdeg[i] > 0 or g.indeg[i] > 0) and not used[i]:
            return False


    # DFS/stack on reversed graph
    rg = reverse_graph(g)
    used = [False] * n
    st = [start]
    used[start] = True
    while st:
        u = st.pop()
        for v in rg.adj[u]:
            if not used[v]:
                used[v] = True
                st.append(v)

    for i in range(n):
        if (g.outdeg[i] > 0 or g.indeg[i] > 0) and not used[i]:
            return False

    return True


def euler_tour(g: DirectedGraph) -> List[int]:
    if not check_euler_condition(g):
        return []
    if not is_strongly_connected_by_edges(g):
        return []

    n = g.V
    idx = [0] * n

    start = 0
    for i in range(n):
        if g.outdeg[i] > 0:
            start = i
            break

    path: List[int] = []
    st = [start]

    while st:
        u = st[-1]
        if idx[u] < len(g.adj[u]):
            v = g.adj[u][idx[u]]
            idx[u] += 1
            st.append(v)
        else:
            path.append(u)
            st.pop()

    path.reverse()
    return path


def topo_sort(g: DirectedGraph) -> List[int]:
    n = g.V
    indeg = g.indeg[:]  # copy
    q = deque([i for i in range(n) if indeg[i] == 0])

    res: List[int] = []
    while q:
        u = q.popleft()
        res.append(u)
        for v in g.adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(res) != n:
        return []  # cycle
    return res


def read_graph_directed() -> DirectedGraph:
    V, E = map(int, input("Enter V (vertices) and E (edges): ").split())
    g = DirectedGraph(V)

    print("Enter edges as: u v (0-indexed, directed u->v)")
    for _ in range(E):
        u, v = map(int, input().split())
        if u < 0 or u >= V or v < 0 or v >= V:
            print(f"Invalid edge ({u},{v}), skipped.")
            continue
        g.add_edge(u, v)
    return g


def print_adj(g: DirectedGraph, title: str) -> None:
    print(f"\n{title}:")
    for u in range(g.V):
        print(f"{u}: " + " ".join(map(str, g.adj[u])))


def print_scc_result(comp: List[int], comp_count: int) -> None:
    print(f"\nSCC count = {comp_count}")
    for i, cid in enumerate(comp):
        print(f"vertex {i} in SCC {cid}")


def solve() -> None:
    while True:
        print("\n================ MENU ================")
        print("1) Reverse graph rev(G)")
        print("2) SCC (Kosaraju) + Condensation DAG + Acyclic check")
        print("3) Reachability u -> v in G")
        print("4) Reachability SCC(u) -> SCC(v) in condensation")
        print("5) Euler Tour (Hierholzer)")
        print("6) Topological Sort (Kahn)")
        print("0) Exit")

        try:
            op = int(input("Choose option: ").strip())
        except ValueError:
            return

        if op == 0:
            break

        g = read_graph_directed()
        print_adj(g, "Input graph")

        if op == 1:
            rg = reverse_graph(g)
            print_adj(rg, "Reversed graph rev(G)")

        elif op == 2:
            comp, comp_count = kosaraju_scc(g)
            print_scc_result(comp, comp_count)

            dag = build_condensation(g, comp, comp_count)
            print_adj(dag, "Condensation DAG scc(G)")
            print("Is condensation DAG acyclic? " + ("YES" if is_acyclic(dag) else "NO"))

        elif op == 3:
            u, v = map(int, input("Enter u and v: ").split())
            if u < 0 or u >= g.V or v < 0 or v >= g.V:
                print("Invalid vertices.")
                continue
            print("YES, u can reach v" if can_reach(g, u, v) else "NO, u cannot reach v")

        elif op == 4:
            comp, comp_count = kosaraju_scc(g)
            dag = build_condensation(g, comp, comp_count)

            u, v = map(int, input("Enter u and v (in original graph): ").split())
            if u < 0 or u >= g.V or v < 0 or v >= g.V:
                print("Invalid vertices.")
                continue


            cu, cv = comp[u], comp[v]
            print(f"SCC(u) = {cu}, SCC(v) = {cv}")
            print("YES, SCC(u) can reach SCC(v)" if can_reach_scc(dag, cu, cv)
                  else "NO, SCC(u) cannot reach SCC(v)")

        elif op == 5:
            print("\nEuler tour requirements:")
            print("1) indeg[v] == outdeg[v] for all v")
            print("2) strongly connected among vertices with non-zero degree")
            print("Check indeg==outdeg? " + ("YES" if check_euler_condition(g) else "NO"))
            print("Check strong connectivity (by edges)? " + ("YES" if is_strongly_connected_by_edges(g) else "NO"))

            tour = euler_tour(g)
            if not tour:
                print("No Euler tour found.")
            else:
                print("Euler tour (vertex sequence):")
                print(" ".join(map(str, tour)))
                print(f"Edges used = {len(tour) - 1}")

        elif op == 6:
            order = topo_sort(g)
            if not order:
                print("Topological sort is impossible (graph has a cycle).")
            else:
                print("Topological ordering:")
                print(" ".join(map(str, order)))

        else:
            print("Unknown option.")


if __name__ == "__main__":
    solve()

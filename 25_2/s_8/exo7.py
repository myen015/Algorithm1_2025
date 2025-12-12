# Problem Set #7 – Bron–Kerbosch + small graph utilities
# Author: Simba

# Simple adjacency list from the assignment
graph = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B", "D"],
    "D": ["C"]
}

# ----------------------------------------
# Helpers for Problem 1 (graph play)
# ----------------------------------------

def transpose_directed(g):
    """Return the transpose of a directed graph."""
    t = {v: [] for v in g}
    for u in g:
        for v in g[u]:
            t[v].append(u)
    return t


def inverse_undirected(g):
    """Return the inverse of an undirected graph."""
    vertices = list(g.keys())
    inv = {v: [] for v in vertices}

    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            a, b = vertices[i], vertices[j]
            # If not connected originally -> connect in inverse
            if b not in g[a]:
                inv[a].append(b)
                inv[b].append(a)

    return inv


# ----------------------------------------
# Bron–Kerbosch Algorithm (without pivoting)
# ----------------------------------------

def bron_kerbosch(R, P, X, g, cliques):
    """Classic Bron–Kerbosch algorithm (no pivoting)."""
    if not P and not X:
        cliques.append(R.copy())
        return

    for v in list(P):
        nbrs = set(g[v])
        bron_kerbosch(
            R | {v},
            P & nbrs,
            X & nbrs,
            g,
            cliques
        )
        P.remove(v)
        X.add(v)


def find_all_cliques(g):
    """Wrapper to return all maximal cliques."""
    R, P, X = set(), set(g.keys()), set()
    cliques = []
    bron_kerbosch(R, P, X, g, cliques)
    return cliques


# Run example from assignment
if __name__ == "__main__":
    cliques = find_all_cliques(graph)
    print("Maximal cliques:", cliques)

    # Compute maximum clique
    mc = max(cliques, key=len)
    print("Maximum clique:", mc)

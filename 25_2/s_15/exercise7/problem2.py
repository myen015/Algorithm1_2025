##problem2.py — Bron–Kerbosch код
# Problem 2 – Bron–Kerbosch without pivoting

graph = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B", "D"],
    "D": ["C"]
}

def neighbors(v):
    return set(graph[v])

def bron_kerbosch(R, P, X, cliques):
    if not P and not X:
        cliques.append(set(R))
        return
    for v in list(P):
        bron_kerbosch(
            R | {v},
            P & neighbors(v),
            X & neighbors(v),
            cliques
        )
        P.remove(v)
        X.add(v)

if __name__ == "__main__":
    V = set(graph.keys())
    R = set()
    P = set(V)
    X = set()
    cliques = []
    bron_kerbosch(R, P, X, cliques)
    print("Maximal cliques:")
    for c in cliques:
        print(sorted(c))

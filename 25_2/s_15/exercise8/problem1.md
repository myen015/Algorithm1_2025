Problem 1 — SCC and Reversal (Full Explanation)

Let G = (V,E) be a directed graph.

⸻

1. Algorithm to compute graph reversal rev(G) in O(V + E)

A graph reversal means replacing each directed edge (u \to v) with the reverse edge (v \to u).

Algorithm (Adjacency List form):
rev = empty adjacency list

for each vertex u in V:
    rev[u] = empty list

for each u in V:
    for each v in G[u]:
        add edge v → u to rev[v]
Explanation:
You visit every vertex once → O(V).
You visit every edge once → O(E).
Total → O(V + E).

⸻

2. Proof: scc(G) is acyclic

A strongly connected component (SCC) is a group of vertices where each vertex can reach every other.

Between SCCs we build the component graph, where each component is a node.

Why is this graph acyclic?
	•	If there were a cycle between components, then by definition all those components would mutually reach each other → they should be one SCC, not several.
	•	Therefore SCC graph must be a DAG (Directed Acyclic Graph).

⸻

3. Prove that:

scc(rev(G)) = rev(scc(G))

Intuition:
Reversing all edges in G does not change which vertices belong to the same SCC because:
	•	If U → V is reachable in G, then V → U is reachable in rev(G).
	•	So mutual reachability stays the same.

Only directions between SCC components flip.
Therefore the graph of SCCs simply reverses direction:
	•	SCC nodes stay identical
	•	edges between SCCs reverse
→ This is exactly rev(scc(G)).

⸻

4. Show: u can reach v in G  ⇔  S(u) reaches S(v) in the SCC graph

Let S(u) and S(v) be the SCCs that contain vertices u and v.

If u → v path exists in the original graph, then:
	•	every time the path crosses SCC boundaries, it corresponds to an edge in the SCC graph.
	•	so S(u) → S(v) must exist.

Conversely, if S(u) → S(v) in the SCC graph, then by definition there must be a path in G connecting the components, therefore connecting u to v.

Thus the equivalence is proven.

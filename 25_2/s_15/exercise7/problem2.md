# Problem 2 — Bron–Kerbosch Execution

We consider the undirected graph G with vertices V = {A, B, C, D} and edges  
E = {AB, AC, BC, CD}.

The graph can be represented as an adjacency list:

```python
graph = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B", "D"],
    "D": ["C"]
}

We apply the Bron–Kerbosch algorithm without pivoting to find all maximal cliques.

The algorithm uses three sets:
	•	R — current growing clique
	•	P — possible candidates to add
	•	X — vertices already processed (to avoid duplicates)

The recursive procedure:
BronKerbosch(R, P, X):
    if P and X are both empty:
        report R as a maximal clique
    for each vertex v in a copy of P:
        BronKerbosch(R ∪ {v}, P ∩ N(v), X ∩ N(v))
        P = P \ {v}
        X = X ∪ {v}
Here N(v) is the set of neighbors of v.

1. Initial call

Vertex set: {A, B, C, D}.

Neighbors:
	•	N(A) = {B, C}
	•	N(B) = {A, C}
	•	N(C) = {A, B, D}
	•	N(D) = {C}

The initial call is:
R = ∅
P = {A, B, C, D}
X = ∅

2. Trace of the first recursive branch leading to a maximal clique

We follow the branch that produces clique {A, B, C}.

Call 0
R = ∅
P = {A, B, C, D}
X = ∅
Take v = A.

Next parameters:
	•	R’ = {A}
	•	P’ = P ∩ N(A) = {B, C}
	•	X’ = X ∩ N(A) = ∅

Call 1
R = {A}
P = {B, C}
X = ∅
Take v = B.
	•	R’’ = {A, B}
	•	P’’ = P ∩ N(B) = {C}
	•	X’’ = X ∩ N(B) = ∅

Call 2
R = {A, B}
P = {C}
X = ∅
Take v = C.
	•	R’’’ = {A, B, C}
	•	P’’’ = P ∩ N(C) = ∅
	•	X’’’ = X ∩ N(C) = ∅

Call 3
R = {A, B, C}
P = ∅
X = ∅
Since both P and X are empty, {A, B, C} is reported as a maximal clique.

Then the recursion unwinds and other branches are explored.

⸻

3. All maximal cliques of G

We now list all cliques and identify the maximal ones.

Edges: AB, AC, BC, CD.

Cliques:
	•	{A, B}
	•	{A, C}
	•	{B, C}
	•	{C, D}
	•	{A, B, C}

A maximal clique is a clique that is not a subset of a larger clique.
	•	{A, B}, {A, C}, {B, C} are all contained in {A, B, C},
so they are not maximal.
	•	{A, B, C} is maximal (no vertex can be added while keeping a clique).
	•	{C, D} is also maximal: D is only connected to C, so we cannot add A or B.

Therefore, the set of maximal cliques is:

{A, B, C} and {C, D}

The Bron–Kerbosch algorithm (without pivoting) correctly outputs exactly these two maximal cliques.


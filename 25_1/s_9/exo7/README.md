Exo 7    
Yeltay Meirambek    
Group: 25_1   
ID: 9 

### 1. Directed graphs and their transposed graphs 

### 2.2. Undirected graphs and their inverse (complement) graphs

Inverse graph (also called complement graph):  

*Two vertices are connected in the inverse graph if and only if they are not connected in the original graph.*

### 3. What happens if the original graph is dense?

* A dense graph has almost all possible edges.

* If the original graph is dense

* Then its inverse (complement) graph is sparse

* If the original graph is complete, its inverse has no edges at all

### 4. Undirected graphs and their dual graphs

The dual graph is constructed as follows:
- place one vertex in each face of the planar graph (including the outer face);
- connect two dual vertices if the corresponding faces share a common edge.

Each edge of the original graph corresponds to exactly one edge in the dual graph.

Non-planar graphs do not have a well-defined dual graph because faces cannot be uniquely identified.

### 5. Why is the dual only well-defined for planar graphs?

*The dual graph is constructed by:*

* Placing a vertex in each face

* Connecting vertices if faces share an edge

*This requires:*

* A clear notion of faces

* Faces only exist if the graph is planar

Non-planar graph example: K5
	​
Complete graph with 5 vertices:


*Every vertex connected to every other vertex*

Facts:

* K5 is non-planar

* It cannot be drawn without edge crossings

* Crossings prevent a consistent definition of faces

* No well-defined faces
* No unique dual graph

**Therefore, non-planar graphs do not have a dual graph.**

Problem2:

Bron–Kerbosch Execution

Given an undirected graph 𝐺=(𝑉,𝐸)  

Vertices:

𝑉
=
{
𝐴
,
𝐵
,
𝐶
,
𝐷
}


Edges:

𝐸
=
{
𝐴
𝐵
,
𝐴
𝐶
,
𝐵
𝐶
,
𝐶
𝐷
}

```
graph = {
  "A": ["B", "C"],
  "B": ["A", "C"],
  "C": ["A", "B", "D"],
  "D": ["C"]
}
```

### 1. Initial call of the Bron–Kerbosch algorithm

At the start:


* R=∅ (current clique)


* P={A,B,C,D} (possible vertices)


* X=∅ (already processed vertices)

```
BronKerbosch(R = ∅, P = {A,B,C,D},X = ∅)   
```
### 2. First recursive calls leading to a maximal clique

*Step 1: choose vertex A from P*
```
R = {A}
P = {B, C}      (neighbors of A)
X = ∅
```

*Step 2: choose vertex B from P*
```
R = {A, B}
P = {C}   (neighbors common to A and B)
X = ∅
```

*Step 3: choose vertex C from P*
```
R = {A, B, C}
P = ∅
X = ∅
```

**Since P = ∅ and X = ∅, a maximal clique is reported:**
```
{A, B, C}
```

### 3. All maximal cliques of G
From the full execution of the algorithm, the maximal cliques are:

* {A, B, C}

* {C, D}

### Maximum clique(s)

*Clique sizes:*

* {A, B, C} → size 3

* {C, D} → size 2

```
{A, B, C}
```


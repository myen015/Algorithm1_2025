

## Problem 1

Let \( G = (V, E) \) be an undirected graph with \( |V| = V \).


1. A connected graph with no cycles  
2. A connected component of a forest  
3. A connected graph with at most \( V-1 \) edges  
4. A graph where every edge is a bridge  
5. An acyclic graph with at least \( V-1 \) edges  
6. A maximally acyclic graph  
7. A graph with a unique path between every pair of vertices  

---

### Proof of Equivalence

#### (1 ⇒ 2)
A forest is defined as a graph that contains no cycles.  
Since the graph in (1) is acyclic and connected, it must appear as a single connected component of a forest.

---

#### (2 ⇒ 7)
In a forest, cycles are not allowed.  
If two different paths existed between the same vertices inside one component, a cycle would be formed.  
Therefore, there must be exactly one path between every pair of vertices.

---

#### (7 ⇒ 1)
A unique path between all vertex pairs guarantees connectivity.  
It also prevents cycles, since a cycle would create multiple paths between the same vertices.  
Thus, the graph is connected and acyclic.

---

#### (1 ⇒ 3)
Construct the graph step by step.
To keep it connected without forming cycles, each newly added vertex must connect with exactly one edge.
Hence, the total number of edges is at most \( V-1 \).

---

#### (3 ⇒ 4)
If a connected graph has at most \( V-1 \) edges, removing any edge will drop the count below what is needed for connectivity.
Therefore, every edge is essential, and the graph is minimally connected.

---

#### (4 ⇒ 6)
If every edge is a bridge, no cycles can exist.
Adding any new edge introduces an alternative path, which immediately creates a cycle.
Thus, the graph is maximally acyclic.

---

#### (6 ⇒ 5)
A maximally acyclic graph already contains the maximum number of edges possible without forming a cycle.
This requires at least \( V-1 \) edges while remaining acyclic.

---

#### (5 ⇒ 1)
An acyclic graph cannot exceed \( V-1 \) edges.
If it has at least \( V-1 \) edges, it must be connected.
Therefore, the graph is a tree.

---

### Conclusion
All seven definitions describe the same structure: a **tree**.

---

## Problem 2 — Graph Reconstruction from CSC Format

Vertex indexing:
A = 0, B = 1, C = 2, D = 3, E = 4
---

## Graph 1 (Undirected)

### Adjacency Matrix

|   | A | B | C | D | E |
|---|---|---|---|---|---|
| A | 0 | 1 | 1 | 0 | 0 |
| B | 1 | 0 | 1 | 1 | 0 |
| C | 1 | 1 | 0 | 1 | 0 |
| D | 0 | 1 | 1 | 0 | 1 |
| E | 0 | 0 | 0 | 1 | 0 |

---

### Adjacency List
A: B, C
B: A, C, D
C: A, B, D
D: B, C, E
E: D
---

### Edge Set
A–B, A–C, B–C, B–D, C–D, D–E
---


## Graph 2 (Directed)

### Adjacency Matrix

|   | A | B | C | D | E |
|---|---|---|---|---|---|
| A | 0 | 0 | 0 | 0 | 0 |
| B | 1 | 0 | 0 | 1 | 0 |
| C | 1 | 1 | 0 | 0 | 0 |
| D | 0 | 0 | 1 | 0 | 0 |
| E | 0 | 1 | 0 | 1 | 0 |

---

### Outgoing Edges

B → A
B → D
C → A
C → B
D → C
E → B
E → D
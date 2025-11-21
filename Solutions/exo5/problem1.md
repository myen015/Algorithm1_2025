# Problem 1: Equivalence of Tree Definitions

## Definitions

1. A tree is a connected acyclic graph.
2. A tree is one component of a forest. (A forest is an acyclic graph.)
3. A tree is a connected graph with at most V − 1 edges.
4. A tree is a minimally connected graph; removing any edge disconnects the graph.
5. A tree is an acyclic graph with at least V − 1 edges.
6. A tree is a maximally acyclic graph; adding an edge between any two vertices creates a cycle.
7. A tree is a graph that contains a unique path between each pair of vertices.

---

## Proof of Equivalence

To prove all definitions are equivalent, we will show that each definition implies all others. We establish this by proving key implications that form a logical cycle.

---

### Theorem 1: Definitions 1 and 7 are equivalent

**Part A: Definition 1 implies Definition 7**

Assume G is a connected acyclic graph (Definition 1). We prove G has a unique path between each pair of vertices.

_Proof:_

- Let u and v be any two vertices in G.
- Since G is connected, there exists at least one path from u to v.
- Suppose there are two distinct paths P₁ and P₂ from u to v.
- Let x be the first vertex where P₁ and P₂ diverge.
- Let y be the first vertex after x where P₁ and P₂ reconverge.
- The portion of P₁ from x to y, combined with the portion of P₂ from y back to x, forms a cycle.
- This contradicts the assumption that G is acyclic.
- Therefore, there is exactly one path between u and v.

**Part B: Definition 7 implies Definition 1**

Assume G has a unique path between each pair of vertices (Definition 7). We prove G is connected and acyclic.

_Proof of connectivity:_

- By assumption, there exists a path between every pair of vertices.
- Therefore, G is connected by definition.

_Proof of acyclicity:_

- Suppose G contains a cycle C involving vertices v₁, v₂, ..., vₖ, v₁.
- Consider vertices v₁ and v₂ in this cycle.
- Path 1: The direct edge (v₁, v₂).
- Path 2: The path v₁ → vₖ → vₖ₋₁ → ... → v₂ (going the other way around the cycle).
- These are two distinct paths from v₁ to v₂.
- This contradicts the uniqueness of paths.
- Therefore, G must be acyclic.

---

### Theorem 2: Definitions 1 and 4 are equivalent

**Part A: Definition 1 implies Definition 4**

Assume G is a connected acyclic graph. We prove removing any edge disconnects G.

_Proof:_

- Let e = (u, v) be any edge in G.
- Since G is connected and acyclic, by Theorem 1, there is exactly one path from u to v.
- This unique path must be the edge e itself (a path of length 1).
- If any other path existed, we would have two distinct paths from u to v, which contradicts Theorem 1.
- Removing edge e eliminates the only path from u to v.
- Therefore, G becomes disconnected.

**Part B: Definition 4 implies Definition 1**

Assume G is minimally connected (removing any edge disconnects G). We prove G is connected and acyclic.

_Proof of connectivity:_

- This is given directly by the definition: G is connected.

_Proof of acyclicity:_

- Suppose G contains a cycle C.
- Let e be any edge in cycle C.
- Remove edge e from G, creating graph G'.
- For any two vertices u and v that were connected by a path using edge e, we can find an alternative path:
  - If the original path used e going from u to v, we can go around the cycle C in the opposite direction.
- Therefore, G' remains connected.
- This contradicts the minimal connectivity property (that removing any edge disconnects G).
- Therefore, G must be acyclic.

---

### Theorem 3: Definitions 1 and 3 are equivalent

**Part A: Definition 1 implies Definition 3**

Assume G is a connected acyclic graph with V vertices. We prove G has exactly V − 1 edges (hence at most V − 1 edges).

_Proof by induction on V:_

Base case (V = 1): A single vertex has 0 edges. 0 = 1 − 1. ✓

Inductive hypothesis: Assume true for all connected acyclic graphs with k vertices (k < V).

Inductive step: Let G be a connected acyclic graph with V vertices.

- Since V ≥ 2 and G is connected, G has at least one edge.
- Pick any edge e = (u, v).
- By Theorem 2, removing e disconnects G into exactly two components (since G is acyclic).
- Let these components be G₁ with V₁ vertices and G₂ with V₂ vertices.
- We have V₁ + V₂ = V.
- Both G₁ and G₂ are connected acyclic graphs.
- By inductive hypothesis: G₁ has V₁ − 1 edges and G₂ has V₂ − 1 edges.
- Total edges in G = (V₁ − 1) + (V₂ − 1) + 1 = V − 1. ✓

**Part B: Definition 3 implies Definition 1**

Assume G is connected with at most V − 1 edges. We prove G is acyclic.

_Proof:_

- First, note that any connected graph on V vertices must have at least V − 1 edges.
  - This can be shown by considering that starting from one vertex, we need at least V − 1 edges to reach all other V − 1 vertices without creating redundant connections.
- Since G has at most V − 1 edges and must have at least V − 1 edges, G has exactly V − 1 edges.
- Suppose G contains a cycle C.
- Pick any edge e in cycle C and remove it, creating G'.
- G' is still connected (we can route around the cycle using the remaining edges of C).
- G' has V vertices and V − 2 edges, but is connected.
- This contradicts the fact that a connected graph needs at least V − 1 edges.
- Therefore, G must be acyclic.

---

### Theorem 4: Definitions 1 and 5 are equivalent

**Part A: Definition 1 implies Definition 5**

Assume G is a connected acyclic graph with V vertices. We prove G has at least V − 1 edges.

_Proof:_

- By Theorem 3, we proved that a connected acyclic graph has exactly V − 1 edges.
- Therefore, G has at least V − 1 edges. ✓
- G is acyclic by assumption. ✓

**Part B: Definition 5 implies Definition 1**

Assume G is an acyclic graph with at least V − 1 edges. We prove G is connected.

_Proof:_

- An acyclic graph on V vertices can have at most V − 1 edges.
  - This can be proven by induction: Each new vertex can connect to the existing structure with at most one edge without creating a cycle.
- Since G is acyclic with at least V − 1 edges, G must have exactly V − 1 edges.
- Suppose G is not connected. Let it have k ≥ 2 connected components with V₁, V₂, ..., Vₖ vertices.
- Each component is acyclic (subgraph of an acyclic graph).
- By the result in Theorem 3, component i has at most Vᵢ − 1 edges.
- Total edges ≤ (V₁ − 1) + (V₂ − 1) + ... + (Vₖ − 1) = V − k ≤ V − 2 (since k ≥ 2).
- This contradicts G having V − 1 edges.
- Therefore, G must be connected.

---

### Theorem 5: Definitions 1 and 6 are equivalent

**Part A: Definition 1 implies Definition 6**

Assume G is a connected acyclic graph. We prove adding any edge creates a cycle.

_Proof:_

- Let u and v be any two non-adjacent vertices in G.
- Since G is connected, there exists a path P from u to v.
- If we add edge (u, v), we create a cycle: the path P from u to v, plus the new edge (v, u) back.
- Therefore, G is maximally acyclic.

**Part B: Definition 6 implies Definition 1**

Assume G is maximally acyclic (adding any edge creates a cycle). We prove G is connected.

_Proof:_

- G is acyclic by definition.
- Suppose G is not connected. Then there exist vertices u and v in different connected components.
- Since they are in different components, there is no path from u to v.
- By the maximally acyclic property, adding edge (u, v) should create a cycle.
- A cycle requires a closed path: u → ... → v → u.
- But since no path exists from u to v in the original graph, adding one edge (u, v) cannot create a cycle.
- This is a contradiction.
- Therefore, G must be connected.

---

### Theorem 6: Definitions 1 and 2 are equivalent

**Part A: Definition 1 implies Definition 2**

Assume G is a connected acyclic graph. We prove G is one component of a forest.

_Proof:_

- An acyclic graph is called a forest by definition.
- G itself is an acyclic graph (a forest).
- G is connected, so it has exactly one connected component.
- Therefore, G is one component of a forest (specifically, a forest consisting of a single tree).

**Part B: Definition 2 implies Definition 1**

Assume G is one connected component of a forest. We prove G is a connected acyclic graph.

_Proof:_

- By definition, G is a connected component, so G is connected. ✓
- A forest is an acyclic graph by definition.
- G is a subgraph of this acyclic forest.
- Any subgraph of an acyclic graph is itself acyclic.
- Therefore, G is acyclic. ✓

---

## Conclusion

We have proven that Definition 1 is equivalent to each of Definitions 2, 3, 4, 5, 6, and 7. By transitivity of equivalence, all seven definitions are equivalent to each other.

Therefore, all seven definitions describe the same mathematical object: a tree.

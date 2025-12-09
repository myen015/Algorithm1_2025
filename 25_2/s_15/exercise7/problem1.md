# Problem 1 — Graph Play

In this problem we play with basic graph constructions: directed vs undirected graphs, transposed graphs, inverse (complement) graphs, and dual graphs for planar graphs.

We denote the vertex set by V = {A, B, C, D, E} when needed.

---

## 1. Examples of directed graphs and their transposed graphs

**Example 1 (simple directed path):**

Directed graph G₁:

- Vertices: A, B, C
- Edges: A → B, B → C

Adjacency list:
- A: [B]
- B: [C]
- C: []

The **transpose** G₁ᵀ is obtained by reversing all edges:

- Edges: B → A, C → B

Adjacency list:
- A: []
- B: [A]
- C: [B]

---

**Example 2 (directed triangle):**

Directed graph G₂:

- Vertices: A, B, C
- Edges: A → B, B → C, C → A

Transpose G₂ᵀ:

- Edges: B → A, C → B, A → C

This shows that the transpose preserves the structure of strongly connected components but reverses the direction of every edge.

---

## 2. Examples of undirected graphs and their inverse (complement) graphs

For an undirected graph on vertex set V, the **inverse (complement)** Ĝ has the same vertices, and an edge {u, v} in Ĝ exists if and only if {u, v} is not an edge in G (ignoring self-loops).

**Example 1:**

G:

- V = {A, B, C}
- E = {{A, B}}

Adjacency:
- A: {B}
- B: {A}
- C: ∅

Complement Ĝ:

- All possible edges on 3 vertices: {A, B}, {A, C}, {B, C}
- Remove {A, B} because it is in G
- So Ĝ has edges: {A, C}, {B, C}

Adjacency of Ĝ:
- A: {C}
- B: {C}
- C: {A, B}

---

**Example 2:**

G is an empty graph on V = {A, B, C} (no edges).

Then Ĝ is the complete graph K₃ with all three edges {A, B}, {A, C}, {B, C}.

---

## 3. What happens if the original is dense for the inverse?

If the original undirected graph G is **dense** (close to complete), then its complement Ĝ is **sparse** (few edges), and vice versa.

- If G is the **complete graph** Kₙ, then Ĝ has **no edges** (empty graph).
- If G has very few edges, then Ĝ is almost complete.

Thus, density is inverted by taking the complement.

---

## 4. Simple examples of undirected graphs and their dual graphs

The **dual graph** is defined for a planar embedding:  
each **face** (region) becomes a vertex of the dual, and two dual vertices are connected if their corresponding faces share an edge.

**Example 1: Triangle**

Take a triangle T:

- Vertices: A, B, C
- Edges: AB, BC, CA

It has:
- 1 bounded face (inside the triangle),
- 1 unbounded outer face.

The dual T* therefore has two vertices (inner and outer face) and a triple edge between them (each primal edge separates inner and outer face). In simplified form, we can say the dual is a multigraph with two vertices connected by three edges.

---

**Example 2: Square with one diagonal**

Graph G:

- Vertices: A, B, C, D
- Edges: AB, BC, CD, DA (a square) and AC (a diagonal)

Faces:
- Triangle ABC,
- Triangle ACD,
- Outer face.

Dual G*:

- One vertex for each face: f₁ (ABC), f₂ (ACD), fₒ (outside).
- Edges in the dual correspond to primal edges that separate faces.  
  For example, the diagonal AC separates faces f₁ and f₂, so there is an edge between f₁ and f₂ in G*.

This demonstrates how dual graphs encode adjacency of faces instead of adjacency of vertices.

---

## 5. Why is the dual only well-defined for planar graphs?

The usual notion of a dual graph relies on a **planar embedding**:

1. We need to draw the graph in the plane **without edge crossings**.
2. Faces (regions) must be well-defined.
3. The dual graph has one vertex per face, and edges of the dual correspond to shared boundaries between faces.

For **non-planar graphs**, such as:

- K₅ (complete graph on 5 vertices),
- K₃,₃ (complete bipartite graph with partitions of size 3),

there is **no way** to draw the graph in the plane without crossings.  
Since faces are not well defined in a non-planar embedding with crossings, the standard construction of a dual graph does not work.

**Example of a non-planar graph without a well-defined dual:**

- K₃,₃ with bipartition {A, B, C} and {D, E, F}.
- It is impossible to embed K₃,₃ in the plane without edge crossings.
- Therefore we cannot consistently define planar faces and hence cannot define a planar dual.

This explains why the dual is only well-defined for planar graphs.

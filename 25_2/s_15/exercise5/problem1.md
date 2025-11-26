Problem 1 — Equivalence of Tree Definitions
In graph theory, a tree is one of the most fundamental structures, and it has many different (but equivalent) definitions.
In this problem, we prove that all seven definitions given in the assignment describe the same mathematical object.
The goal is to show that each definition implies all others, meaning that they are logically equivalent.

To keep the proof clear, we take Definition (1) as the “canonical” form:

A tree is a connected acyclic graph.

Then, for each definition (2)–(7), we show why it is equivalent to (1).
This approach is standard in graph theory: once you establish equivalence to a single definition, all the definitions become equivalent to each other.
1 ⇔ 2 — Tree as a Component of a Forest

Definition 2:

A tree is one component of a forest (a forest is an acyclic graph).

(1 ⇒ 2)

If a graph is connected and acyclic, then by definition it is a component of a forest.
A forest is simply any acyclic graph, and a tree is the connected piece inside it.
Thus every tree is a component of some forest.

(2 ⇒ 1)

If a graph is a connected component of a forest, then: the forest has no cycles, each component of a forest is connected.
Therefore, this component is both connected and acyclic, which is exactly Definition (1).

1 ⇔ 3 — Tree Has at Most V - 1 Edges

Definition 3:

A tree is a connected graph with at most V - 1 edges.

(1 ⇒ 3)

A connected acyclic graph with V vertices always has exactly V - 1 edges.
This is a classical theorem in graph theory.
Therefore, a tree automatically satisfies “at most V - 1” (because it has exactly V - 1).

(3 ⇒ 1)

If a graph is connected and has at most V - 1 edges, it cannot have a cycle, because every cycle would require an extra edge.
Thus the graph must be acyclic and connected → tree.

1 ⇔ 4 — Tree as a Minimally Connected Graph

Definition 4:

A tree is a minimally connected graph; removing any edge disconnects it.

(1 ⇒ 4)

In a connected acyclic graph, there is a unique path between any two vertices.
If you remove one edge from that path, the vertices become disconnected.
Therefore, a tree is minimally connected.

(4 ⇒ 1)

If removing any edge disconnects the graph, then it cannot contain a cycle.
In a cycle, removing one edge does not disconnect the graph.
Hence the graph must be acyclic and connected → tree.

1 ⇔ 5 — Tree as Acyclic Graph With ≥ V - 1 Edges

Definition 5:

A tree is an acyclic graph with at least V - 1 edges.

(1 ⇒ 5)

A tree has exactly V - 1 edges.
Thus it satisfies “acyclic” and “at least V - 1” automatically.

(5 ⇒ 1)

An acyclic graph with at least V - 1 edges must be connected; otherwise it would need fewer edges.
Therefore such a graph must be connected and acyclic → tree.

1 ⇔ 6 — Tree as Maximally Acyclic Graph

Definition 6:

A tree is a maximally acyclic graph; adding any edge creates a cycle.

(1 ⇒ 6)

In a tree, every pair of vertices already has a unique path between them.
Adding any new edge would immediately form a cycle (because it introduces a second path).
Therefore, a tree is maximally acyclic.

(6 ⇒ 1)

If adding any new edge always forms a cycle, the graph must already be connected; otherwise adding an edge between components would not form a cycle.
Thus the graph is acyclic and connected → tree.

1 ⇔ 7 — Unique Path Between Every Pair of Vertices

Definition 7:

A tree is a graph that contains a unique path between each pair of vertices.

(1 ⇒ 7)

In a connected graph, there must be at least one path between any two vertices.
If the graph had two or more different paths, that would create a cycle.
Since a tree is acyclic, the path must be unique.

(7 ⇒ 1)

If there is a unique path between all vertices, the graph must be: connected (paths exist), acyclic (if a cycle existed, there would be two paths).
Thus the graph is connected and acyclic → tree.

Final Conclusion

All seven definitions describe the exact same structure — the mathematical object we call a tree.
Each definition emphasizes a different structural property: minimal connectivity, maximal acyclicity, unique paths, edge count, relation to forests.

Together, they show how rich and elegant the concept of a tree is in graph theory.


Problem 1 — Equivalence of tree definitions

We are given several different definitions of a tree and need to show that they are all equivalent.
Instead of proving every definition with every other one, it is enough to show a chain of implications that forms a cycle.
This proves that all definitions describe the same type of graph.

First, assume that a graph is connected and has no cycles.
Then between any two vertices there must exist at least one path.
If there were two different paths between the same vertices, they would form a cycle.
This contradicts the assumption.
So the path between any two vertices is unique.

Now assume that between every pair of vertices there is a unique path.
If we remove any edge, this unique path is destroyed, and the graph becomes disconnected.
Therefore, the graph is minimally connected.

If a graph is minimally connected, it cannot have more than
V-1 edges.
Otherwise, we could remove an edge and the graph would still stay connected, which contradicts minimality.

Next, consider a connected graph with at most
V-1 edges.
Such a graph cannot contain a cycle, because removing one edge from a cycle would keep the graph connected.
Hence, the graph must be acyclic.

If a graph is acyclic and has at least
V-1 edges, then it is maximally acyclic.
Adding any new edge will create a cycle, since all vertices are already connected by paths.

Finally, assume that a graph is maximally acyclic.
If it were not connected, we could add an edge between two components without creating a cycle.
This contradicts maximal acyclicity.
So the graph must be connected and acyclic.

Since we can go from the first definition back to it again through logical implications, all given definitions of a tree are equivalent.

Problem 2 - Sparse representation of graphs (CSC format)

In this problem, graphs are given using the Compressed Sparse Column (CSC) representation.
In CSC, for each column
𝑗
j, the array col_pointers shows where the column starts and ends in the array row_indices.
Each value in row_indices represents a row index that has a non-zero entry in this column.

Graph 1 (undirected graph)

Using the CSC arrays, we reconstruct the adjacency matrix by reading the rows listed for each column.
Because the matrix is symmetric, the graph is undirected.

After reconstructing the matrix, we observe that:

vertex A is connected to B and C,

vertex B is connected to A, C, and D,

vertex C is connected to A, B, and D,

vertex D is connected to B, C, and E,

vertex E is connected only to D.

From this adjacency information, we can describe the structure of the graph.
It consists of a connected undirected graph where vertex E is a leaf connected to D.

Graph 2 (directed graph)

Again, we reconstruct the adjacency matrix by reading the CSC representation column by column.
In this case, the matrix is not symmetric, so the graph is directed.

From the reconstructed matrix, we see that:

there is a directed path from A to B, from B to C, from C to D, and from D to E,

there is also an edge from D back to A.

This means the graph contains exactly one directed cycle.
The cycle is:

A→B→C→D→A

No other cycles exist, because vertex E has no outgoing edges.

Conclusion

In Problem 1, we showed that all common definitions of a tree are logically equivalent by proving a chain of implications.
In Problem 2, we explained how to interpret the CSC representation, reconstructed adjacency information, and identified the unique cycle in the directed graph.

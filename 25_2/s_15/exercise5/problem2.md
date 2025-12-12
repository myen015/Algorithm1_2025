Problem 2 — Reconstruction of Graphs from CSC Format

In this problem, we are given two graphs represented in CSC (Compressed Sparse Column) format.
Our task is to:
	1.	reconstruct the adjacency matrix of each graph,
	2.	draw a clear diagram of each graph,
	3.	identify the unique cycle in the directed graph.

To solve this, we first recall what CSC format means.

1. Understanding CSC Representation

CSC represents a sparse matrix column by column using three arrays:

col_pointers[j] — starting index of column j in row_indices

row_indices[k] — row index for the element

values[k] — value at position (row, col)

Thus, all non-zero entries of column j are located in:

k = col_pointers[j] … col_pointers[j+1] − 1

row = row_indices[k]

For a graph, this means:

If row_indices[k] = i, then there is an edge
(i → j) in the adjacency matrix.

For an undirected graph, the matrix is symmetric.

2. Graph 1 — Undirected Graph

Given CSC data

col_pointers = [0, 2, 5, 8, 11, 12]

row_indices  = [1, 2, 0, 2, 3, 0, 1, 3, 1, 2, 4, 3]

values       = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

Vertices correspond to:

A → 0

B → 1

C → 2

D → 3

E → 4

2.1 Reconstructed Adjacency Matrix

We read each column:

Column A (0): rows = [1, 2] → edges: A–B, A–C

Column B (1): rows = [0, 2, 3] → edges: B–A, B–C, B–D

Column C (2): rows = [0, 1, 3] → edges: C–A, C–B, C–D

Column D (3): rows = [1, 2, 4] → edges: D–B, D–C, D–E

Column E (4): rows = [3] → edge: E–D

Removing duplicates gives undirected edges:

AB, AC, BC, BD, CD, DE

Adjacency Matrix


       { 0  1  1  0  0  

         1  0  1  1  0

  A=     1  1  0  1  0 

         0  1  1  0  1 

         0  0  0  1  0 }


2.2 Graph Diagram (Undirected)
   
      B ------- D ------- E
   
     / \       /

    A---C----- 

A triangle A–B–C, connected to D, which connects to E.

3. Graph 2 — Directed Graph
Given CSC data

col_pointers = [0, 0, 2, 4, 5, 7]

row_indices  = [0, 3, 0, 1, 2, 1, 3]

values       = [1, 1, 1, 1, 1, 1, 1]

3.1 Reconstructed Adjacency Matrix

Read each column:

Column A (0): no rows → no incoming edges

Column B (1): rows = [0, 3] → A→B, D→B

Column C (2): rows = [0, 1] → A→C, B→C

Column D (3): rows = [2] → C→D

Column E (4): rows = [1, 3] → B→E, D→E

Thus edges are:

A → B

A → C

B → C

B → E

C → D

D → B

D → E

Adjacency Matrix


     { 0  1  1  0  0 

       0  0  1  0  1 

  B=   0  0  0  1  0 

       0  1  0  0  1 

       0  0  0  0  0 }


3.2 Graph Diagram (Directed)

    A → B → C → D

    ↑         ↓

    │         B

    │ 

    A → C → D → E
 
          ↑

          B

A simpler clear diagram:

        A → B → C → D

          ↑    ↓

          └────┘

     B → E      D → E

4. Unique Cycle in Directed Graph

We look for directed cycles.

From edges:

B →C  	

C → D

D → B

This forms the cycle:

B → C → D → B

No other cycles exist because: A has only outgoing edges, E has only incoming edges,all other paths lead into the B–C–D loop.

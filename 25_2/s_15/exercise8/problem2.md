1. Euler tour exists iff in-degree(v) = out-degree(v)

In a strongly connected directed graph:
	•	Every time we enter a vertex, we must leave it.
	•	Therefore counts must match:

\forall v:\; indeg(v) = outdeg(v)

If any vertex has mismatch, we cannot traverse all edges exactly once.

⸻

2. O(E)-time algorithm to find Euler tour

This is Hierholzer’s Algorithm.

Steps:
	1.	Pick any vertex v
	2.	Follow unused edges until you return to v, forming a cycle
	3.	If that cycle contains vertices with unused outgoing edges → start a new cycle there
	4.	Merge the cycles

Every edge is used exactly once, so time is:

O(E)


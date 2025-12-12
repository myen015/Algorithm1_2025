Problem 1 — Classification (P, NP, NP-Complete, NP-Hard)

We classify each line according to the complexity class.

⸻

1. find max, linear search, shortest path in unweighted graph, matrix multiplication
 Class: P
— All these problems have polynomial-time deterministic algorithms.
— Linear search: O(n)
— BFS shortest path: O(V+E)
— Matrix multiplication: polynomial (O(n³) or better)

⸻

2. sorting, Dijkstra (non-negative weights), BFS, DFS, merge sort, quicksort
 Class: P
— Sorting: O(n log n)
— Dijkstra: O(E log V)
— BFS/DFS: O(V+E)
All solvable efficiently.

⸻

3. sudoku
 Class: NP-complete
— Verifying a solved sudoku is easy (polynomial).
— Finding a solution is NP-complete.

⸻

4. 3-coloring, scheduling with conflicts
 Class: NP-complete
— 3-coloring graph: classic NP-complete problem.
— Scheduling with conflicts reduces to graph coloring.

⸻

5. Traveling Salesperson Problem, Hamiltonian Cycle, Clique
 Optimization version (TSP) → NP-hard
 Decision versions (HC, Clique) → NP-complete

Thus classification:
	•	TSP optimization → NP-hard
	•	Hamiltonian Cycle → NP-complete
	•	Clique → NP-complete

⸻

6. Cryptography, factoring large integers
 Factoring → in NP, not known to be in P, not known NP-complete
 Many cryptographic hardness assumptions rely on “believed exponential complexity”.

So:
	•	Factoring → NP, believed hard, but not NP-complete
	•	Cryptographic problems → often outside P, but not NP-complete

⸻

7. Halting problem, Busy Beaver
 Undecidable (not in any of P/NP)
— Halting problem cannot be solved by any algorithm.
— Busy Beaver grows faster than any computable function.

Final Table
|Problem                                 |Class                               |
|max, BFS shortest-path, matrix multiply |P                                   |
|sorting, BFS/DFS, Dijkstra              |P                                   |
|sudoku                                  |NP-complete                         |
|3-coloring, scheduling                  |NP-complete                         |
|TSP (opt)                               |NP-hard                             |
|HC, Clique                              |NP-complete                         |
|factoring                               |in NP (not known to be NP-complete) |
|halting, busy beaver                    |undecidable                         |


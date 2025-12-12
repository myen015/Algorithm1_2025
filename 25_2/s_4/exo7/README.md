# Exo 7: Graph Algorithms & Bron-Kerbosch

## Explanation
This script executes two problems:
1.  **Graph Operations**: It generates a directed graph's transpose and determines the inverse (complement) edges of an undirected graph.
2.  **Bron-Kerbosch Trace**: It performs a recursive search for maximal cliques. The log below tracks the state of **R** (current clique), **P** (candidates), and **X** (excluded nodes) at every depth of the recursion.

## Script Output
```text
--- PROBLEM 1 OUTPUT ---
Original Directed: {'A': ['B'], 'B': ['C'], 'C': ['A']}
Transposed: {'A': ['C'], 'B': ['A'], 'C': ['B']}

Original Edges: [('A', 'B'), ('B', 'C'), ('C', 'D')]
Inverse Edges: [('A', 'C'), ('A', 'D'), ('B', 'D')]

--- PROBLEM 2: BRON-KERBOSCH TRACE ---
Starting Algorithm...
Step Call: R=set(), P={'A', 'B', 'D', 'C'}, X=set()
  Step Call: R={'A'}, P={'B', 'C'}, X=set()
    Step Call: R={'B', 'A'}, P={'C'}, X=set()
      Step Call: R={'B', 'C', 'A'}, P=set(), X=set()
      -> Found Maximal Clique: {'B', 'C', 'A'}
    Step Call: R={'C', 'A'}, P=set(), X={'B'}
  Step Call: R={'B'}, P={'C'}, X={'A'}
    Step Call: R={'B', 'C'}, P=set(), X={'A'}
  Step Call: R={'D'}, P={'C'}, X=set()
    Step Call: R={'D', 'C'}, P=set(), X=set()
    -> Found Maximal Clique: {'D', 'C'}
  Step Call: R={'C'}, P=set(), X={'B', 'D', 'A'}

--- RESULTS ---
All Maximal Cliques Found:
{'B', 'C', 'A'}
{'D', 'C'}
Maximum Clique is: {'B', 'C', 'A'} with size 3

```bash
python Exo_7.ipynb
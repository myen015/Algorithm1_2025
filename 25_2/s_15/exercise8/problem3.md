Graph:

Edges:
A → B
A → C
B → C
B → D
C → E
D → E
D → F
G → F
G → E

1. Topological sort starting from A

Use DFS or Kahn’s Algorithm (in-degree).

One possible result:
A, B, D, C, G, F, E

2. Starting from another random node

Let’s start from G:
G, A, B, D, C, F, E

Another valid topological order:
A, G, B, C, D, F, E



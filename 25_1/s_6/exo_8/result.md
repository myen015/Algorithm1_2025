PS C:\Users\Asus\exo_8> python problem1_1_reverse_graph.py
Original graph:
A -> ['B', 'C']
B -> ['D']
C -> ['D']
D -> []

Reversed graph:
A -> []
B -> ['A']
C -> ['A']
D -> ['B', 'C']
PS C:\Users\Asus\exo_8> python problem1_2_scc_acyclic.py
SCCs:
Component 0: ['A', 'C', 'B']
Component 1: ['D', 'E']     

SCC Graph:
0 -> [1]

SCC graph is acyclic
PS C:\Users\Asus\exo_8> python problem1_3_scc_reverse_proof.py
original graph G:
A -> ['B']
B -> ['C']
C -> ['A', 'D']
D -> ['E']
E -> ['D']

scc(G):
0 -> [1]
1 -> []
reversed graph rev(G):
A -> ['C']
B -> ['A']
C -> ['B']
D -> ['C', 'E']
E -> ['D']

scc(rev(G)):
0 -> [1]
1 -> []

rev(scc(G)):
0 -> []
1 -> [0]

they are the same
PS C:\Users\Asus\exo_8> python problem1_4_reachability.py
components:
S0: ['A', 'C', 'B']
S1: ['D', 'E']

checking reachability:

result: True

can S(A)=S0 reach S(E)=S1 in scc(G)?
result: True

both are True - proof works
PS C:\Users\Asus\exo_8> python problem2_1_euler_check.py
graph 1
A -> ['B']
B -> ['C']
C -> ['A']

degrees:
A: in=1, out=1
C: in=1, out=1
has euler

========================================

graph 2
A -> ['B', 'C']
B -> ['C']
C -> ['A']

degrees:
A: in=1, out=2
B: in=1, out=1
C: in=2, out=1
no euler
PS C:\Users\Asus\exo_8> python problem2_2_euler_find.py
graph:
A -> ['B']
B -> ['C']
C -> ['D']
D -> ['A']

degrees:
A: in=1, out=1
B: in=1, out=1
C: in=1, out=1
D: in=1, out=1

euler tour found
A -> B -> C -> D -> A
PS C:\Users\Asus\exo_8> python problem3_topological_sort.py
graph:
A -> ['B', 'C']
B -> ['C', 'D']
C -> ['E']
D -> ['E', 'F']
E -> []
F -> []
G -> ['F', 'E']

==================================================
topological sort start from A
G -> A -> B -> D -> F -> C -> E

==================================================
topological sort start from G
A -> B -> D -> C -> G -> E -> F

==================================================
topological sort start from B
G -> A -> B -> D -> F -> C -> E
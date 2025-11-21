# N-ary Tree Weight Sum

This repository contains a C++ implementation of an **n-ary tree** where each child has a weight equal to `parent_weight / n`. The code includes:

- Depth-First Search (DFS) recursive sum
- Breadth-First Search (BFS) iterative sum
- DFS/BFS with weight flipping
- Recursive BFS version

The tree is generated with:

- Depth = 3
- Root weight = `1 / (depth + 1)` so that total weight sums to 1
- Any number of children `n`

---

## Sample Output

DFS sum: 1
BFS sum: 1
DFS flip: -1
BFS flip: 1
DFS flip again: -1
BFS flip again: 1
Recursive BFS sum: 1

---

## Notes

- The `flip` functions change the sign of each node's weight when visited.
- BFS is implemented both iteratively and recursively (recursive version uses level vectors).
- The total sum is always 1, regardless of the number of children `n`.

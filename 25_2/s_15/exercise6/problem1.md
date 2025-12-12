
# Problem 1 — n-ary Tree with Fractional Weights

In this problem, we work with a special n-ary tree where each node has **n children**,  
and each child receives **1/n** of its parent’s weight.

The goal is to construct such a tree, traverse it using DFS and BFS, flip signs,  
and analyze why recursive DFS is natural while recursive BFS is not.

---

## 1. General Class

I implemented a `TreeNode` class that contains:

- `weight` — float value
- `children` — list of TreeNode
- `generate_children()` — creates n children, each with weight `parent_weight / n`

This models exactly the structure described in the assignment.

---

## 2. Building a Tree of Depth N = 3

Using the class, I wrote `build_tree(depth, n, root_weight)`.

For each node, we generate n children and extend the next level.  
Depth 3 gives a full n-ary tree.

Root weight = **1/n**, and since children divide weight further,  
the total sum over all nodes must equal **1**.

---

## 3. Recursive Depth-First Search

`dfs_sum(node)` visits the tree recursively and accumulates weights.

For many values of **n**, the total sum returns **1**,  
proving that the fractional weight distribution is preserved.

---

## 4. Breadth-First Search (Iterative)

I implemented BFS using a queue (`collections.deque`).  
Again, the sum returns **1**, confirming correctness.

---

## 5. Searching with Sign Flips

In this variant, every time we visit a node we flip its weight:
weight *= -1
Both DFS and BFS versions were implemented.

For any fixed tree with fixed n, 
I obtain +1 on the first run and -1 on the second run, as required.

---

## 6. Recursive and Non-Recursive Versions of BFS

DFS is naturally recursive because depth-first order matches recursion behavior.

However, BFS requires a queue and processes nodes by levels.  
This order is not naturally represented by a call stack,  
so recursive BFS is not recommended and becomes unnatural.

---

## 7. Why DFS Can Be Recursive but BFS Cannot

DFS = recursion follows tree edges downward  
BFS = needs a queue and processes nodes horizontally by levels  

Therefore:

- DFS recursion = natural  
- BFS recursion = forced and inefficient

This is why BFS is traditionally implemented iteratively.

---

## 8. Code

All my implementations are included in `problem1.py` as requested.

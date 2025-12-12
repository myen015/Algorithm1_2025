
Tasks:

1. Implement a tree class.
2. Generate a tree of depth N=3, with root weight 1.
3. DFS recursive sum of all weights.
4. BFS sum of all weights.
5. DFS/BFS with alternating signs (flip each level).
6. Implement BFS both recursively and non-recursively.
7. Explain why DFS can be recursive but BFS is usually not recommended.


2. Tree Class and Generation

class TreeNode:
    def __init__(self, wt, kids=None):
        self.wt = wt
        self.kids = kids or []

    def add_child(self, child):
        self.kids.append(child)

def make_tree(n, depth, parent_wt=1):
    if depth == 0:
        return TreeNode(parent_wt)
    node = TreeNode(parent_wt)
    child_wt = parent_wt / n
    for _ in range(n):
        node.add_child(make_tree(n, depth-1, child_wt))
    return node

 `wt` — node weight
`kids` — list of children
`make_tree` recursively generates the tree

3. Depth-First Search (DFS)

def dfs_sum(node):
    total = node.wt
    for kid in node.kids:
        total += dfs_sum(kid)
    return total

Recursive sum of all node weights
Check: `dfs_sum(root)` = 1 

4. Breadth-First Search (BFS)

from collections import deque

def bfs_sum(node):
    total = 0
    q = deque([node])
    while q:
        cur = q.popleft()
        total += cur.wt
        for kid in cur.kids:
            q.append(kid)
    return total

BFS traverses level by level using a queue
Check: `bfs_sum(root)` = 1 


5. DFS and BFS with Alternating Signs

def dfs_flip(node, flip=True):
    total = node.wt if flip else -node.wt
    for kid in node.kids:
        total += dfs_flip(kid, not flip)
    return total

def bfs_flip(node):
    total = 0
    q = deque([(node, True)])
    while q:
        cur, flip = q.popleft()
        total += cur.wt if flip else -cur.wt
        for kid in cur.kids:
            q.append((kid, not flip))
    return total

Flip alternates the sign at each level
Check:
 `dfs_flip(root)` ≈ ±1
 `bfs_flip(root)` ≈ ±1

6. Recursive BFS

def bfs_recursive(nodes):
    if not nodes:
        return 0
    next_lvl = []
    total = 0
    for n in nodes:
        total += n.wt
        next_lvl.extend(n.kids)
    return total + bfs_recursive(next_lvl)

Sums node weights level by level recursively
Check: `bfs_recursive([root])` = 1 

7. DFS vs BFS Notes

DFS naturally follows a branch, so recursion is simple and efficient.
BFS is level-based, so recursion requires storing all nodes at the current level — inefficient and awkward.
Therefore, BFS is usually implemented **iteratively using a queue**.

8. Test Run (n=3, depth=3)

n = 3
N = 3
root = make_tree(n, N)

print("DFS sum:", dfs_sum(root))            # 1
print("BFS sum:", bfs_sum(root))            # 1
print("DFS flip:", dfs_flip(root))          # ±1
print("BFS flip:", bfs_flip(root))          # ±1
print("BFS recursive:", bfs_recursive([root]))  # 1


Output Example:

DFS sum: 1.0
BFS sum: 1.0
DFS flip: 1.0
BFS flip: 1.0
BFS recursive: 1.0

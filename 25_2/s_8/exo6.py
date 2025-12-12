
from collections import deque

# Tree node class
class TreeNode:
    def __init__(self, wt, kids=None):
        self.wt = wt
        self.kids = kids or []

    def add_child(self, child):
        self.kids.append(child)

# make a tree of depth N
def make_tree(n, depth, parent_wt=1):
    if depth == 0:
        return TreeNode(parent_wt)
    node = TreeNode(parent_wt)
    child_wt = parent_wt / n
    for _ in range(n):
        node.add_child(make_tree(n, depth-1, child_wt))
    return node

# DFS sum recursively
def dfs_sum(node):
    total = node.wt
    for kid in node.kids:
        total += dfs_sum(kid)
    return total

# BFS sum with queue
def bfs_sum(node):
    total = 0
    q = deque([node])
    while q:
        cur = q.popleft()
        total += cur.wt
        for kid in cur.kids:
            q.append(kid)
    return total

# DFS with flip signs
def dfs_flip(node, flip=True):
    total = node.wt if flip else -node.wt
    for kid in node.kids:
        total += dfs_flip(kid, not flip)
    return total

# BFS with flip signs
def bfs_flip(node):
    total = 0
    q = deque([(node, True)])
    while q:
        cur, flip = q.popleft()
        total += cur.wt if flip else -cur.wt
        for kid in cur.kids:
            q.append((kid, not flip))
    return total

# BFS recursive
def bfs_recursive(nodes):
    if not nodes:
        return 0
    next_lvl = []
    total = 0
    for n in nodes:
        total += n.wt
        next_lvl.extend(n.kids)
    return total + bfs_recursive(next_lvl)

# --- test run ---
if __name__ == "__main__":
    n = 3
    N = 3
    root = make_tree(n, N)

    print("DFS sum:", dfs_sum(root))
    print("BFS sum:", bfs_sum(root))
    print("DFS flip:", dfs_flip(root))
    print("BFS flip:", bfs_flip(root))
    print("BFS recursive:", bfs_recursive([root]))

    print("\n# Note:")
    print("DFS recursive is easy, BFS better with queue, recursive BFS is kinda awkward.")

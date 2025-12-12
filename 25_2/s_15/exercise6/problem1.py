class TreeNode:
    def __init__(self, weight, n):
        self.weight = weight
        self.children = []
        self.n = n

    def generate_children(self):
        child_weight = self.weight / self.n
        for _ in range(self.n):
            self.children.append(TreeNode(child_weight, self.n))


def build_tree(depth, n, root_weight):
    root = TreeNode(root_weight, n)
    level = [root]
    for _ in range(depth):
        new_level = []
        for node in level:
            node.generate_children()
            new_level.extend(node.children)
        level = new_level
    return root


# DFS recursive sum
def dfs_sum(node):
    s = node.weight
    for child in node.children:
        s += dfs_sum(child)
    return s


# DFS with flip (+1 then -1)
def dfs_flip(node):
    node.weight *= -1
    s = node.weight
    for child in node.children:
        s += dfs_flip(child)
    return s


# BFS iterative sum
from collections import deque

def bfs_sum(root):
    q = deque([root])
    total = 0
    while q:
        node = q.popleft()
        total += node.weight
        q.extend(node.children)
    return total


# BFS with flip
def bfs_flip(root):
    q = deque([root])
    total = 0
    while q:
        node = q.popleft()
        node.weight *= -1
        total += node.weight
        q.extend(node.children)
    return total


# Test run
if __name__ == "__main__":
    n = 3
    depth = 3
    root = build_tree(depth, n, 1/n)

    print("DFS sum:", dfs_sum(root))
    root = build_tree(depth, n, 1/n)
    print("BFS sum:", bfs_sum(root))

    root = build_tree(depth, n, 1/n)
    print("DFS flip:", dfs_flip(root))

    root = build_tree(depth, n, 1/n)
    print("BFS flip:", bfs_flip(root))

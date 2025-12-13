from collections import deque


class TreeNode:
    def __init__(self, weight):
        self.weight = weight
        self.children = []


def build_tree(weight, n, depth):
    node = TreeNode(weight)

    if depth == 0:
        return node

    child_weight = weight / n
    for _ in range(n):
        child = build_tree(child_weight, n, depth - 1)
        node.children.append(child)

    return node


def dfs_sum(node):
    total = node.weight
    for child in node.children:
        total += dfs_sum(child)
    return total


def bfs_sum(root):
    queue = deque([root])
    total = 0

    while queue:
        node = queue.popleft()
        total += node.weight
        for child in node.children:
            queue.append(child)

    return total


def dfs_flip_sum(node):
    node.weight *= -1
    total = node.weight
    for child in node.children:
        total += dfs_flip_sum(child)
    return total


def bfs_flip_sum(root):
    queue = deque([root])
    total = 0

    while queue:
        node = queue.popleft()
        node.weight *= -1
        total += node.weight
        for child in node.children:
            queue.append(child)

    return total


def bfs_iterative(root):
    queue = deque([root])
    visited_weights = []

    while queue:
        node = queue.popleft()
        visited_weights.append(node.weight)
        for child in node.children:
            queue.append(child)

    return visited_weights

def bfs_recursive(queue, visited_weights):
    if not queue:
        return

    node = queue.pop(0)
    visited_weights.append(node.weight)

    for child in node.children:
        queue.append(child)

    bfs_recursive(queue, visited_weights)


if __name__ == "__main__":
    n = 4
    depth = 3

    root = build_tree(1, n, depth)
    print("DFS sum =", dfs_sum(root))
    print("BFS sum =", bfs_sum(root))

    root = build_tree(1, n, depth)
    print("DFS flip:", dfs_flip_sum(root), dfs_flip_sum(root))

    root = build_tree(1, n, depth)
    print("BFS flip:", bfs_flip_sum(root), bfs_flip_sum(root))

    print("BFS iterative:", bfs_iterative(root))

    res = []
    bfs_recursive([root], res)
    print("BFS recursive:", res)

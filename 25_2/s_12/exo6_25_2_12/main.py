from collections import deque


class Node:
    def __init__(self, weight, children=None):
        self.weight = weight
        self.children = children or []


def build_tree(weight, n, depth):
    if depth == 0:
        return Node(weight)
    return Node(weight, [build_tree(weight / n, n, depth - 1) for _ in range(n)])


def dfs_sum(node):
    return node.weight + sum(dfs_sum(c) for c in node.children)


def bfs_sum(root):
    q = deque([root])
    total = 0
    while q:
        node = q.popleft()
        total += node.weight
        q.extend(node.children)
    return total


def dfs_flip(node):
    total = node.weight
    node.weight *= -1
    for c in node.children:
        total += dfs_flip(c)
    return total


def bfs_flip(root):
    q = deque([root])
    total = 0
    while q:
        node = q.popleft()
        total += node.weight
        node.weight *= -1
        q.extend(node.children)
    return total


def bfs_iter(root):
    q = deque([root])
    while q:
        node = q.popleft()
        q.extend(node.children)


def bfs_rec(queue):
    if not queue:
        return
    node = queue.popleft()
    queue.extend(node.children)
    bfs_rec(queue)


if __name__ == "__main__":
    n = 3
    root = build_tree(1.0, n, 3)

    print("DFS sum:", dfs_sum(root))
    print("BFS sum:", bfs_sum(root))

    root = build_tree(1.0, n, 3)
    print("DFS flip:", dfs_flip(root))
    print("BFS flip:", bfs_flip(root))

    root = build_tree(1.0, n, 3)
    bfs_iter(root)
    bfs_rec(deque([root]))


#Why BFS should not be recursive

 #Breadth-first search uses a queue.
 #Recursive BFS grows the call stack with each level and may cause stack overflow.
 #Depth-first search follows a single path and fits recursion naturally.
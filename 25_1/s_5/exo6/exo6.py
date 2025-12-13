from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Node:
    weight: float = 0.0
    children: List["Node"] = field(default_factory=list)


def build_tree(depth: int, n: int, root_weight: float) -> Node:
    root = Node(root_weight)
    if depth == 0:
        return root 
    child_weight = root_weight / n
    root.children = [build_tree(depth - 1, n, child_weight) for _ in range(n)]
    return root


def is_leaf(node: Node) -> bool:
    return len(node.children) == 0


def dfs_sum_leaves(root: Optional[Node]) -> float:
    def _dfs(node: Optional[Node]) -> float:
        if node is None:
            return 0.0
        if is_leaf(node):
            return node.weight
        return sum(_dfs(ch) for ch in node.children)

    return _dfs(root)


def bfs_sum_leaves(root: Optional[Node]) -> float:
    if root is None:
        return 0.0
    q = deque([root])
    s = 0.0
    while q:
        node = q.popleft()
        if is_leaf(node):
            s += node.weight
        else:
            q.extend(node.children)
    return s


def dfs_flip_and_sum_leaves(root: Optional[Node]) -> float:
    def _dfs(node: Optional[Node]) -> float:
        if node is None:
            return 0.0
        node.weight = -node.weight
        if is_leaf(node):
            return node.weight
        return sum(_dfs(ch) for ch in node.children)

    return _dfs(root)


def bfs_flip_and_sum_leaves(root: Optional[Node]) -> float:
    if root is None:
        return 0.0
    q = deque([root])
    s = 0.0
    while q:
        node = q.popleft()
        node.weight = -node.weight
        if is_leaf(node):
            s += node.weight
        else:
            q.extend(node.children)
    return s


def bfs_sum_leaves_recursive(root: Optional[Node]) -> float:
    def bfs_level(level: List[Node]) -> float:
        if not level:
            return 0.0
        next_level: List[Node] = []
        s = 0.0
        for node in level:
            if is_leaf(node):
                s += node.weight
            else:
                next_level.extend(node.children)
        return s + bfs_level(next_level)

    return 0.0 if root is None else bfs_level([root])


def bfs_flip_and_sum_leaves_recursive(root: Optional[Node]) -> float:
    def bfs_level(level: List[Node]) -> float:
        if not level:
            return 0.0
        next_level: List[Node] = []
        s = 0.0
        for node in level:
            node.weight = -node.weight
            if is_leaf(node):
                s += node.weight
            else:
                next_level.extend(node.children)
        return s + bfs_level(next_level)

    return 0.0 if root is None else bfs_level([root])


def solve():
    depth = 3
    n = 3
    root_weight = 1.0

    root = build_tree(depth, n, root_weight)

    print(f"n = {n}, depth = {depth}")
    dfs_sum = dfs_sum_leaves(root)
    print(f"DFS sum of leaves (no flip) = {dfs_sum}  (expect 1)")
    bfs_sum = bfs_sum_leaves(root)
    print(f"BFS sum of leaves (no flip) = {bfs_sum}  (expect 1)")
    dfs_flip1 = dfs_flip_and_sum_leaves(root)
    print(f"DFS flip #1, sum of leaves = {dfs_flip1}  (expect -1)")
    dfs_flip2 = dfs_flip_and_sum_leaves(root)
    print(f"DFS flip #2, sum of leaves = {dfs_flip2}  (expect +1)")
    bfs_flip1 = bfs_flip_and_sum_leaves(root)
    print(f"BFS flip #1, sum of leaves = {bfs_flip1}")

    bfs_flip2 = bfs_flip_and_sum_leaves(root)
    print(f"BFS flip #2, sum of leaves = {bfs_flip2}")
    bfs_rec_sum = bfs_sum_leaves_recursive(root)
    print(f"BFS recursive sum of leaves (no flip) = {bfs_rec_sum}")
    bfs_rec_flip1 = bfs_flip_and_sum_leaves_recursive(root)
    print(f"BFS recursive flip #1 sum of leaves = {bfs_rec_flip1}")

    print("Answer to seventh question")
    print(
        "BFS is logically based on a queue of levels\n"
        "A recursive implementation of BFS relies on the call stack and can easily\n"
        "cause stack overflow on large trees, while an iterative implementation\n"
        "with an explicit queue scales much better"
    )


if __name__ == "__main__":
    t = 1
    for _ in range(t):
        solve()

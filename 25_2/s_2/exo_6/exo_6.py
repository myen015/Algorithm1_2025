class Node:
    def __init__(self, weight):
        self.weight = weight
        self.children = []


def build_tree(depth, weight, n):
    node = Node(weight)

    if depth == 0:
        return node

    for _ in range(n):
        child = build_tree(depth - 1, weight / n, n)
        node.children.append(child)

    return node


def dfs_sum(node):
    total = node.weight
    for child in node.children:
        total += dfs_sum(child)
    return total


def bfs_sum(root):
    queue = [root]
    total = 0.0

    while queue:
        current = queue.pop(0)
        total += current.weight

        for child in current.children:
            queue.append(child)

    return total


def dfs_flip(node):
    node.weight = -node.weight
    total = node.weight

    for child in node.children:
        total += dfs_flip(child)

    return total


def bfs_flip(root):
    queue = [root]
    total = 0.0

    while queue:
        current = queue.pop(0)
        current.weight = -current.weight
        total += current.weight

        for child in current.children:
            queue.append(child)

    return total


def bfs_recursive(level_nodes):
    if not level_nodes:
        return 0.0

    next_level = []
    level_sum = 0.0

    for node in level_nodes:
        level_sum += node.weight
        for child in node.children:
            next_level.append(child)

    return level_sum + bfs_recursive(next_level)


def print_tree(node, level=0):
    indent = "   " * level
    print(f"{indent}weight = {node.weight:.6f}")
    for child in node.children:
        print_tree(child, level + 1)


if __name__ == "__main__":
    n = 5
    depth = 3

    # starting weight for the root
    root_weight = 1.0 / (depth + 1)

    root = build_tree(depth, root_weight, n)

    print("Tree Structure (basic print)")
    print_tree(root)

    print("\nSum Checks")
    print("DFS sum:", dfs_sum(root))
    print("BFS sum:", bfs_sum(root))

    print("\nFirst Flip")
    print("DFS flip:", dfs_flip(root))
    print("BFS flip:", bfs_flip(root))

    print("\nSecond Flip")
    print("DFS flip #2:", dfs_flip(root))
    print("BFS flip #2:", bfs_flip(root))

    print("\nRecursive BFS")
    print("Recursive BFS sum:", bfs_recursive([root]))

    print("\nProgram Finished")

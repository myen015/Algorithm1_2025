import collections

class Node:
    def __init__(self, weight, children=None):
        self.weight = weight
        self.children = children if children is not None else []


def generate_tree(depth, n, current_weight=1.0):
    node = Node(current_weight)
    if depth == 0:
        return node
    child_weight = current_weight / n

    # recursion
    for _ in range(n):
        child_node = generate_tree(depth - 1, n, child_weight)
        node.children.append(child_node)

    return node


# recursive DFS
def dfs_sum_leaves(node):
    if not node.children:
        return node.weight
    total = 0
    for child in node.children:
        total += dfs_sum_leaves(child)
    return total


# fliping the value size
def dfs_flip_signs(node):
    node.weight = -node.weight
    for child in node.children:
        dfs_flip_signs(child)


# BFS
def bfs_sum_leaves_iterative(root):
    if not root:
        return 0

    total_weight = 0
    queue = collections.deque([root])

    while queue:
        current_node = queue.popleft()

        if not current_node.children:
            total_weight += current_node.weight
        else:
            for child in current_node.children:
                queue.append(child)

    return total_weight


# recursive BFS
def bfs_recursive(queue, total_weight=0):
    if not queue:
        return total_weight

    next_queue = []
    for node in queue:
        if not node.children:
            total_weight += node.weight
        else:
            next_queue.extend(node.children)

    return bfs_recursive(next_queue, total_weight)


# flipping the value size
def bfs_flip_signs(root):
    queue = collections.deque([root])
    while queue:
        node = queue.popleft()
        node.weight = -node.weight  # Меняем знак
        for child in node.children:
            queue.append(child)


# testing
if __name__ == "__main__":
    N_CHILDREN = 2
    DEPTH = 3

    print("1. tree generation (Depth={DEPTH}, n={N_CHILDREN})")
    root = generate_tree(DEPTH, N_CHILDREN, current_weight=1.0)
    print("tree is generated.")

    # DFS checkup
    print("2. DFS sum check (expected is 1.0)")
    total_dfs = dfs_sum_leaves(root)
    print("sum of leaves (DFS): {total_dfs}")

    # BFS checkup
    print("3. BFS sum check (expected is 1.0)")
    total_bfs = bfs_sum_leaves_iterative(root)
    print("sum of leaves (BFS iterative): {total_bfs}")

    # recursive BFS
    total_bfs_rec = bfs_recursive([root])
    print("sum of leaves (BFS recursive): {total_bfs_rec}")

    # check of signs flipping
    print("4. flipping signs")

    print("starting signs flipping...")
    dfs_flip_signs(root)

    check_sum = dfs_sum_leaves(root)
    print("sum after first flip (expected is -1.0): {check_sum}")

    print("starting the sign change back via BFS...")
    bfs_flip_signs(root)

    final_sum = bfs_sum_leaves_iterative(root)
    print("sum after second flip (expected is 1.0): {final_sum}")

    if abs(final_sum - 1.0) < 0.00001:
        print("SUCCESS: we've got 1 and 1 after both searches")
    else:
        print("NOT SUCCESS: sum is not correct")
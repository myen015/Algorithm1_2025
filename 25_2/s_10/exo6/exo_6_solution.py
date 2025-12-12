class WeightedTreeNode:
    """Tree node with n children, each child has weight = (1/n) * parent's weight."""
    
    def __init__(self, weight, n_children, depth=0, max_depth=None):
        self.weight = weight
        self.n_children = n_children
        self.depth = depth
        self.children = []
        
        if max_depth is None or depth < max_depth:
            child_weight = weight / n_children
            for _ in range(n_children):
                child = WeightedTreeNode(
                    weight=child_weight,
                    n_children=n_children,
                    depth=depth + 1,
                    max_depth=max_depth
                )
                self.children.append(child)


def generate_tree(n_children, max_depth=3, initial_weight=None):
    """Generate tree of depth N with initial parent weight."""
    if initial_weight is None:
        initial_weight = 1.0 / (max_depth + 1)  # Normalize so sum = 1
    return WeightedTreeNode(initial_weight, n_children, 0, max_depth)


def dfs_sum_weights(node, sign_flip=False):
    """DFS: Recursively visit each node and sum weights."""
    weight = -node.weight if sign_flip else node.weight
    
    if not node.children:
        return weight
    
    total = weight
    for child in node.children:
        total += dfs_sum_weights(child, sign_flip)
    return total


def bfs_sum_weights_iterative(root, sign_flip=False):
    """BFS: Iterative version using queue."""
    from collections import deque
    
    queue = deque([root])
    total = 0
    
    while queue:
        node = queue.popleft()
        total += -node.weight if sign_flip else node.weight
        queue.extend(node.children)
    
    return total


def bfs_sum_weights_recursive(nodes, sign_flip=False, total=0):
    """BFS: Recursive version (not recommended)."""
    if not nodes:
        return total
    
    next_level = []
    for node in nodes:
        total += -node.weight if sign_flip else node.weight
        next_level.extend(node.children)
    
    return bfs_sum_weights_recursive(next_level, sign_flip, total)


def test_sum_weights():
    """Test that sum of weights equals 1 for various n values."""
    print("Testing: Sum of weights should equal 1")
    print("-" * 50)
    
    for n in [2, 3, 4, 5]:
        root = generate_tree(n, max_depth=3)
        
        dfs_result = dfs_sum_weights(root, sign_flip=False)
        bfs_iter = bfs_sum_weights_iterative(root, sign_flip=False)
        bfs_rec = bfs_sum_weights_recursive([root], sign_flip=False)
        
        assert abs(dfs_result - 1.0) < 1e-10, f"DFS failed for n={n}"
        assert abs(bfs_iter - 1.0) < 1e-10, f"BFS iterative failed for n={n}"
        assert abs(bfs_rec - 1.0) < 1e-10, f"BFS recursive failed for n={n}"
        
        print(f"n={n}: DFS={dfs_result:.6f}, BFS_iter={bfs_iter:.6f}, BFS_rec={bfs_rec:.6f}")
    
    print("✓ All tests passed!\n")


def test_sign_flip():
    """Test sign flipping: should get 1 and -1 after both searches."""
    print("Testing: Sign flip behavior")
    print("-" * 50)
    
    n = 3
    root = generate_tree(n, max_depth=3)
    
    # First search: no flip
    result1_dfs = dfs_sum_weights(root, sign_flip=False)
    result1_bfs = bfs_sum_weights_iterative(root, sign_flip=False)
    
    # Second search: with flip
    result2_dfs = dfs_sum_weights(root, sign_flip=True)
    result2_bfs = bfs_sum_weights_iterative(root, sign_flip=True)
    
    assert abs(result1_dfs - 1.0) < 1e-10, "First DFS should return 1"
    assert abs(result2_dfs - (-1.0)) < 1e-10, "Second DFS should return -1"
    assert abs(result1_bfs - 1.0) < 1e-10, "First BFS should return 1"
    assert abs(result2_bfs - (-1.0)) < 1e-10, "Second BFS should return -1"
    
    print(f"First search (no flip): DFS={result1_dfs:.6f}, BFS={result1_bfs:.6f}")
    print(f"Second search (flip):   DFS={result2_dfs:.6f}, BFS={result2_bfs:.6f}")
    print("✓ All sign flip tests passed!\n")


def explain_bfs_recursive():
    """Explanation: Why BFS recursive is not recommended."""
    explanation = """
Why BFS recursive is not recommended:

1. Stack Overflow Risk: Recursive BFS maintains state for each level in the call
   stack. For deep trees, this can cause stack overflow errors.

2. Inefficiency: Each recursive call passes the entire list of nodes at the
   current level, creating overhead. The iterative version with a queue is more
   memory-efficient.

3. Complexity: Recursive BFS is more complex to understand and maintain
   compared to the straightforward iterative queue-based approach.

4. Natural Fit: BFS is inherently iterative - you process nodes in a queue,
   which maps naturally to iterative code. DFS, on the other hand, naturally
   follows the recursive structure of the tree.

In contrast, DFS recursive is recommended because:
- It naturally follows the tree structure (visit node, then children)
- The call stack naturally represents the path from root to current node
- It's simpler and more intuitive than iterative DFS with explicit stack
"""
    print(explanation)


if __name__ == "__main__":
    print("=" * 50)
    print("Problem Set #6: Weighted Tree with n Children")
    print("=" * 50)
    
    # Problem 2: Generate tree
    print("\nProblem 2: Generate tree of depth 3")
    root = generate_tree(n_children=3, max_depth=3)
    print(f"Generated tree: n=3, depth=3, root_weight={root.weight:.6f}")
    
    # Problem 3: DFS recursive sum
    print("\nProblem 3: DFS recursive sum")
    test_sum_weights()
    
    # Problem 4: BFS sum
    print("Problem 4: BFS sum")
    # Already tested in test_sum_weights()
    
    # Problem 5: Sign flip
    print("Problem 5: Sign flip tests")
    test_sign_flip()
    
    # Problem 6: Recursive and non-recursive BFS
    print("Problem 6: Recursive and non-recursive BFS")
    print("Both versions implemented and tested above.\n")
    
    # Problem 7: Explanation
    print("Problem 7: Why BFS recursive is not recommended")
    explain_bfs_recursive()
    
    print("=" * 50)
    print("All problems solved!")

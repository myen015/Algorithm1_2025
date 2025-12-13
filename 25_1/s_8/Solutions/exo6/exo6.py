"""
Fundamental Algorithm Techniques - Problem Set #6
Facebook Interview: Tree with weighted children

Each node has n children, each child gets 1/n of parent's weight
"""

from collections import deque

# ============================================================================
# PROBLEM 1: CREATE THE TREE CLASS
# ============================================================================

class WeightedTree:
    """
    A tree where each node has n children
    Each child gets 1/n of the parent's weight
    
    Example: If parent has weight 1 and n=3 children,
    each child gets weight 1/3
    """
    def __init__(self, weight, n_children=0):
        """
        weight: the weight of this node
        n_children: how many children this node has
        """
        self.weight = weight
        self.n_children = n_children
        self.children = []
    
    def add_children(self):
        """Create n children, each with weight = parent_weight / n"""
        if self.n_children > 0:
            child_weight = self.weight / self.n_children
            for i in range(self.n_children):
                child = WeightedTree(child_weight, self.n_children)
                self.children.append(child)
    
    def __repr__(self):
        return f"Node(weight={self.weight:.4f}, children={len(self.children)})"

# ============================================================================
# PROBLEM 2: BUILD A TREE OF DEPTH 3
# ============================================================================

def build_tree(n, depth):
    """
    Build a tree where:
    - Root has weight 1/n
    - Each node has n children
    - Tree goes down 'depth' levels
    
    Example with n=2, depth=3:
    Level 0: root (weight 1/2)
    Level 1: 2 children (each weight 1/4)
    Level 2: 4 grandchildren (each weight 1/8)
    """
    # Start with root
    root = WeightedTree(1.0 / n, n)
    
    # Build level by level
    current_level = [root]
    for level in range(depth):
        next_level = []
        for node in current_level:
            node.add_children()
            next_level.extend(node.children)
        current_level = next_level
    
    return root

# ============================================================================
# PROBLEM 3: DEPTH FIRST SEARCH (DFS) - ADD UP ALL WEIGHTS
# ============================================================================

def dfs_sum_weights(node):
    """
    Go deep first: visit a node, then go all the way down one branch
    before moving to the next branch
    
    Example path: Root -> Child1 -> Grandchild1 -> Grandchild2 -> Child2 ...
    """
    if node is None:
        return 0.0
    
    # Start with this node's weight
    total = node.weight
    
    # Add all children's weights (recursively go deep)
    for child in node.children:
        total += dfs_sum_weights(child)
    
    return total

# ============================================================================
# PROBLEM 4: BREADTH FIRST SEARCH (BFS) - ADD UP ALL WEIGHTS
# ============================================================================

def bfs_sum_weights(root):
    """
    Go wide first: visit all nodes at one level before going deeper
    
    Example path: Root -> All Children -> All Grandchildren ...
    
    Uses a queue (line): add nodes to back, take from front
    """
    if root is None:
        return 0.0
    
    total = 0.0
    queue = deque([root])  # Start with root in the queue
    
    while queue:
        node = queue.popleft()  # Take first node from queue
        total += node.weight
        
        # Add all children to the back of queue
        for child in node.children:
            queue.append(child)
    
    return total

# ============================================================================
# PROBLEM 5: FLIP SIGNS WHILE TRAVERSING
# ============================================================================

def dfs_flip_signs(node):
    """
    Same as DFS but flip the sign of each node's weight
    Positive becomes negative, negative becomes positive
    """
    if node is None:
        return 0.0
    
    # Flip the sign
    node.weight = -node.weight
    
    # Start with flipped weight
    total = node.weight
    
    # Visit children
    for child in node.children:
        total += dfs_flip_signs(child)
    
    return total

def bfs_flip_signs(root):
    """
    Same as BFS but flip the sign of each node's weight
    """
    if root is None:
        return 0.0
    
    total = 0.0
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        
        # Flip the sign
        node.weight = -node.weight
        total += node.weight
        
        for child in node.children:
            queue.append(child)
    
    return total

# ============================================================================
# PROBLEM 6: RECURSIVE VS NON-RECURSIVE BFS
# ============================================================================

def bfs_recursive(nodes, total=0.0):
    """
    BFS using recursion - processes one level at a time
    
    NOT RECOMMENDED! (see problem 7)
    This is just to show it's possible
    """
    if not nodes:
        return total
    
    # Process current level
    next_level = []
    for node in nodes:
        total += node.weight
        next_level.extend(node.children)
    
    # Move to next level
    return bfs_recursive(next_level, total)

# We already have non-recursive BFS above (bfs_sum_weights)

# ============================================================================
# PROBLEM 7: WHY RECURSIVE BFS IS BAD
# ============================================================================

"""
WHY YOU SHOULDN'T USE RECURSION FOR BFS:

1. MEMORY WASTE
   - Recursion uses the call stack (system memory)
   - Each level of the tree = one function call on stack
   - For a tree with depth 100, you have 100 function calls waiting
   - The queue method only keeps track of current level nodes

2. DOESN'T MATCH THE PATTERN
   - BFS is naturally iterative (loop-based)
   - You process nodes level by level in a loop
   - Recursion is naturally for DFS (going deep)
   - Forcing BFS into recursion makes code weird and hard to read

3. STACK OVERFLOW RISK
   - Deep trees can crash the program with recursion
   - Call stack has limited size
   - Queue in memory has much more space available

4. PERFORMANCE
   - Function calls have overhead (setup and cleanup)
   - Simple loop with queue is faster
   - No function call overhead with iteration

SUMMARY: Use recursion for DFS, use iteration (queue) for BFS!
"""

# ============================================================================
# TEST EVERYTHING
# ============================================================================

def run_tests():
    """Test all functions with different values of n"""
    
    print("=" * 70)
    print("TESTING TREE TRAVERSAL WITH WEIGHTED CHILDREN")
    print("=" * 70)
    
    test_ns = [2, 3, 4, 5]
    
    for n in test_ns:
        print(f"\n{'='*70}")
        print(f"Testing with n = {n} children per node, depth = 3")
        print(f"{'='*70}")
        
        # Build tree
        root = build_tree(n, depth=3)
        print(f"✓ Tree built with root weight: {root.weight:.4f}")
        
        # Test DFS sum
        dfs_sum = dfs_sum_weights(root)
        print(f"\nDFS Sum: {dfs_sum:.6f} (should be ≈ 1.0)")
        assert abs(dfs_sum - 1.0) < 0.0001, f"DFS sum failed! Got {dfs_sum}"
        print("✓ DFS test passed!")
        
        # Rebuild tree for BFS test
        root = build_tree(n, depth=3)
        
        # Test BFS sum
        bfs_sum = bfs_sum_weights(root)
        print(f"\nBFS Sum: {bfs_sum:.6f} (should be ≈ 1.0)")
        assert abs(bfs_sum - 1.0) < 0.0001, f"BFS sum failed! Got {bfs_sum}"
        print("✓ BFS test passed!")
        
        # Rebuild tree for BFS recursive test
        root = build_tree(n, depth=3)
        
        # Test BFS recursive
        bfs_rec_sum = bfs_recursive([root])
        print(f"\nBFS Recursive Sum: {bfs_rec_sum:.6f} (should be ≈ 1.0)")
        assert abs(bfs_rec_sum - 1.0) < 0.0001, f"BFS recursive failed! Got {bfs_rec_sum}"
        print("✓ BFS Recursive test passed!")
    
    # Test sign flipping with n=3
    print(f"\n{'='*70}")
    print("TESTING SIGN FLIPPING (n=3)")
    print(f"{'='*70}")
    
    n = 3
    
    # First flip with DFS
    root = build_tree(n, depth=3)
    first_sum = dfs_flip_signs(root)
    print(f"\nAfter 1st DFS flip: {first_sum:.6f} (should be ≈ -1.0)")
    assert abs(first_sum - (-1.0)) < 0.0001, f"First flip failed! Got {first_sum}"
    print("✓ First flip correct!")
    
    # Second flip with DFS (should go back to positive)
    second_sum = dfs_flip_signs(root)
    print(f"After 2nd DFS flip: {second_sum:.6f} (should be ≈ 1.0)")
    assert abs(second_sum - 1.0) < 0.0001, f"Second flip failed! Got {second_sum}"
    print("✓ Second flip correct!")
    
    # Same test with BFS
    root = build_tree(n, depth=3)
    first_sum_bfs = bfs_flip_signs(root)
    print(f"\nAfter 1st BFS flip: {first_sum_bfs:.6f} (should be ≈ -1.0)")
    assert abs(first_sum_bfs - (-1.0)) < 0.0001, f"BFS first flip failed!"
    print("✓ BFS first flip correct!")
    
    second_sum_bfs = bfs_flip_signs(root)
    print(f"After 2nd BFS flip: {second_sum_bfs:.6f} (should be ≈ 1.0)")
    assert abs(second_sum_bfs - 1.0) < 0.0001, f"BFS second flip failed!"
    print("✓ BFS second flip correct!")
    
    print(f"\n{'='*70}")
    print("ALL TESTS PASSED! 🎉")
    print(f"{'='*70}")

# Run all tests
if __name__ == "__main__":
    run_tests()
    
    # Show example tree structure
    print("\nEXAMPLE TREE STRUCTURE (n=2, depth=2):")
    print("-" * 50)
    root = build_tree(2, depth=2)
    
    def print_tree(node, level=0, prefix="Root: "):
        """Helper to visualize tree structure"""
        print("  " * level + prefix + f"weight={node.weight:.4f}")
        for i, child in enumerate(node.children):
            print_tree(child, level + 1, f"Child {i+1}: ")
    
    print_tree(root)
    print("\nSum of all weights:", dfs_sum_weights(root))
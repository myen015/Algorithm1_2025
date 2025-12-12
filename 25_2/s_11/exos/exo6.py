from collections import deque
from typing import List, Optional

# Task 1.1 — Tree Node Class
class MultiwayTreeNode:
    
    def __init__(self, data: float, offspring: Optional[List["MultiwayTreeNode"]] = None):
        self.data = float(data)
        self.offspring = offspring if offspring is not None else []

    def insert_child(self, child_node: "MultiwayTreeNode") -> None:
        """Adds a child node to the current node"""
        self.offspring.append(child_node)

    def __str__(self) -> str:
        """String representation of the node"""
        return f"TreeNode(data={self.data:.4f}, offspring_count={len(self.offspring)})"


# Task 1.2 — Constructing K-ary Tree
def generate_k_ary_tree(branching_factor: int, height: int, initial_value: float) -> MultiwayTreeNode:
    """
    Generates a complete K-ary tree with specified height
    """
    def _generate_layer(current_height: int, node_value: float) -> MultiwayTreeNode:
        new_node = MultiwayTreeNode(node_value)
        if current_height >= height:
            return new_node
        
        # Create child nodes with distributed values
        for _ in range(branching_factor):
            child_value = node_value / branching_factor
            child_node = _generate_layer(current_height + 1, child_value)
            new_node.insert_child(child_node)
        return new_node
    
    return _generate_layer(0, initial_value)


# Task 1.3 — Recursive Depth-First Traversal with Summation
def depth_first_cumulative(node: Optional[MultiwayTreeNode]) -> float:
    """
    Recursive depth-first traversal calculating cumulative sum
    """
    if node is None:
        return 0.0
    
    cumulative_total = node.data
    # Aggregate values from all child nodes
    for child in node.offspring:
        cumulative_total += depth_first_cumulative(child)
    
    return cumulative_total


# Task 1.4 — Iterative Breadth-First Traversal
def breadth_first_cumulative(root: Optional[MultiwayTreeNode]) -> float:
    """
    Iterative breadth-first traversal calculating total sum
    """
    if root is None:
        return 0.0
    
    overall_sum = 0.0
    processing_queue = deque([root])
    
    while processing_queue:
        current = processing_queue.popleft()
        overall_sum += current.data
        # Enqueue all children for processing
        processing_queue.extend(current.offspring)
    
    return overall_sum


# Task 1.5 — Alternating Sign Summations
def depth_first_sign_alternating(node: Optional[MultiwayTreeNode]) -> float:
    """
    Depth-first traversal with alternating signs at each level
    """
    sign_multiplier = 1
    alternating_total = 0.0
    
    def _traverse_with_alternation(current_node: MultiwayTreeNode, sign: int):
        nonlocal alternating_total
        alternating_total += sign * current_node.data
        # Reverse sign for children
        for child in current_node.offspring:
            _traverse_with_alternation(child, -sign)
    
    if node is not None:
        _traverse_with_alternation(node, sign_multiplier)
    return alternating_total


def breadth_first_sign_alternating(root: Optional[MultiwayTreeNode]) -> float:
    """
    Breadth-first traversal with alternating signs per level
    """
    if root is None:
        return 0.0
    
    alternating_sum = 0.0
    level_sign = 1
    current_level = deque([root])
    
    while current_level:
        level_size = len(current_level)
        for _ in range(level_size):
            current_node = current_level.popleft()
            alternating_sum += level_sign * current_node.data
            current_level.extend(current_node.offspring)
        # Flip sign for next level
        level_sign *= -1
    
    return alternating_sum


# Task 1.6 — Recursive Breadth-First Approach
def recursive_breadth_accumulation(root: Optional[MultiwayTreeNode]) -> float:
    """
    Recursive implementation of breadth-first accumulation
    """
    if root is None:
        return 0.0
    
    def _accumulate_level(nodes_at_level: List[MultiwayTreeNode]) -> float:
        if not nodes_at_level:
            return 0.0
        
        level_sum = 0.0
        next_level_nodes = []
        
        # Process current level
        for node in nodes_at_level:
            level_sum += node.data
            next_level_nodes.extend(node.offspring)
        
        # Recursively process subsequent level
        return level_sum + _accumulate_level(next_level_nodes)
    
    return _accumulate_level([root])


# Additional Analytical Utilities
def compute_tree_metrics(root: MultiwayTreeNode) -> dict:
    """
    Computes comprehensive tree metrics: node count, depth, statistical measures
    """
    def _aggregate_metrics(node: MultiwayTreeNode, depth: int, metrics: dict):
        metrics["node_count"] += 1
        metrics["value_sum"] += node.data
        metrics["maximum_depth"] = max(metrics["maximum_depth"], depth)
        
        for child in node.offspring:
            _aggregate_metrics(child, depth + 1, metrics)
    
    metrics = {
        "node_count": 0,
        "value_sum": 0.0,
        "maximum_depth": 0,
        "mean_value": 0.0
    }
    
    _aggregate_metrics(root, 0, metrics)
    metrics["mean_value"] = metrics["value_sum"] / metrics["node_count"] if metrics["node_count"] > 0 else 0.0
    
    return metrics


def display_tree_analysis(root: MultiwayTreeNode, tree_identifier: str = "Tree"):
    """
    Displays comprehensive tree analysis summary
    """
    metrics = compute_tree_metrics(root)
    dfs_result = depth_first_cumulative(root)
    bfs_result = breadth_first_cumulative(root)
    
    print(f"\n=== {tree_identifier} Analysis ===")
    print(f"Total nodes: {metrics['node_count']}")
    print(f"Maximum depth: {metrics['maximum_depth']}")
    print(f"Average node value: {metrics['mean_value']:.6f}")
    print(f"DFS cumulative sum: {dfs_result:.6f}")
    print(f"BFS cumulative sum: {bfs_result:.6f}")
    print(f"Consistency check: {abs(dfs_result - bfs_result) < 1e-10}")


# Comparative Analysis Function
def perform_comparative_analysis():
    """
    Performs comparative analysis of different tree configurations
    """
    print("K-ary Tree Structure Analysis")
    print("=" * 55)
    
    # Test configurations
    analysis_configurations = [
        {"branches": 2, "levels": 3, "root_value": 0.25},
        {"branches": 3, "levels": 3, "root_value": 0.25},
        {"branches": 4, "levels": 3, "root_value": 0.25},
        {"branches": 2, "levels": 4, "root_value": 0.20}
    ]
    
    for config_num, config in enumerate(analysis_configurations, 1):
        k = config["branches"]
        levels = config["levels"]
        root_val = config["root_value"]
        
        # Generate tree structure
        tree_structure = generate_k_ary_tree(k, levels, root_val)
        
        print(f"\n--- Analysis {config_num}: K={k}, Levels={levels} ---")
        
        # Core traversal results
        dfs_total = depth_first_cumulative(tree_structure)
        bfs_iterative = breadth_first_cumulative(tree_structure)
        bfs_recursive = recursive_breadth_accumulation(tree_structure)
        
        print(f"DFS total: {dfs_total:.6f}")
        print(f"BFS iterative: {bfs_iterative:.6f}")
        print(f"BFS recursive: {bfs_recursive:.6f}")
        
        # Alternating sign analyses
        dfs_alternating = depth_first_sign_alternating(tree_structure)
        bfs_alternating = breadth_first_sign_alternating(tree_structure)
        
        print(f"Alternating DFS: {dfs_alternating:.6f}")
        print(f"Alternating BFS: {bfs_alternating:.6f}")
        
        # Validation checks
        print(f"DFS == BFS: {abs(dfs_total - bfs_iterative) < 1e-10}")
        print(f"BFS methods consistent: {abs(bfs_iterative - bfs_recursive) < 1e-10}")
    
    # Detailed structural analysis
    print("\n" + "=" * 55)
    sample_tree = generate_k_ary_tree(3, 3, 0.25)
    display_tree_analysis(sample_tree, "Structural Analysis")


# Performance verification
def verify_tree_properties():
    """
    Verifies mathematical properties of the tree structure
    """
    print("\nTree Property Verification")
    print("-" * 35)
    
    test_tree = generate_k_ary_tree(3, 3, 1.0)
    
    # Property 1: Sum of all nodes should equal root value
    total_sum = depth_first_cumulative(test_tree)
    print(f"Root value: 1.000000")
    print(f"Total sum: {total_sum:.6f}")
    print(f"Sum equals root: {abs(total_sum - 1.0) < 1e-10}")
    
    # Property 2: Each level's sum equals parent level sum
    metrics = compute_tree_metrics(test_tree)
    print(f"Total nodes: {metrics['node_count']}")
    print(f"Expected nodes: {sum([3**i for i in range(4)])}")
    
    # Property 3: Alternating sums should differ
    dfs_alt = depth_first_sign_alternating(test_tree)
    bfs_alt = breadth_first_sign_alternating(test_tree)
    print(f"Alternating methods yield different results: {abs(dfs_alt - bfs_alt) > 1e-10}")


if __name__ == "__main__":
    perform_comparative_analysis()
    verify_tree_properties()
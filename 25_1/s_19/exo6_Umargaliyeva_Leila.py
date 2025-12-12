from collections import deque

class WeightedTree:
    def __init__(self, weight, n_children=0, depth=0):
        self.weight = weight
        self.children = []
        
        if depth > 0 and n_children > 0:
            w_child = weight / n_children
            for k in range(n_children):
                child_node = WeightedTree(w_child, n_children, depth - 1)
                self.children.append(child_node)
    
    def __repr__(self):
        return f"Node(weight={self.weight:.6f}, children={len(self.children)})"


# PROBLEM 3: DEPTH FIRST SEARCH

def dfs_sum(tree_node):
    if tree_node is None:
        return 0
    
    weight_sum = tree_node.weight
    
    for child_node in tree_node.children:
        weight_sum += dfs_sum(child_node)
    
    return weight_sum


# PROBLEM 4: BREADTH FIRST SEARCH

def bfs_sum(root_node):
    if root_node is None:
        return 0
    
    running_total = 0
    node_queue = deque([root_node])
    
    while node_queue:
        current_node = node_queue.popleft()
        running_total += current_node.weight
        
        for kid in current_node.children:
            node_queue.append(kid)
    
    return running_total


# PROBLEM 5: FLIP SIGNS

def dfs_flip(tree_node):
    if tree_node is None:
        return 0
    
    tree_node.weight = -tree_node.weight
    weight_sum = tree_node.weight
    
    for child_node in tree_node.children:
        weight_sum += dfs_flip(child_node)
    
    return weight_sum


def bfs_flip(root_node):

    if root_node is None:
        return 0
    
    total_flipped = 0
    node_queue = deque([root_node])
    
    while node_queue:
        current_node = node_queue.popleft()
        current_node.weight = -current_node.weight
        total_flipped += current_node.weight
        
        for c in current_node.children:
            node_queue.append(c)
    
    return total_flipped



# PROBLEM 6: BFS (ITERATIVE + RECURSIVE)

def bfs_iterative(root_node):
 
    if root_node is None:
        return 0
    
    weight_sum = 0
    node_queue = deque([root_node])
    
    while node_queue:
        current_node = node_queue.popleft()
        weight_sum += current_node.weight
        
        for child_node in current_node.children:
            node_queue.append(child_node)
    
    return weight_sum


def bfs_recursive(level_nodes):
    if not level_nodes:
        return 0
    
    level_sum = sum(nd.weight for nd in level_nodes)
    
    next_level = []
    for nd in level_nodes:
        next_level.extend(nd.children)
    
    return level_sum + bfs_recursive(next_level)



# MAIN TESTING SECTION

def main():
    print("PROBLEM SET #6: WEIGHTED TREE")
    
    print("\nProblem 2: create example tree")
    n = 3
    depth = 3
    sample_tree = WeightedTree(1.0, n_children=n, depth=depth)
    print("Tree created:", sample_tree)
    print("Number of children on level 1:", len(sample_tree.children))
    
    print("\nProblem 3: DFS sum")
    for num_children in [2, 3, 4, 5]:
        t = WeightedTree(1.0, n_children=num_children, depth=3)
        s = dfs_sum(t)
        print(f"{num_children} children → sum = {s:.6f}")
    
    print("\nProblem 4: BFS sum")
    for num_children in [2, 3, 4, 5]:
        t = WeightedTree(1.0, n_children=num_children, depth=3)
        s = bfs_sum(t)
        print(f"{num_children} children → sum = {s:.6f}")
    
    print("\nProblem 5: flip signs")
    t = WeightedTree(1.0, n_children=4, depth=3)
    
    original = dfs_sum(t)
    print("Initial sum:", original)
    
    neg = dfs_flip(t)
    print("After DFS flip:", neg)
    
    check_neg = dfs_sum(t)
    print("Check negative sum:", check_neg)
    
    back_pos = bfs_flip(t)
    print("After BFS flip:", back_pos)
    
    verify = bfs_sum(t)
    print("Check restored positive sum:", verify)
    
    print("\nProblem 6: BFS recursive vs iterative")
    tree_6 = WeightedTree(1.0, n_children=3, depth=3)
    
    it_sum = bfs_iterative(tree_6)
    rec_sum = bfs_recursive([tree_6])
    
    print("Iterative BFS:", it_sum)
    print("Recursive BFS:", rec_sum)
    print("Equal results? →", abs(it_sum - rec_sum) < 1e-10)



if __name__ == "__main__":
    main()

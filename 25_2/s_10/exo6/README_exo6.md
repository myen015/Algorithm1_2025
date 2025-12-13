# Problem Set #6 - Solution

## Overview
Facebook Interview Problem: Weighted Tree with n Children

Tree structure where each node has `n` children, and each child has weight = (1/n) × parent's weight.

## Files
- `exo_6_solution.py`: Complete solution

## Running
```bash
python exo_6_solution.py
```

## Solutions

### Problem 1: General Class
- `WeightedTreeNode`: Tree node class with n children

### Problem 2: Generate Tree
- `generate_tree()`: Creates tree of depth 3
- Root weight normalized to 1/(max_depth+1) so total sum = 1

### Problem 3: DFS Recursive Sum
- `dfs_sum_weights()`: Depth-first recursive traversal
- Returns 1 for n = 2, 3, 4, 5

### Problem 4: BFS Sum
- `bfs_sum_weights_iterative()`: Iterative BFS (recommended)
- `bfs_sum_weights_recursive()`: Recursive BFS (not recommended)
- Both return 1

### Problem 5: Sign Flip
- `sign_flip` parameter in both DFS and BFS
- First search: returns 1
- Second search: returns -1

### Problem 6: Recursive and Non-Recursive BFS
- Both versions implemented and tested

### Problem 7: Why BFS Recursive is Not Recommended
1. Stack overflow risk for deep trees
2. Inefficiency: passing entire level lists
3. Complexity: harder to understand
4. Natural fit: BFS is inherently iterative

DFS recursive is recommended because it naturally follows tree structure.

## Test Results
- ✓ Sum equals 1 for n = 2, 3, 4, 5
- ✓ Sign flip: first = 1, second = -1
- ✓ All implementations verified
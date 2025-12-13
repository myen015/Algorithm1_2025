Breadth-first search explores nodes level by level.
This naturally requires a queue to store all nodes at the current level

Using recursion for BFS:
- Replaces the queue with the call stack
- Can easily lead to stack overflow for wide trees
- Is harder to read and less efficient

Depth-first search works well recursively because:
- It follows one branch at a time
- The call stack naturally represents the traversal path

DFS → suitable for recursion 
BFS → should be implemented iteratively
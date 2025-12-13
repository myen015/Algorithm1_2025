# Exercise 6: Weighted Tree Algorithms

## Quick Start

```bash
javac exo_6/*.java
java exo_6.Main
```

---

## Overview

| Component | Description |
|-----------|-------------|
| **WeightedTreeNode.java** | Tree node class |
| **TreeAlgorithms.java** | Traversal algorithms (DFS, BFS) |
| **Main.java** | Main program |

---

## Tree Structure Specification

### Weight Calculation

| Property | Formula | Example |
|----------|---------|---------|
| Root weight | `1/n` | n=3 → weight=1/3 |
| Child weight | `(1/n) × parent_weight` | parent=1/3, n=3 → child=1/9 |
| Depth d weight | `(1/n)^(d+1)` | depth=2, n=3 → (1/3)^3 = 1/27 |

### Tree Construction
```
For each node:
  - Generate n children
  - Assign weight = parent_weight / n
  - Recursively build subtree
```

---

## Algorithm Examples

### Example 1: DFS Traversal

**Tree Structure:**
```
        Root (w=1/3)
       /  |  \
   Child1 Child2 Child3 (w=1/9 each)
   / | \  / | \  / | \
  ... (depth 2)
```

**DFS Order:** Root → Child1 → (subtree) → Child2 → (subtree) → Child3 → (subtree)

**Implementation:**
- Recursive depth-first traversal
- Naturally fits for trees
- Call stack represents path from root

### Example 2: BFS Traversal

**BFS Order:** Root → Child1, Child2, Child3 → (all depth 2 nodes) → ...

**Implementation:**
- Iterative version (recommended) - uses queue
- Recursive version (not recommended) - for demonstration

---

## Implementation Notes

- **DFS Complexity**: O(V) where V is number of nodes
- **BFS Complexity**: O(V) where V is number of nodes
- **Recursive BFS**: Not recommended due to stack overflow risk and inefficiency
- **Recursive DFS**: Recommended because naturally follows tree structure

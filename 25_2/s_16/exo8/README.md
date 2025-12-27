# Exercise 8: Advanced Graph Algorithms

## Quick Start

```bash
javac exo_8/*.java
java exo_8.Main
```

---

## Overview

| Component | Description |
|-----------|-------------|
| **SCCAlgorithms.java** | Strongly connected components |
| **EulerTour.java** | Euler tour |
| **TopologicalSort.java** | Topological sort |
| **Main.java** | Main program |

---

## Algorithm Specification

### Algorithm Types

| Algorithm | Type | Complexity | Description |
|-----------|------|------------|-------------|
| `reverseGraph` | Graph operation | O(V+E) | Reverse all edge directions |
| `kosarajuSCC` | SCC finding | O(V+E) | Find strongly connected components |
| `findEulerTour` | Path finding | O(E) | Find Euler tour if exists |
| `topologicalSort` | Ordering | O(V+E) | Topological ordering of vertices |

### Access Pattern
```
SCC:        DFS → Reverse → DFS
Euler Tour: Check degrees → Find cycles → Merge
Topo Sort:  Calculate in-degrees → Process queue
```

---

## Algorithm Examples

### Example 1: Strongly Connected Components

**Input Graph G:**
```
A → B → C
    ↓   ↑
    D   └───┘
    ↓
    E
```

**Strongly Connected Components:**
- {A, B, C} - cycle (mutually reachable)
- {D} - separate vertex
- {E} - separate vertex

**Algorithm Steps:**
1. DFS on original graph → fill stack
2. Reverse graph → create G^T
3. DFS on reversed graph → find SCCs

### Example 2: Euler Tour

**Graph:**
```
A → B → C → A
```

**Condition:** in-degree(v) = out-degree(v) for all v

**Euler Tour:** `A → B → C → A`

**Algorithm:** Hierholzer's method - find cycles and merge

### Example 3: Topological Sort

**Dependencies:**
```
A → B, A → C
B → C, B → D
C → E
D → E, D → F
G → F, G → E
```

**Structure:**
```
    A
   / \
  B   C
 / \   \
C   D   E
||   |\ /
E   E F
    | |
    F G
```

**Topological Order (starting from A):**
```
A → B → C → D → G → E → F
```

---

## Implementation Notes

- **Graph Reversal**: O(V+E) - go through all vertices and edges once
- **Kosaraju SCC**: O(V+E) - two DFS traversals
- **Euler Tour**: O(E) - Hierholzer algorithm (merge cycles)
- **Topological Sort**: O(V+E) - Kahn's algorithm (queue-based)

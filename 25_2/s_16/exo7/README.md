# Exercise 7: Graph Operations & Clique Finding

## Quick Start

```bash
javac exo_7/*.java
java exo_7.Main
```

---

## Overview

| Component | Description |
|-----------|-------------|
| **GraphOperations.java** | Graph operations |
| **Main.java** | Main program |

---

## Graph Operations Specification

### Operation Types

| Operation | Type | Complexity | Description |
|-----------|------|------------|-------------|
| `transposeGraph` | Directed | O(V+E) | Reverse all edge directions |
| `inverseGraph` | Undirected | O(V²) | Complement graph (edges that don't exist) |
| `bronKerbosch` | Undirected | Exponential | Find all maximal cliques |

### Access Pattern
```
Transpose: For each edge (u→v), create edge (v→u)
Inverse:   For each pair (u,v), add edge if not in original
Cliques:   Recursive backtracking with pruning
```

---

## Graph Examples

### Example 1: Graph Transpose

**Original Graph:**
```
A → B
↓   ↓
C → D
```

**Transposed Graph:**
```
A ← B
↑   ↑
C ← D
```

**Edge List:**
- Original: `A→B, A→C, B→D, C→D`
- Transposed: `A←B, A←C, B←D, C←D`

### Example 2: Graph Inverse

**Original Graph:**
```
A---B
|\ /|
| X |
|/ \|
C---D
```

**Inverse Graph:**
```
A   B
|   |
C---D
```

**Property:** Dense graph → Sparse inverse (and vice versa)

### Example 3: Maximal Cliques

**Graph:** V={A,B,C,D}, E={AB, AC, BC, CD}

**Structure:**
```
    A
   / \
  B---C
      |
      D
```

**Maximal Cliques:**
- {A, B, C} - triangle (maximum clique, size 3)
- {C, D} - edge (size 2)

---

## Implementation Notes

- **Transpose**: O(V+E) - iterate through all edges once
- **Inverse**: O(V²) - check all vertex pairs
- **Bron-Kerbosch**: Exponential in worst case, but efficient with pruning
- **Dual Graphs**: Only defined for planar graphs, require planar embedding

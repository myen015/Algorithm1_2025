# Exercise 5: CSC Graph Representation

## Quick Start

```bash
javac exo_5/*.java
java exo_5.Main
```

---

## Overview

| Component | Description |
|-----------|-------------|
| **CSCGraph.java** | CSC format operations |
| **Main.java** | Main program |

---

## CSC Format Specification

### Data Structure

| Field | Purpose | Example |
|-------|---------|---------|
| `colPointers` | Column boundaries | `[0, 2, 5, 8, 11, 12]` |
| `rowIndices` | Row positions | `[1, 2, 0, 2, 3, ...]` |
| `values` | Edge weights | `[1, 1, 1, ...]` (unweighted) |

### Access Pattern
```
For column i:
  Start: colPointers[i]
  End:   colPointers[i+1] - 1
  Rows:  rowIndices[start..end]
```

---

## Graph Examples

### Graph 1: Undirected Graph

**CSC Data:**
- `colPointers`: `[0, 2, 5, 8, 11, 12]`
- `rowIndices`: `[1, 2, 0, 2, 3, 0, 1, 3, 1, 2, 4, 3]`

**Edge List:**
```
A-B, A-C, B-C, B-D, C-D, D-E
```

**Structure:**
```
    A
   / \
  B---C
  |   |
  D---E
```

### Graph 2: Directed Graph

**CSC Data:**
- `colPointers`: `[0, 0, 2, 4, 5, 7]`
- `rowIndices`: `[0, 3, 0, 1, 2, 1, 3]`

**Edge List:**
```
B→A, B→D, C→A, C→B, D→C, E→B, E→D
```

**Structure:**
```
    A ← B
    ↑   ↓
    C → D ← E
    ↑   ↑
    └───┘
```

**Cycle Detected:** `D → C → B → D`

---

## Implementation Notes

- **Time Complexity**: O(V+E) for conversion
- **Space Complexity**: O(V+E) for CSC storage
- **Cycle Detection**: DFS-based algorithm

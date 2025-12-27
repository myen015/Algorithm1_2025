# Exercise 10: Complexity, Bayes, Entropy

---

## Overview

| Topic | Description |
|-------|-------------|
| **Problem 1** | Complexity classification (P, NP, NP-complete, etc.) |
| **Problem 2** | Bayes' theorem application |
| **Problem 3** | Shannon entropy calculation |

---

## Problem 1: Complexity Classification

### Complexity Classes

| Class | Description | Examples |
|-------|-------------|----------|
| **P** | Polynomial time, can solve efficiently | Sorting, BFS, DFS, Dijkstra |
| **NP** | Can verify solution in polynomial time | Factoring, cryptography |
| **NP-complete** | Hardest in NP, no poly-time algorithm | Sudoku, 3-coloring, TSP (decision) |
| **NP-hard** | At least as hard as NP-complete | TSP (optimization), Clique |
| **Undecidable** | Cannot be solved by any algorithm | Halting Problem, Busy Beaver |

### Classifications

**P:**
- Find max, linear search
- Shortest path (unweighted)
- Matrix multiplication
- Sorting, BFS, DFS, Dijkstra (non-negative)

**NP-complete:**
- Sudoku
- 3-coloring
- Scheduling with conflicts
- TSP (decision version)
- Hamiltonian Cycle (decision)
- Clique (decision)

**NP (intermediate):**
- Factoring large integers
- Cryptography problems

**Undecidable:**
- Halting Problem
- Busy Beaver

---

## Problem 2: Bayes' Theorem

### Problem Setup

- Disease prevalence: 0.1% (1 in 1000)
- Test accuracy: 99% (sensitivity and specificity)
- Patient tests positive
- **Question:** P(disease | positive test) = ?

### Solution

**Given:**
- P(D) = 0.001
- P(no D) = 0.999
- P(+|D) = 0.99
- P(+|no D) = 0.01

**Step 1: Find P(positive)**
```
P(+) = P(+|D)×P(D) + P(+|no D)×P(no D)
P(+) = 0.99×0.001 + 0.01×0.999
P(+) = 0.00099 + 0.00999 = 0.01098
```

**Step 2: Apply Bayes**
```
P(D|+) = P(+|D) × P(D) / P(+)
P(D|+) = (0.99 × 0.001) / 0.01098
P(D|+) ≈ 0.09 = 9%
```

### Intuitive Check

Out of 1000 people:
- 1 actually sick → 1 true positive
- 999 healthy → ~10 false positives
- Total positives: ~11
- Probability = 1/11 ≈ 9%

**Key insight:** Base rate fallacy - rare disease + accurate test still gives mostly false positives.

---

## Problem 3: Shannon Entropy

### Formula

H(X) = -Σ p_i × log₂(p_i)

### Three Coins

**Coin A: Fair (50/50)**
```
H = -0.5×log₂(0.5) - 0.5×log₂(0.5)
H = -0.5×(-1) - 0.5×(-1) = 1.0 bit
```

**Coin B: 99% heads**
```
H = -0.99×log₂(0.99) - 0.01×log₂(0.01)
H ≈ 0.08 bits
```

**Coin C: 1% heads**
```
H ≈ 0.08 bits (symmetric to B)
```

### Why Fair Coin = 1 Bit?

- Maximum uncertainty (can't predict)
- Each flip = 1 bit of information
- Need 1 binary digit to encode

### Why Biased Coin = 0.08 Bits?

- Almost predictable (99% heads)
- Learning heads gives little new info
- Only rare outcome is surprising
- Can compress efficiently

### Key Concept

**Entropy = uncertainty = information content**
- High entropy → high uncertainty → more info
- Low entropy → low uncertainty → less info
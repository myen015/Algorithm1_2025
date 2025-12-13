# Exercise 10

---

## Problem 1: Complexity Classes (4 pts)

Need to classify problems: P, NP, NP-complete, NP-hard, or Undecidable

**Group 1:**
- Find max, linear search, shortest path (unweighted), matrix multiplication
- All in P - polynomial time

**Group 2:**
- Sorting, Dijkstra (non-negative), BFS, DFS, merge sort, quicksort
- Also P - polynomial time

**Group 3:**
- Sudoku
- NP-complete

**Group 4:**
- 3-coloring, scheduling with conflicts
- NP-complete

**Group 5:**
- TSP, Hamiltonian Cycle, Clique
- NP-hard / NP-complete (decision version is NP-complete)

**Group 6:**
- Cryptography, factoring
- NP (but not NP-complete, NP-intermediate)

**Group 7:**
- Halting Problem, Busy Beaver
- Undecidable - can't solve at all

**Why:**
- P = can solve in polynomial time
- NP = can verify solution in polynomial time
- NP-complete = hardest in NP, no poly-time algorithm known
- NP-hard = at least as hard as NP-complete
- Undecidable = impossible to solve

---

## Problem 2: Bayes' Theorem (3 pts)

**Given:**
- Disease: 0.1% of people (1 in 1000)
- Test: 99% accurate (sensitivity and specificity both 99%)
- Patient tests positive
- **Find:** P(has disease | positive test)

**Answer: ~9%**

**Solution:**

Bayes formula:
P(D|+) = P(+|D) × P(D) / P(+)

Given:
- P(D) = 0.001
- P(no D) = 0.999
- P(+|D) = 0.99
- P(+|no D) = 0.01

First find P(+):
P(+) = P(+|D)×P(D) + P(+|no D)×P(no D)
P(+) = 0.99×0.001 + 0.01×0.999
P(+) = 0.00099 + 0.00999 = 0.01098

Then:
P(D|+) = (0.99 × 0.001) / 0.01098
P(D|+) = 0.00099 / 0.01098 ≈ 0.09 = 9%

**Intuition with 1000 people:**
- 1 actually sick → ~1 true positive
- 999 healthy → ~10 false positives
- Total positives: ~11
- So P = 1/11 ≈ 9%

**Key point:** Even 99% accurate test gives mostly false positives when disease is rare. This is base rate fallacy.

---

## Problem 3: Shannon Entropy (3 pts)

**Formula:**
H(X) = -Σ p_i × log₂(p_i)

For coin: n=2 (heads/tails)

**Three coins:**

**Coin A: fair (50/50)**
H = -0.5×log₂(0.5) - 0.5×log₂(0.5)
H = -0.5×(-1) - 0.5×(-1) = 0.5 + 0.5 = 1.0 bit

**Coin B: 99% heads**
H = -0.99×log₂(0.99) - 0.01×log₂(0.01)
H ≈ -0.99×(-0.0145) - 0.01×(-6.644)
H ≈ 0.0144 + 0.0664 ≈ 0.08 bits

**Coin C: 1% heads**
Same as B, H ≈ 0.08 bits (symmetric)

**Why fair coin = 1 bit?**
- Maximum uncertainty (can't predict)
- Each flip gives 1 bit info
- Need exactly 1 binary digit to encode

**Why 99% coin = 0.08 bits?**
- Almost always predictable (99% heads)
- Learning heads tells you nothing new
- Only rare tails (1%) is surprising, but happens rarely
- Can compress many flips with few bits

**Main idea:**
- High entropy = high uncertainty = more info
- Low entropy = low uncertainty = less info
- Predictable = less information
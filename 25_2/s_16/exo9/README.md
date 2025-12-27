# Exercise 9: Boolean Functions & Circuit Theory

Theoretical exercise - mathematical proofs only, no code required. 

---

## Problem 1: Finite Function Counting (3/10 pts)

### Statement

For function F: {0,1}^n → output_set, show the number of possible functions:

| Output Set | Number of Functions |
|------------|-------------------|
| {0,1} | 2^(2^n) |
| {-1,0,1} | 3^(2^n) |
| {0,1}^m | 2^(m·2^n) |

### Proof Using Decision Tree Model

**Step 1: Count Input Combinations**
- For n boolean variables, there are 2^n possible input combinations
- Each input combination corresponds to one leaf in the decision tree

**Step 2: Count Output Choices**
- For each input combination, we can choose any value from the output set
- If output set has size k, each leaf can be labeled with k different values

**Step 3: Total Function Count**
- Number of functions = (number of ways to label all leaves)
- Since there are 2^n leaves, and each can be labeled in k ways:
  - **Total functions = k^(2^n)**

**Detailed Proof:**

**Case 1: Output = {0,1}**
- Input combinations: 2^n
- Output choices per input: 2
- Total functions: 2 × 2 × ... × 2 (2^n times) = 2^(2^n) ✓

**Case 2: Output = {-1,0,1}**
- Input combinations: 2^n
- Output choices per input: 3
- Total functions: 3 × 3 × ... × 3 (2^n times) = 3^(2^n) ✓

**Case 3: Output = {0,1}^m**
- Input combinations: 2^n
- Output choices per input: 2^m (each output is m bits)
- Total functions: (2^m) × (2^m) × ... × (2^m) (2^n times) = (2^m)^(2^n) = 2^(m·2^n) ✓

### Decision Tree Visualization

**Example: n=2, output={0,1}**

```
        Root
      /      \
    x1=0     x1=1
   /    \    /    \
 x2=0  x2=1 x2=0  x2=1
  |     |    |     |
  ?     ?    ?     ?  (each ? can be 0 or 1)
```

- Leaves: 2^2 = 4
- Each leaf: 2 choices (0 or 1)
- Total functions: 2^4 = 16

---

## Problem 2: NAND Universality (4/10 pts)

### NAND Truth Table

| A | B | A↑B (NAND) |
|---|---|------------|
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

### Circuit Constructions

#### 1. NOT from NAND

**Formula:** NOT(A) = A NAND A

**Circuit Diagram:**
```
    A ──┐
        │
        ├─→ [NAND] ──→ NOT(A)
        │
    A ──┘
```

**Verification:**
- A=0: 0 NAND 0 = 1 = NOT(0) ✓
- A=1: 1 NAND 1 = 0 = NOT(1) ✓

**Gates:** 1 NAND gate

---

#### 2. AND from NAND

**Formula:** AND(A,B) = (A NAND B) NAND (A NAND B)

**Circuit Diagram:**
```
    A ──┐
        ├─→ [NAND] ──┐
    B ──┘            │
                     ├─→ [NAND] ──→ AND(A,B)
    A ──┐            │
        ├─→ [NAND] ──┘
    B ──┘
```

**Step-by-step:**
1. Compute A NAND B (first NAND gate)
2. Feed result to both inputs of second NAND gate
3. Output: NOT(A NAND B) = AND(A,B)

**Verification:**
- A=0, B=0: (0↑0)↑(0↑0) = 1↑1 = 0 = AND(0,0) ✓
- A=0, B=1: (0↑1)↑(0↑1) = 1↑1 = 0 = AND(0,1) ✓
- A=1, B=0: (1↑0)↑(1↑0) = 1↑1 = 0 = AND(1,0) ✓
- A=1, B=1: (1↑1)↑(1↑1) = 0↑0 = 1 = AND(1,1) ✓

**Gates:** 2 NAND gates

---

#### 3. OR from NAND

**Formula:** OR(A,B) = (A NAND A) NAND (B NAND B)

**Circuit Diagram:**
```
    A ──┐
        ├─→ [NAND] ──┐
    A ──┘            │
                     ├─→ [NAND] ──→ OR(A,B)
    B ──┐            │
        ├─→ [NAND] ──┘
    B ──┘
```

**Step-by-step:**
1. Compute NOT(A) = A NAND A (first NAND gate)
2. Compute NOT(B) = B NAND B (second NAND gate)
3. Compute NOT(A) NAND NOT(B) = OR(A,B) (third NAND gate)

**Verification:**
- A=0, B=0: (0↑0)↑(0↑0) = 1↑1 = 0 = OR(0,0) ✓
- A=0, B=1: (0↑0)↑(1↑1) = 1↑0 = 1 = OR(0,1) ✓
- A=1, B=0: (1↑1)↑(0↑0) = 0↑1 = 1 = OR(1,0) ✓
- A=1, B=1: (1↑1)↑(1↑1) = 0↑0 = 1 = OR(1,1) ✓

**Gates:** 3 NAND gates

---

### Theorem: NAND Universality

**Statement:** NAND is a universal operation. For each circuit C of n components, there is a NAND-equivalent circuit using at most 3n components.

**Proof:**

1. **Complete Basis:** The set {NOT, AND, OR} forms a complete basis for boolean circuits
   - Any boolean function can be expressed using only NOT, AND, and OR gates

2. **NAND Constructions:**
   - NOT: 1 NAND gate (Lemma 1)
   - AND: 2 NAND gates (Lemma 2)
   - OR: 3 NAND gates (Lemma 3)

3. **Replacement Strategy:**
   - Replace each NOT gate with 1 NAND gate
   - Replace each AND gate with 2 NAND gates
   - Replace each OR gate with 3 NAND gates

4. **Worst Case Analysis:**
   - Maximum gates needed: 3 per original gate (for OR)
   - For circuit with n components: at most 3n NAND gates

**Conclusion:** Any boolean circuit C with n components has a NAND-equivalent circuit using at most 3n NAND gates. ∎

---

## Problem 3: Universality of Boolean Circuits (3/10 pts)

### Delta Function Definition

For target x ∈ {0,1}^n, define:

```
δ_x(y) = { 1  if y = x
         { 0  otherwise
```

### Circuit Construction for δ_x

**Goal:** Build a circuit that outputs 1 if and only if input y equals target x.

**Step-by-step Construction:**

1. **Equality Checks:**
   - For each bit position i (i = 1 to n):
     - Check if y[i] == x[i]
     - This requires: y[i] if x[i]=1, or NOT(y[i]) if x[i]=0
     - Each check: O(1) gates

2. **Combine Checks:**
   - AND all n equality checks together
   - Output is 1 only if all checks pass (i.e., y = x)
   - AND of n inputs: O(n) gates

**Total Circuit Size:** O(1) × n + O(n) = O(n) gates

**Detailed Circuit Structure:**
```
y[1] ──→ [Check if y[1]==x[1]] ──┐
y[2] ──→ [Check if y[2]==x[2]] ──┤
  ...                             ├─→ [AND] ──→ δ_x(y)
y[n] ──→ [Check if y[n]==x[n]] ──┘
```

Each check: If x[i]=1, pass y[i]; if x[i]=0, pass NOT(y[i]). Then AND all results.

---

### Universal Circuit Theorem

**Statement:** Any function F: {0,1}^n → {0,1} can be computed by a circuit of size O(n·2^n).

**Proof:**

**Step 1: Decomposition**
For any input x ∈ {0,1}^n:
```
F(x) = Σ_{y ∈ {0,1}^n} F(y) · δ_y(x)
```

**Explanation:**
- For each possible input y, δ_y(x) = 1 only if x = y
- F(y) · δ_y(x) contributes F(y) to the sum when x = y, and 0 otherwise
- The sum equals F(x) because only one term (when y = x) is non-zero

**Step 2: Circuit Construction**

1. **Build δ_y circuits:**
   - For each y ∈ {0,1}^n, build circuit for δ_y
   - Number of such circuits: 2^n
   - Size of each circuit: O(n) gates (from previous construction)
   - Total for all δ_y: 2^n × O(n) = O(n·2^n) gates

2. **Combine with OR gates:**
   - For each y where F(y) = 1, include δ_y in the OR
   - Maximum OR gates needed: 2^n (one per possible input)
   - Total OR gates: O(2^n)

**Step 3: Total Size**
- δ_y circuits: O(n·2^n) gates
- OR combination: O(2^n) gates
- **Total: O(n·2^n) + O(2^n) = O(n·2^n) gates**

**Conclusion:** Any boolean function F: {0,1}^n → {0,1} is computable by a circuit of size O(n·2^n). ∎

---

## Summary

| Problem | Solution |
|---------|----------|
| **Problem 1** | Proof using decision tree model: k^(2^n) functions for output size k |
| **Problem 2** | Three circuit constructions + universality theorem (≤3n NAND gates) |
| **Problem 3** | δ_x circuit (O(n)) + universal circuit (O(n·2^n)) |
# Problem Set #9  
Fundamental Algorithm Techniques  

---

## Problem 1 — Finite Functions on {0,1}ⁿ

We consider finite functions  
F : {0,1}ⁿ → {0,1}ᵐ.

### 1. Number of functions {0,1}ⁿ → {0,1}
A function from an n-bit input has 2ⁿ possible inputs.  
For each input we choose an output bit ∈ {0,1}.  
So the total number of such functions is:

**2^(2ⁿ)**.

### 2. Number of functions {0,1}ⁿ → {−1,0,1}
Now each input has 3 choices instead of 2, for 2ⁿ inputs:

**3^(2ⁿ)**.

### 3. Number of functions {0,1}ⁿ → {0,1}ᵐ
Each output is an m-bit vector. That means each input has 2ᵐ choices.  
Total number of functions:

**(2ᵐ)^(2ⁿ) = 2^(m·2ⁿ)**.

These results follow simply from “number of inputs × number of choices per input”.  
To visualize this, one can imagine a decision-tree with 2ⁿ leaves (each leaf is one input), and each leaf gets an m-bit label.

---

## Problem 2 — NAND Equivalent to AND, OR, NOT

We are given the NAND truth-table. Using it we can reconstruct all basic gates.

### NOT from NAND  
NOT(x) = NAND(x, x)

### AND from NAND  
AND(x, y) = NOT(NAND(x, y)) = NAND(NAND(x, y), NAND(x, y))

### OR from NAND  
Using De Morgan:  
x OR y = NOT(NOT x AND NOT y)

So:  
OR(x, y) = NAND(NOT(x), NOT(y))

This shows that NAND is universal.  
Any circuit with n gates can be rewritten using at most 3n NAND gates.

Below is the small helper code used for this part:

```python
def NAND(a, b):
    return 0 if (a and b) else 1

def NOT(x):
    return NAND(x, x)

def AND(a, b):
    t = NAND(a, b)
    return NAND(t, t)

def OR(a, b):
    return NAND(NOT(a), NOT(b))

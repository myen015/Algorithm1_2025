# Fundamental Algorithm Techniques — Problem Set #3

## Overview

This repository contains solutions for **Problem Set #3** of the course *Fundamental Algorithm Techniques*.

### 📅 Due Date
**October 25, 2025**

---

## 🧮 Problem 1 — Fibonacci Super Fast!

We compute Fibonacci numbers using **matrix exponentiation**:

$$
\begin{bmatrix}
F_{n+1} \\
F_n
\end{bmatrix}
=
\begin{bmatrix}
1 & 1 \\
1 & 0
\end{bmatrix}^{n}
\begin{bmatrix}
1 \\
0
\end{bmatrix}
$$

This approach runs in **O(log n)** time complexity, proven using the **Master Theorem**.

The code also plots:
- Fibonacci numbers for small `n`
- Execution time vs input size

---

## 🎒 Problem 2 — 0/1 Knapsack Algorithm!

Implemented using **Dynamic Programming** (DP).  
- Shows why **Greedy** algorithms fail for this problem  
- Demonstrates DP table computation  
- Retrieves chosen items for optimal value  
- Includes a visualization of item values

Space complexity can be reduced to **O(W)** by using a **1D DP array**.

---

## 🧠 Problem 3 — Neuro Computing!

Generates random **binary vectors** and computes two similarity measures:

- **Dot-product–based similarity**
- **Jaccard similarity**

Then plots their distributions for different vector sizes (`N = 50, 200, 1000`), showing that similarity scores tend toward a **Gaussian-like** shape as `N` increases.

Additionally, sparse vectors (`N = 2000`, `w = 5`) are analyzed to calculate the number of possible combinations and their similarity distribution.

---

## 📊 Dependencies

```bash
pip install numpy matplotlib
```

---

## ▶️ Run Instructions

Run the script directly:

```bash
python exo3.py
```

---

## 📈 Output

- Fibonacci growth plots
- Knapsack value bars
- Similarity histograms (dense and sparse vectors)

---

**Author:** Your Name  
**Course:** Fundamental Algorithm Techniques  
**Date:** October 2025

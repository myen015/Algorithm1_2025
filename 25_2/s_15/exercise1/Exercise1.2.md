Exercise 1.2 — Recursive Multiplication and Karatsuba Algorithm

We want to multiply two large integers using recursion. We first implement a naïve divide-and-conquer multiplication, then improve it using the **Karatsuba** trick. Example:
a = 123456
b = 789123

We split each number into two halves:
a = a₀·10^(n/2) + a₁
b = b₀·10^(n/2) + b₁

We compute:
a·b = a₀b₀·10^n + (a₀b₁ + a₁b₀)·10^(n/2) + a₁b₁

This requires **4 recursive sub-multiplications**:
T(n) = 4T(n/2) + O(n)

By the Master Theorem:
log₂(4) = 2  →  T(n) = O(n²)

Karatsuba Improvement
Karatsuba uses the identity:
(a₀ + a₁)(b₀ + b₁) = a₀b₀ + a₁b₁ + a₀b₁ + a₁b₀
Instead of 4 multiplications, we compute only 3:
p₁ = a₀b₀
yp₂ = a₁b₁
p₃ = (a₀ + a₁)(b₀ + b₁)

a·b = p₁·10^n + (p₃ − p₁ − p₂)·10^(n/2) + p₂

Now:
T(n) = 3T(n/2) + O(n)
log₂(3) ≈ 1.585  →  T(n) = O(n^1.585)
This is asymptotically **faster than O(n²)**.

---
 Final Comparison Table

| Method | Multiplications | Recurrence | Complexity |
|---------|----------------|------------|------------|
| Classical | 4 | `T(n)=4T(n/2)+O(n)` | `O(n²)` |
| Karatsuba | 3 | `T(n)=3T(n/2)+O(n)` | `O(n^log₂3)` ≈ `O(n^1.585)` |

---

Conclusion
Karatsuba reduces the number of recursive calls and therefore improves the time complexity. For very large numbers, Karatsuba is significantly faster than the classical divide-and-conquer multiplication algorithm.


## 1. Purpose
This program simulates a collection of random binary vectors and computes **pairwise similarity measures** between them.  
The goal is to observe how the distribution of cosine and Jaccard similarity changes as the vector dimensionality `N` increases.

This experiment illustrates the phenomenon known as **concentration of measure** — in high-dimensional spaces, random vectors tend to become statistically similar to one another.

---

## 2. Concept Overview
The program generates `M` random binary vectors of length `N`, where each element is `0` or `1` with equal probability (Bernoulli(0.5)).  
Then, for every pair of vectors `(i, j)`, it calculates:

1. **Cosine similarity**  
   Measures how aligned two vectors are:
   \[
   \text{cosine}(A, B) = \frac{|A \cap B|}{\sqrt{|A| \cdot |B|}}
   \]

2. **Jaccard similarity**  
   Measures the ratio of intersection to union:
   \[
   J(A, B) = \frac{|A \cap B|}{|A \cup B|}
   \]

---

## 3. Code Structure
| Function | Description |
|-----------|--------------|
| `gen(M, N)` | Generates `M` random binary vectors of length `N`. |
| `cosine(a, b)` | Computes cosine similarity between vectors `a` and `b`. |
| `jaccard(a, b)` | Computes the Jaccard index between `a` and `b`. |
| `mean_std(vals)` | Computes the mean and standard deviation (population std). |
| `run(M, N)` | Runs one experiment and prints summary statistics. |

The main section (`if __name__ == "__main__":`) runs three tests with `N = 100`, `500`, and `1000`.

---

## 4. How to Run
```bash
python3 neuro_sim.py
```

Example output:
```
N=100, pairs=4950
Cosine   mean=0.5013 std=0.0512
Jaccard  mean=0.3345 std=0.0431
```

---

## 5. Result Interpretation
- For **small N**, similarity values are widely spread.  
- For **large N**, the mean stays nearly constant while the standard deviation shrinks — random vectors become **more similar on average**.  
  This demonstrates the **concentration of measure** effect.

---

## 6. Computational Complexity
- **Time:** `O(M² * N)` — every pair of vectors is compared across `N` elements.  
- **Space:** `O(M * N)` — for storing the binary matrix.

---

## 7. Possible Improvements
- **Performance:** Use `NumPy` for vectorized operations.  
- **Memory efficiency:** Compute statistics on the fly instead of storing all pairwise values.  
- **Visualization:** Plot histograms of cosine and Jaccard distributions.  
- **CLI parameters:** Allow users to set `M`, `N`, and random seed via command-line arguments.

---

## 8. Example Extension
Adding a quick visualization:

```python
import matplotlib.pyplot as plt
plt.hist(cos, bins=30, alpha=0.6, label='Cosine')
plt.hist(jac, bins=30, alpha=0.6, label='Jaccard')
plt.legend()
plt.title(f"N={N}, M={M}")
plt.show()
```

---

## 9. Summary
This program illustrates how random binary vectors behave in high-dimensional spaces and how their similarity distributions evolve.  
Such analysis helps understand foundational principles behind neural networks, clustering, and other algorithms based on vector similarity.

---

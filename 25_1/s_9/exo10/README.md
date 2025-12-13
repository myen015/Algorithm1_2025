### Problem 1: Classification of Problems

```
{Problem Group} ->[Classification]

{find max, linear search, shortest path in unweighted graph, matrix multiplication} ->[P]

{sorting of list, Dijkstra on non-negative weights, BFS, DFS, merge sort, quicksort} ->[P]

{sudoku} -> [NP-complete]

{3 coloring of graph, scheduling with conflicts} ->	[NP-complete]

{Traveling Salesperson Problem, Hamiltonian Cycle, Clique} -> [NP-complete]

{Cryptography, factoring large integers} -> [NP]

{Halting Problem, busy beaver} -> [	NP-hard]
```

### Problem 2: Bayes' Theorem

*Given:*

* Disease prevalence = 0.1% = 0.001

* Test accuracy = 99% (sensitivity and specificity)

* P(positive│disease) = 0.99

* P(negative│no disease) = 0.99 → P(positive│no disease) = 0.01

Calculation: P(disease│positive) = (0.99 × 0.001) / (0.99×0 001 + 0.01×0.999) = 0.00099 / 0.01098 ≈ 0.09016 ≈ 9% (*code in **calculation.py file***) 

The probability is approximately *9%* **because even with a 99% accurate test, the disease is extremely rare (0.1% prevalence).** This means the number of false positives from the large healthy population *outweighs the true positives from the small diseased population.*

Mathematical Derivation:
```
Let D = has disease, T+ = tests positive.
Given:
1) P(D)=0.001
2) P(T+∣D)=0.99 (sensitivity)
3) P(T−∣¬D)=0.99 (specificity) → P(T+∣¬D)=0.01

Using Bayes' Theorem:
P(D∣T+) = (P(T+)P(T+∣D)⋅P(D))/P(T+)

P(T+) = P(T+∣D)P(D)+P(T+∣¬D)P(¬D)=(0.99)(0.001)+(0.01)(0.999)=0.01098

P(D∣T+) = 0.01098/0.00099 = 0.09016% = 9%
```


### Problem 3: Shannon Entropy

*Formula:*
```
H(X) = -Σ pᵢ log₂(pᵢ)
```
where p is the probability of heads.

### Calculations for Each Coin:

*Coin A: p=0.5* 

* H(A)=−0.5log2(0.5)−0.5log2(0.5)

* log2(0.5)=−1

* H(A)=−0.5(−1)−0.5(−1)=0.5+0.5=1 bit

*Coin B: p=0.99*

* H(B)=−0.99log2(0.99)−0.01log2​(0.01) 

* log2(0.99)≈−0.0145, log2(0.01)≈−6.6439

* H(B)=−0.99(−0.0145)−0.01(−6.6439)=0.014355+0.066439≈0 0808 bits

*Coin C: p=0.01*

* H(C)=−0.01log2(0.01)−0.99log2(0.99)

This is symmetric to Coin B, so:
```
H(C)≈0.0808 bits
```

**Why the Difference?**

* Fair coin (50%): Maximum uncertainty, each flip provides 1 bit of information.

- Biased coin (99%): Highly predictable, low uncertainty, requires minimal bits to describe.

- This shows that entropy measures average information content per symbol in optimal encoding.



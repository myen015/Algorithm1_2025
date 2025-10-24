*Problem1 Fibonacci*
Question:
Use Master Theorem to discuss the complexity of this decomposition and show, explain why time complexity is then log₂(n).

**Answer:**
When computing Fibonacci numbers with matrix exponentiation, we repeatedly divide the power n by 2.
Each step performs one or two constant-time 2×2 matrix multiplications.
Therefore the recurrence relation for the running time is:

**𝑇(𝑛)=𝑇(𝑛/2)+𝑂(1)**

Here we have one recursive subproblem of size n/2 (𝑎=1, 𝑏=2) and a constant amount of extra work (𝑓(𝑛)=𝑂(1)).
According to the Master Theorem, since

𝑛log𝑏𝑎=𝑛log21=𝑛0=1 nlogb
	​
and f(n)=O(1)=O(nlogba),
it follows that:

𝑇(𝑛)=𝑂(log𝑛)


Thus the time complexity of computing 𝐹𝑛 using matrix exponentiation (either [1,1;1,0]𝑛 or 
[2,1;1,1]𝑛/2) is logarithmic in n, i.e. O(log₂ n).



*Problem 2 — 0/1 Knapsack*

**Why not Greedy?**

Greedy doesn’t work because picking the most valuable or lightest item first doesn’t always give the best total.
Choices affect each other, so we need to check combinations → use **Dynamic Programming**.


We use DP to find the best value for each possible weight.
Formula:
[dp[w] = \max(dp[w],\ dp[w - weight_i] + value_i)]
Example: weights = [2,3,4,5], values = [3,4,5,6], W = 5 → best value = **7**.


Use only one array `dp[W+1]` and loop backward.
Space becomes **O(W)**.

*Problem 3 — Neuro Computing*

**Random Binary Vectors**

We create 100 random binary vectors of length N, for example:
`[1, 0, 0, 1, 0, 1, ...]`.
Each vector is just a set of zeros and ones, like neuron signals.


**Similarity Functions**

To see how similar two vectors are, we calculate a **similarity**.
There are two types:

* **sim(x, y)** — normal dot product divided by the number of ones.
* **Jaccard(x, y)** — number of positions where both have 1 divided by total number of ones in both.

When we calculate many pairs, the similarity values look like a **bell curve** (Gaussian distribution).


**When N gets larger**

If N becomes bigger, the random vectors become more different from each other.
Their similarity gets smaller and the distribution becomes narrower.


**Large and Sparse Vectors**

If we take a very large vector, for example N = 2000 with only 5 ones,
then the number of possible such vectors is huge:
C(2000, 5).
That shows how many different patterns can exist.


**5Capacity**

“Capacity” means how many different vectors (or patterns) can be stored
without mixing them up.
When vectors are long and sparse (few ones), the capacity becomes higher.


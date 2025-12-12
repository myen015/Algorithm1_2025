1. # Fibonacci
In the file problem.c computed Fibonacci with given relation. ime Complexity

The recurrence relation is:

𝑇(𝑛)=𝑇(𝑛/2)+𝑂(1)
T(n)=T(n/2)+O(1)

Solving with the Master Theorem ⇒ 
𝑇(𝑛)=𝑂(log𝑛)
T(n)=O(logn).

That’s why this method is called “Fibonacci Super Fast” — it grows logarithmically with 𝑛 instead of linearly or exponentially.


2. # Kpansack Algorithm
A greedy algorithm makes decisions based on the best local choice at each step, for example by selecting items with the highest value-to-weight ratio first.
While this works for the Fractional Knapsack Problem (where items can be divided), it fails for the 0/1 Knapsack Problem because partial items are not allowed.


3. # Vector
## For larger N 
Mean similarity ≈ 1/N, → 0 as N↑.
Distribution of similarity becomes narrow and Gaussian-like (Central Limit Theorem).

## Number of possible sparse vectors
    C(2000,5)=2.65335665×1014.

## Capacity idea:
    If each vector has w ones, expected overlap ≈ w2/N.
    To keep overlaps small, number of storable distinct random vectors ≈
    M ≈ sqrt(2N/w2)

    For N=2000, w=5 → M≈12 random independent vectors before collisions appear.
​

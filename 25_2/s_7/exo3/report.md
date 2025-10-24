Output:

=== PROBLEM 1: FIBONACCI ===

Testing Fibonacci computation:
F(0) = 0
F(1) = 1
F(2) = 1
F(3) = 2
F(4) = 3
F(5) = 5
F(6) = 8
F(7) = 13
F(8) = 21
F(9) = 34
F(10) = 55
F(11) = 89
F(12) = 144
F(13) = 233
F(14) = 377
F(15) = 610

=== FIBONACCI COMPLEXITY ANALYSIS ===

Master Theorem Analysis:
Recurrence: T(n) = T(n/2) + O(1)
This is because each recursive call:
  - Divides n by 2 (when n is even)
  - Performs O(1) matrix multiplication

Applying Master Theorem (Case 2):
  a = 1 (one recursive call)
  b = 2 (problem size halved)
  f(n) = O(1)
  log_b(a) = log_2(1) = 0
  Since f(n) = Θ(n^0) = Θ(1), we have Case 2
  Therefore: T(n) = Θ(log n)

Conclusion: Time complexity is O(log n)

=== PROBLEM 2: 0/1 KNAPSACK ALGORITHM ===

Course Example:
Weights: [ 2, 3, 4, 5 ]
Values: [ 3, 4, 5, 6 ]
Capacity: 8

Maximum value: 10
Maximum value (space-optimized): 10

=== KNAPSACK ALGORITHM ANALYSIS ===

1. Why is Knapsack NOT a greedy algorithm?
   - Greedy algorithms make locally optimal choices
   - In Knapsack, greedy by value/weight ratio fails:
   - Example: W=10, items: (w=6,v=30), (w=5,v=20), (w=4,v=20)
   - Greedy picks (6,30) first, can't fit both others
   - Optimal: (5,20) + (4,20) = 40 > 30

2. Why is it Dynamic Programming?
   - Has optimal substructure: optimal solution contains optimal subsolutions
   - Has overlapping subproblems: same subproblems computed multiple times
   - Decision for each item depends on ALL previous decisions

3. Time Complexity: O(n*W)
   - n items × W capacity states
   - This is pseudo-polynomial (depends on W value, not its bit length)

4. Space Complexity:
   - Standard DP: O(n*W)
   - Space-optimized: O(W) - using 1D array

=== PROBLEM 3: NEURO COMPUTING ===

1. Generating 100 random binary vectors of length N=100
   Generated 100 vectors
   Sample vector: [1, 0, 0, 1, 1, 0, 1, 0, 0, 1...]

2. Computing similarity functions:

Cosine Similarity Statistics:
  Mean: 0.4942
  Std Dev: 0.0656
  Min: 0.2162
  Max: 0.7259

Jaccard Similarity Statistics:
  Mean: 0.3293
  Std Dev: 0.0579
  Min: 0.1212
  Max: 0.5694

   Observation: Similarities distribute like a Gaussian!
   This is due to the Central Limit Theorem:
   - Each similarity is a sum/average of many binary comparisons
   - With large N, these sums converge to normal distribution

3. Repeating for larger N values:

  N=500 Statistics:
  Mean: 0.5043
  Std Dev: 0.0257
  Min: 0.4164
  Max: 0.5920
     Range: 0.1756

  N=1000 Statistics:
  Mean: 0.5007
  Std Dev: 0.0184
  Min: 0.4407
  Max: 0.5527
     Range: 0.1119

  N=2000 Statistics:
  Mean: 0.4992
  Std Dev: 0.0140
  Min: 0.4584
  Max: 0.5504
     Range: 0.0920

   Why? As N increases:
   - More bits to compare → more precise similarity estimates
   - Standard error decreases as ~1/√N
   - Distribution becomes tighter around the mean

4. Sparse binary vectors (N=2000, w=5 ones):
   Number of possible vectors: 2.65e+14
   This is C(2000,5) = 2000!/(5!*1995!)

5. Capacity of sparse binary vectors:
   Capacity = log₂(number of possible vectors)
   Capacity ≈ 47.91 bits

   Interpretation:
   - Each unique sparse vector can encode this many bits of information
   - High capacity despite sparsity (only 5 out of 2000 bits set)
   - Useful for: hash functions, neural network representations
   - Related to: compressed sensing, locality-sensitive hashing
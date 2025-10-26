NEURO COMPUTING - ANALYSIS

2. SIMILARITY FUNCTIONS

sim(x, y) = (x · y) / (||x||₁ × ||y||₁)

This is the dot product normalized by L1 norms. Measures correlation between vectors.

Jaccard(x, y) = |x ∩ y| / |x ∪ y|

Intersection divided by union. Measures overlap between sets represented as binary vectors.

Both distribute like Gaussian when computed across random vector pairs.

3. WHAT HAPPENS FOR LARGER N

Distribution becomes narrower (smaller standard deviation) around the mean.

Why: Central Limit Theorem. Similarity score is average of N independent random contributions. As N grows, variance decreases proportionally to 1/sqrt(N). The distribution concentrates around expected value.

4. SPARSE BINARY VECTORS N=2000, w=5

How many binary vectors of length 2000 with exactly 5 ones?

Answer: C(2000, 5) = 2000! / (5! × 1995!)

Calculation: (2000 × 1999 × 1998 × 1997 × 1996) / (5 × 4 × 3 × 2 × 1) ≈ 2.56 × 10^15

Massive number because we choose 5 positions from 2000 possible positions.

5. CAPACITY FOR BINARY VECTORS

Capacity = Hamming distance = number of positions where vectors differ

For sparse vectors with w=5 ones each, maximum Hamming distance between any two vectors is 10 (all 5 positions different in each).

Minimum is 0 (identical vectors).

Typical capacity = how many bits must change to transform one vector into another.

For dense random vectors, expected Hamming distance ≈ N/2 (half the positions differ).

Capacity concept relates to error correction: how many bit flips can network tolerate and still recover original pattern.

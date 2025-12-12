Problem 1 (Fibonacci Super Fast!).
To compute Fibonacci fast, we use a 2x2 matrix. Instead of multiplying the matrix n times, we repeatedly square the matrix. Each time we square it, the exponent becomes twice as large, so we reduce the problem size by half.
This means that instead of doing n steps, we only need to do about log₂(n) steps, because every step cuts n in half. The matrices are always 2×2, so each multiplication takes constant time.
Therefore, the total time is proportional to how many times you can divide n by 2, which is log₂(n). That is why the time complexity is O(log n).

Problem 2 (0/1 Knapsack Algorithm!). 
A. A greedy approach cannot be used for the 0/1 Knapsack problem because taking items based only on the highest value, lowest weight, or best value-to-weight ratio does not always produce the optimal total value. Some combinations of items that initially look less profitable may lead to a better final solution under the capacity limit.

B. The optimal way to solve this problem is by using Dynamic Programming, where we systematically build up the best possible value for every capacity from 0 to W using the available items.

C. The time complexity of this algorithm is O(n·W). The standard space complexity is also O(n·W), but it can be optimized to O(W) by storing only one row and updating it in reverse order.
Problem 3 (Neuro Computing!).

3. What happens for larger N and why?
As N increases, random vectors become almost orthogonal, and the similarity values concentrate around the mean. This happens due to the law of large numbers and high-dimensional effects.

4. How many such sparse vectors (N = 2000, w = 5)?
The number of possible binary vectors is:
𝐶(2000,5)≈2.67×10^15

This is extremely large.

5. Capacity

The capacity is defined by how many distinct patterns can be represented. For sparse binary vectors, the capacity is approximately equal to the combinatorial numberC(N,w), which is very high, meaning sparse coding allows storing a huge number of patterns with low overlap.
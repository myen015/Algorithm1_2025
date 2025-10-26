## Problem 1 — Fibonacci Super Fast (O(log n))

To compute the Fibonacci number efficiently, we use matrix exponentiation instead of slow recursion.

The classical recurrence is:

\[
F(n) = F(n-1) + F(n-2)
\]

Naive recursion has exponential time:

\[
O(2^n)
\]
Example: compute \(F(10)\)

\[
F(0)=0,\quad F(1)=1
\]

Then:

\[
F(2)=1,\;
F(3)=2,\;
F(4)=3,\;
F(5)=5,\;
F(6)=8,\;
F(7)=13,\;
F(8)=21,\;
F(9)=34,\;
F(10)=55
\]

So the final result is:

\[
F(10)=55
\]

Using matrix exponentiation, we reduce Fibonacci computation from:

| Method | Time |
|---------|------|
| naive recursion | \(O(2^n)\) |
| matrix fast power | \(O(\log n)\)|

The method is exponentially faster and allows computing very large Fibonacci numbers efficiently.

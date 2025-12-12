Problem 3 — Explanation

We consider a Boolean function:

F : \{0,1\}^n \rightarrow \{0,1\}

We want to explain why any such function can be computed by a circuit of size:

O(n \cdot 2^n)

⸻

Step 1: Every input x has a unique bitstring

There are 2^n possible inputs.
For each input x = (x_1, ..., x_n) we define:

\delta_x(y) =
\begin{cases}
1 & \text{if } y = x \\
0 & \text{otherwise}
\end{cases}

This is like a decoder, selecting exactly one input pattern.

A decoder of n bits can be built using O(n) gates.

⸻

Step 2: Reconstruct F using decoders

Since F maps input → output 0/1, write:

F(y) = \bigvee_{x : F(x)=1} \delta_x(y)

Meaning:
	•	For every input x such that F(x)=1
we activate its decoder δx
and OR them all together.

There are at most 2^n such decoders.
Each decoder uses O(n) gates.

Total circuit size:

O(n \cdot 2^n)

⸻

Final Statement

Any Boolean function
F : \{0,1\}^n \rightarrow \{0,1\}
can be computed using a circuit of size:

\boxed{O(n \cdot 2^n)}

Thus Boolean circuits are universal.

Problem 2 — Bayesian reasoning

A disease affects 0.1% of people:

P(D) = 0.001,\quad P(\neg D)=0.999

The test is 99% accurate:

P(\text{positive} \mid D)=0.99,\quad
P(\text{positive} \mid \neg D)=0.01

We want:

P(D \mid +)

Using Bayes Theorem:

P(D \mid +) = \frac{P(+ \mid D) P(D)}{P(+ \mid D)P(D) + P(+ \mid \neg D) P(\neg D)}

Substitute:

P(D \mid +) =
\frac{0.99 \cdot 0.001}
{0.99\cdot 0.001 + 0.01\cdot 0.999}

Compute:
	•	Numerator: 0.00099
	•	Denominator: 0.00099 + 0.00999 = 0.01098

P(D \mid +) ≈ 0.09016 = 9\%


Interpretation

Even with a very accurate test:
	•	The disease is extremely rare, so false positives dominate.
	•	Most positive tests come from healthy people.

Thus the probability the patient truly has the disease is only 9%, not 99%.



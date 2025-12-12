Problem 3 — Shannon Entropy of biased coins

Entropy formula:

H(X) = -\sum_i p_i \log_2 p_i

For a coin:

H = -p\log_2 p - (1-p)\log_2(1-p)

Coin A: P(heads) = 0.5 (fair coin)

H = -0.5\log_2 0.5 - 0.5\log_2 0.5 = 1 \text{ bit}

Surprise = medium (max uncertainty)


Coin B: P(heads) = 0.99 (almost always heads)

H ≈ -0.99\log_2 0.99 - 0.01\log_2 0.01 ≈ 0.08 \text{ bits}

Heads gives tiny surprise (expected result)


Coin C: P(heads) = 0.01 (rare heads)

H ≈ -0.01\log_2 0.01 - 0.99\log_2 0.99 ≈ 0.08 \text{ bits}

Heads gives HUGE surprise, but entropy same as coin B.


Why such small entropy?

Entropy measures average uncertainty, not the shock of rare events.
	•	Coin B: heads almost always → low uncertainty
	•	Coin C: tails almost always → low uncertainty

Both are highly predictable → ≈0.08 bits.

Why fair coin has 1 bit?

Because:
	•	Two outcomes equally likely
	•	Maximum uncertainty
	•	Need exactly 1 bit to encode the result



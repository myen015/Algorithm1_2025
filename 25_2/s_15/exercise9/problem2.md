Problem 2 — Solution

NAND (↑) is defined as:

A ↑ B = \text{NOT}(A \text{ AND } B)

Truth table:
A     B     A ↑ B
0     0     1
0     1     1
1     0     1
1     1     0


Constructing NOT with NAND

\text{NOT}(A) = A ↑ A

⸻

Constructing AND with NAND

A \text{ AND } B = \text{NOT}(A ↑ B) = (A ↑ B) ↑ (A ↑ B)

⸻

Constructing OR with NAND

Using De Morgan:

A \text{ OR } B = \text{NOT}( \text{NOT}(A) \text{ AND } \text{NOT}(B) )

So:

A \text{ OR } B = (A ↑ A) ↑ (B ↑ B)

Final formulas
|Logic gate|Formula using only NAND|
|NOT A     |A ↑ A                 |
|A AND B   |(A ↑ B) ↑ (A ↑ B)   |
|A OR B    |(A ↑ A) ↑ (B ↑ B)   |
These are linear 2- or 3-component circuits.




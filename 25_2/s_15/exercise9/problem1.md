Problem 1 — Explanation & Solution

A finite function on a computer is written as:

F : \{0,1\}^n \longrightarrow \{0,1\}^m

This means:
— There are 2ⁿ possible inputs (all binary strings of length n)
— Each input is mapped to one output.

We must show:

Number of all possible functions with output {0,1} is
2^{2^n}

Number of all possible functions with output {-1, 0, 1} is
3^{2^n}

Number of all possible functions with output {0,1}^m is
(2^m)^{2^n} = 2^{m \cdot 2^n}


 Reasoning

1. Output set = {0,1} → 2 choices per input

For each of the 2^n possible inputs, the function must choose output 0 or 1.
So total number of functions:

2^{(2^n)}

⸻

2. Output set = {–1, 0, 1} → 3 choices per input

Each input now has 3 possible outputs.
Total number of functions:

3^{(2^n)}

⸻

3. Output set = {0,1}^m → 2^m choices per input

Each output is m-bit binary vector.
So for each of the 2^n inputs we must pick 1 among 2^m outputs:

(2^m)^{2^n} = 2^{m \cdot 2^n}

⸻

Final Answer

|Output set | # of possible outputs per input |# of inputs |Total # of functions|
|{0,1}      |        2                        |      2^n   |      2^{2^n}       |
|{–1,0,1}   |        3                        |      2^n   |      3^{2^n}       |
|{–1,0,1}   |        3                        |      2^n   |      3^{2^n}       |




PS C:\Users\Asus\exo_9> python problem1_1_binary_output.py
problem count functions F: {0,1}^n -> {0,1}

  number inputs 2^1 = 2
  number functions 2^(2^1) = 2^2 = 4

n = 2:
  number inputs 2^2 = 4
  number functions 2^(2^2) = 2^4 = 16

n = 3:
  number inputs 2^3 = 8
  number functions 2^(2^3) = 2^8 = 256

n = 4:
  number inputs 2^4 = 16
  number functions 2^(2^4) = 2^16 = 65536

formula 2^(2^n)
PS C:\Users\Asus\exo_9> python problem1_2_ternary_output.py
problem count functions F: {0,1}^n -> {-1,0,1}

  number inputs: 2^1 = 2
  number functions: 3^(2^1) = 3^2 = 9

n = 2:
  number inputs: 2^2 = 4
  number functions: 3^(2^2) = 3^4 = 81

n = 3:
  number inputs: 2^3 = 8
  number functions: 3^(2^3) = 3^8 = 6561

n = 4:
  number inputs: 2^4 = 16
  number functions: 3^(2^4) = 3^16 = 43046721

formula: 3^(2^n)
PS C:\Users\Asus\exo_9> python problem1_3_multi_output.py
problem count functions F: {0,1}^n -> {0,1}^m

n = 1, m = 1:
  number inputs: 2^1 = 2
  number outputs: 2^1 = 2
  number functions: 2^(m*2^1) = 2^2 = 4

n = 1, m = 2:
  number inputs: 2^1 = 2
  number outputs: 2^2 = 4
  number functions: 2^(m*2^1) = 4^2 = 16

n = 1, m = 3:
  number inputs: 2^1 = 2
  number outputs: 2^3 = 8
  number functions: 2^(m*2^1) = 8^2 = 64

n = 2, m = 1:
  number inputs: 2^2 = 4
  number outputs: 2^1 = 2
  number functions: 2^(m*2^2) = 2^4 = 16

n = 2, m = 2:
  number inputs: 2^2 = 4
  number outputs: 2^2 = 4
  number functions: 2^(m*2^2) = 4^4 = 256

n = 2, m = 3:
  number inputs: 2^2 = 4
  number outputs: 2^3 = 8
  number functions: 2^(m*2^2) = 8^4 = 4096
n = 3, m = 1:
  number inputs: 2^3 = 8
  number outputs: 2^1 = 2
  number functions: 2^(m*2^3) = 2^8 = 256

n = 3, m = 2:
  number inputs: 2^3 = 8
  number outputs: 2^2 = 4
  number functions: 2^(m*2^3) = 4^8 = 65536

n = 3, m = 3:
  number inputs: 2^3 = 8
  number outputs: 2^3 = 8
  number functions: 2^(m*2^3) = 8^8 = 16777216

Formula: 2^(m * 2^n)
PS C:\Users\Asus\exo_9> python problem2_nand_gates.py
NAND truth table:
A B | A NAND B
0 0 |    1
0 1 |    1
1 0 |    1
1 1 |    0

==================================================
NOT from NAND:
NOT(A) = A NAND A

A | NOT A
0 |   1
1 |   0

==================================================
AND from NAND:
AND(A,B) = NOT(A NAND B) = (A NAND B) NAND (A NAND B)

A B | A AND B
0 0 |    0
0 1 |    0
1 0 |    0
1 1 |    1
==================================================
OR from NAND:
OR(A,B) = (NOT A) NAND (NOT B) = (A NAND A) NAND (B NAND B)

A B | A OR B
0 0 |   0
0 1 |   1
1 0 |   1
1 1 |   1

==================================================
Summary:
NOT(A) uses 1 NAND gate
AND(A,B) uses 2 NAND gates
OR(A,B) uses 3 NAND gates
total we can build any circuit with only NAND gates
PS C:\Users\Asus\exo_9> python problem3_boolean_circuits.py
problem Universality of Boolean Circuits
F: {0,1}^n -> {0,1}

n = 1:
  number possible inputs: 2^1 = 2
  gates per delta function: O(1) = ~2
  total gates needed: O(n * 2^n) = ~4

n = 2:
  number possible inputs: 2^2 = 4
  gates per delta function: O(2) = ~3
  total gates needed: O(n * 2^n) = ~12

n = 3:
  number possible inputs: 2^3 = 8
  gates per delta function: O(3) = ~4
  total gates needed: O(n * 2^n) = ~32

n = 4:
  number possible inputs: 2^4 = 16
  gates per delta function: O(4) = ~5
  total gates needed: O(n * 2^n) = ~80

n = 5:
  number possible inputs: 2^5 = 32
  gates per delta function: O(5) = ~6
  total gates needed: O(n * 2^n) = ~192

==================================================
example with n=2:

all possible inputs:
  x0 = [0, 0]
  x1 = [0, 1]
  x2 = [1, 0]
  x3 = [1, 1]

delta functions:
  delta_[0, 0](x) = 1 if x = [0, 0], else 0
  delta_[0, 1](x) = 1 if x = [0, 1], else 0
  delta_[1, 0](x) = 1 if x = [1, 0], else 0
  delta_[1, 1](x) = 1 if x = [1, 1], else 0

any function F can be written as:
F(x) = OR of all delta_x where F(x) = 1

circuit size:
  each delta: O(n) = O(2) gates
  total deltas: 2^n = 4
  total size: O(n * 2^n) = O(2 * 4) = O(8) gates
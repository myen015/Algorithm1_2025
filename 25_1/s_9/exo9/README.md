Problem Set #9 - Fundamental Algorithm Techniques

### Problem 1: Finite Function on the computer  

For a function 
F:{0,1}n⟶{0,1}m:

**Case 1: Output {0,1}**

* Domain size: 2n (number of possible inputs)

* For each input, output can be either 0 or 1 → 2 choices per input

Total functions: 2(pow2n) = 2(pow2n) 

pow means = power (sorry i can't write it)

### Case 2: Output {−1,0,1}

* Domain size: 2n
 
* For each input, output has 3 possible values

* Total functions: 3(2n) = 3(2n)

### Case 3: Output {0,1}m

* Domain size: 2n

* For each input, output is an m-bit string →2m possible outputs per input

* Total functions: (2m) * (2n)=2m * 2n

### Problem 2: Equivalence NAND ⇒ AND, OR & NOT

*Using NAND gate truth table:*

```
A	B	A↑B
0	0	1
0	1	1
1	0	1
1	1	0
```

1. NOT from NAND
```
NOT(A) = A ↑ A
```
2. AND from NAND
```
AND(A,B) = NOT(A ↑ B) = (A ↑ B) ↑ (A ↑ B)
```

3. OR from NAND (using De Morgan's law)
```
OR(A,B) = NOT(NOT(A) ∧ NOT(B)) = (A ↑ A) ↑ (B ↑ B)
```

### Problem 3: Universality of Boolean Circuits

For any function F:{0,1}n⟶{0,1}:
Indicator function construction: 

For each input 
x∈{0,1}n, define δx ​where δx(y)=1 if y=x 

Circuit for δx: Can be built with O(n) gates using AND operations to check each bit:

For each bit position i:

* If xi=1, check bit i is 1
* If xi=0, check bit i is 0 (using NOT)
* AND all these checks → circuit of size O(n)

Complete circuit for F:

```
F(y)= V (x:F(x)=1) δx(y)
```

* Number of terms in OR: at most 2n
* Each δx: O(n) gates
* OR of 2n terms: O(2n) gates
* Total: O(n⋅2n) gates


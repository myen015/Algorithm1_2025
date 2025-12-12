import math
#----------
# Problem 1
def count_functions(n, k):
    return k ** (2 ** n)

n = 2 
print("Functions to {0,1}:", count_functions(n, 2))
print("Functions to {-1,0,1}:", count_functions(n, 3))

def count_functions_m(n, m):
    # 2^{m * 2^n}
    return 2 ** (m * (2 ** n))

print("Functions to {0,1}^m (m=2):", count_functions_m(n, 2))

#----------
# Problem 2
def nand(a, b):
    return 1 if not (a and b) else 0 

def not_from_nand(a):
    return nand(a, a)

def and_from_nand(a, b):
    return not_from_nand(nand(a, b))

def or_from_nand(a, b):
    return nand(not_from_nand(a), not_from_nand(b))

# Truth tables
print("\nNOT from NAND:")
inputs = [0, 1] 
for a in inputs:
    print(a, "->", not_from_nand(a))

print("AND from NAND:")
for a in inputs:
    for b in inputs: 
        print(a, b, "->", and_from_nand(a, b))

print("OR from NAND:")
for a in inputs:
    for b in inputs:
        print(a, b, "->", or_from_nand(a, b))
        
#----------
# Problem 3:
def delta_size(n):
    return n + 1  

n = 3
num_inputs = 2 ** n
total_size = num_inputs * delta_size(n)
print("\nFor n=3, one delta size:", delta_size(n))
print("Total circuit size:", total_size)
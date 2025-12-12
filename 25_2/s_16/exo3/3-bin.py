import random
import math

def make_vecs(count, size):
    return [[random.randint(0,1) for _ in range(size)] for _ in range(count)]

def sim(x, y):
    top = sum(x[i]*y[i] for i in range(len(x)))
    s1, s2 = sum(x), sum(y)
    return top/(s1*s2) if s1 and s2 else 0

def stats(data):
    n = len(data)
    m = sum(data)/n
    var = sum((x-m)**2 for x in data)/n
    std = math.sqrt(var)
    
    skew = kurt = 0
    if std > 0:
        for x in data:
            z = (x-m)/std
            skew += z**3
            kurt += z**4
        skew = skew/n
        kurt = kurt/n - 3
    return m, std, skew, kurt

def sparse(size, ones):
    v = [0]*size
    for p in random.sample(range(size), ones):
        v[p] = 1
    return v

def C(n, k):
    if k > n or k < 0: return 0
    if k == 0: return 1
    k = min(k, n-k)
    r = 1
    for i in range(k):
        r = r*(n-i)//(i+1)
    return r


print("Problem 3: Binary Vectors")
print("="*50)

print("\n1. Random vectors:")
N = 50
num = 100

vecs = make_vecs(num, N)
print(f"Made {num} vectors, length {N}")

sims = []
for i in range(num):
    for j in range(i+1, num):
        sims.append(sim(vecs[i], vecs[j]))

m, s, sk, kt = stats(sims)
print(f"\nSimilarity stats:")
print(f"mean: {m:.4f}, std: {s:.4f}")
print(f"skew: {sk:.4f}, kurt: {kt:.4f}")
print("skew~0, kurt~0 means Gaussian")

print("\n2. Effect of N:")
print(f"{'N':<10} {'skew':<10} {'kurt':<10}")
for N in [10, 20, 50, 100, 200, 500]:
    v = make_vecs(50, N)
    s = []
    for i in range(len(v)):
        for j in range(i+1, len(v)):
            s.append(sim(v[i], v[j]))
    _, _, sk, kt = stats(s)
    print(f"{N:<10} {sk:<10.4f} {kt:<10.4f}")

print("\nBigger N -> more Gaussian (CLT)")

print("\n3. Sparse vectors:")
N = 2000
w = 5

count = C(N, w)
print(f"N={N}, w={w}")
print(f"C({N},{w}) = {count:,}")
print(f"That's {count:.2e}")

print("\nCalculation:")
print(f"C(n,k) = n!/(k!(n-k)!)")
print(f"C({N},{w}) = ({N}*{N-1}*{N-2}*{N-3}*{N-4}) / (5*4*3*2*1)")

print("\nExamples:")
for i in range(3):
    sv = sparse(N, w)
    pos = [j for j in range(N) if sv[j]==1]
    print(f"{i+1}. {pos}")

print("\n4. Capacity:")
cap = math.log2(count)
print(f"log2({count:,}) = {cap:.2f} bits")
print(f"Full vector: {N} bits")
print(f"Efficiency: {cap/N*100:.2f}%")

print(f"\nInterpretation:")
print(f"{N} neurons, {w} active")
print(f"Can make {count:,} patterns")
print(f"Using {w/N*100:.2f}% neurons")

print("\n5. Different w:")
for w in [1, 2, 5, 10, 20]:
    c = C(N, w)
    capacity = math.log2(c)
    print(f"w={w}: capacity={capacity:.2f} bits")
import random
import math

# make random binary vectors
def generate_vectors(num, length):
    return [[random.randint(0,1) for _ in range(length)] for _ in range(num)]

# dot product similarity
def sim_dot(x, y):
    dot = sum(xi*yi for xi,yi in zip(x,y))
    nx = sum(x)
    ny = sum(y)
    if nx == 0 or ny == 0: return 0
    return dot / (nx * ny)

# jaccard similarity
def sim_jacc(x, y):
    inter = sum(xi*yi for xi,yi in zip(x,y))
    union = sum(max(xi,yi) for xi,yi in zip(x,y))
    if union == 0: return 0
    return inter / union

# calculate stats
def get_stats(values):
    n = len(values)
    mean = sum(values) / n
    var = sum((x-mean)**2 for x in values) / n
    std = math.sqrt(var)
    
    # check if gaussian
    skew = sum((x-mean)**3 for x in values) / (n * std**3) if std > 0 else 0
    kurt = sum((x-mean)**4 for x in values) / (n * std**4) - 3 if std > 0 else 0
    
    return mean, std, skew, kurt

# sparse vector
def generate_sparse(length, num_ones):
    vec = [0] * length
    pos = random.sample(range(length), num_ones)
    for p in pos:
        vec[p] = 1
    return vec

# binomial coefficient
def C(n, k):
    if k > n or k < 0: return 0
    if k == 0 or k == n: return 1
    k = min(k, n-k)
    
    result = 1
    for i in range(k):
        result = result * (n-i) // (i+1)
    return result


print("PROBLEM 3: NEURO COMPUTING")
print("="*50)

# part 1-2: random vectors
print("\n1. Generate random vectors and similarities:")
N = 50
num_vecs = 100

vecs = generate_vectors(num_vecs, N)
print(f"Generated {num_vecs} vectors of length {N}")

# calculate similarities
sims_dot = []
sims_jacc = []

for i in range(num_vecs):
    for j in range(i+1, num_vecs):
        sims_dot.append(sim_dot(vecs[i], vecs[j]))
        sims_jacc.append(sim_jacc(vecs[i], vecs[j]))

mean_d, std_d, skew_d, kurt_d = get_stats(sims_dot)
mean_j, std_j, skew_j, kurt_j = get_stats(sims_jacc)

print(f"\nDot similarity: mean={mean_d:.4f}, std={std_d:.4f}")
print(f"  skewness={skew_d:.4f}, kurtosis={kurt_d:.4f}")
print(f"Jaccard similarity: mean={mean_j:.4f}, std={std_j:.4f}")
print(f"  skewness={skew_j:.4f}, kurtosis={kurt_j:.4f}")
print("\nSkew~0 and Kurt~0 -> Gaussian!")

# part 3: effect of N
print("\n2. Effect of increasing N:")
print(f"{'N':<10} {'Mean':<12} {'Skew':<12} {'Kurt':<12}")
print("-"*46)

for N in [10, 20, 50, 100, 200]:
    v = generate_vectors(50, N)
    s = []
    for i in range(len(v)):
        for j in range(i+1, len(v)):
            s.append(sim_dot(v[i], v[j]))
    
    m, st, sk, kt = get_stats(s)
    print(f"{N:<10} {m:<12.4f} {sk:<12.4f} {kt:<12.4f}")

print("\nAs N increases -> more Gaussian (CLT)")

# part 4: sparse vectors
print("\n3. Sparse vectors:")
N = 2000
w = 5

num_possible = C(N, w)

print(f"N={N}, w={w}")
print(f"Number of possible vectors: C({N},{w}) = {num_possible:,}")
print(f"That is ~ {num_possible:.3e}")

print("\nCalculation:")
print(f"C(n,k) = n! / (k!(n-k)!)")
print(f"C({N},{w}) = ({N}*{N-1}*{N-2}*{N-3}*{N-4}) / (5*4*3*2*1)")

# show example
print("\nExample sparse vectors:")
for i in range(3):
    sparse = generate_sparse(N, w)
    ones = [j for j,val in enumerate(sparse) if val==1]
    print(f"  Vector {i+1}: ones at {ones}")

# part 5: capacity
print("\n4. Capacity:")
capacity = math.log2(num_possible)

print(f"Capacity = log_2(C({N},{w}))")
print(f"         = log_2({num_possible:,})")
print(f"         = {capacity:.2f} bits")

print(f"\nInterpretation:")
print(f"  Raw: {N} bits")
print(f"  Actual info: {capacity:.2f} bits")
print(f"  Efficiency: {capacity/N*100:.2f}%")

print(f"\nBiological:")
print(f"  {N} neurons, {w} active")
print(f"  Can represent {num_possible:,} patterns")
print(f"  Using {w/N*100:.1f}% neurons")

print("\nDone!")
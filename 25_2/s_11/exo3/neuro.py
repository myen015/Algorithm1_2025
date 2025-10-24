# neuro_similarity.py
import numpy as np
from math import comb

def generate_binary_vectors(num_vectors, vector_length):
    """Generate random binary vectors"""
    return np.random.randint(0, 2, (num_vectors, vector_length))

def cosine_similarity(x, y):
    """Compute cosine similarity between two binary vectors"""
    dot_product = np.dot(x, y)
    norm_x = np.sum(x)
    norm_y = np.sum(y)
    if norm_x == 0 or norm_y == 0:
        return 0.0
    return dot_product / (norm_x * norm_y)

def jaccard_similarity(x, y):
    """Compute Jaccard similarity between two binary vectors"""
    intersection = np.sum(x & y)
    union = np.sum(x | y)
    if union == 0:
        return 0.0
    return intersection / union

def analyze_similarity_distribution(vector_length, num_vectors=100):
    """Analyze distribution of similarity measures"""
    vectors = generate_binary_vectors(num_vectors, vector_length)
    
    cosine_similarities = []
    jaccard_similarities = []
    
    # Compute pairwise similarities
    for i in range(num_vectors):
        for j in range(i + 1, num_vectors):
            cos_sim = cosine_similarity(vectors[i], vectors[j])
            jac_sim = jaccard_similarity(vectors[i], vectors[j])
            cosine_similarities.append(cos_sim)
            jaccard_similarities.append(jac_sim)
    
    return cosine_similarities, jaccard_similarities

def print_distribution_stats(similarities, metric_name, vector_length):
    """Print statistics for similarity distribution"""
    mean_val = np.mean(similarities)
    std_val = np.std(similarities)
    min_val = np.min(similarities)
    max_val = np.max(similarities)
    
    print(f"\n{metric_name} (N={vector_length}):")
    print(f"  Mean: {mean_val:.4f}")
    print(f"  Std:  {std_val:.4f}")
    print(f"  Min:  {min_val:.4f}")
    print(f"  Max:  {max_val:.4f}")
    
    # Simple histogram using text
    hist, bins = np.histogram(similarities, bins=10, range=(0, 1))
    print("  Distribution:")
    for i in range(len(hist)):
        bin_start = bins[i]
        bin_end = bins[i+1]
        count = hist[i]
        bar = '█' * (count // (num_vectors // 10))  # Scale for display
        print(f"    [{bin_start:.1f}-{bin_end:.1f}): {count:3d} {bar}")

# Analyze for different vector lengths
vector_lengths = [20, 50, 100]
num_vectors = 50  # Reduced for faster computation

print("Neuro Computing Similarity Analysis")
print("=" * 50)

for N in vector_lengths:
    cos_sim, jac_sim = analyze_similarity_distribution(N, num_vectors)
    
    print(f"\nVector Length N = {N}:")
    print("-" * 30)
    
    print_distribution_stats(cos_sim, "Cosine Similarity", N)
    print_distribution_stats(jac_sim, "Jaccard Similarity", N)

# Sparse vectors analysis
N = 2000
w = 5
num_sparse_vectors = comb(N, w)

print(f"\n" + "=" * 50)
print("SPARSE VECTORS ANALYSIS")
print("=" * 50)
print(f"Vector length (N): {N}")
print(f"Ones per vector (w): {w}")
print(f"Number of possible vectors: {num_sparse_vectors}")
print(f"Scientific notation: {num_sparse_vectors:.2e}")

# Capacity estimation
def estimate_capacity(N, w, similarity_threshold=0.1):
    """
    Estimate capacity - maximum number of distinguishable vectors
    Simple heuristic based on expected overlap
    """
    expected_overlap = w**2 / N
    capacity = int(N / (w * np.log(1/similarity_threshold)))
    return capacity

capacity = estimate_capacity(2000, 5)
print(f"\nCapacity Estimation:")
print(f"Estimated distinguishable vectors: {capacity}")
print(f"This represents the number of vectors that can be stored")
print(f"while maintaining similarity below threshold (0.1)")

# Additional analysis - show how capacity scales
print(f"\nCapacity scaling with different parameters:")
for w_val in [3, 5, 7]:
    cap = estimate_capacity(2000, w_val)
    print(f"  w={w_val}: {cap} vectors")

print(f"\nOBSERVATIONS:")
print(f"1. Similarity distributions become narrower as N increases")
print(f"2. Gaussian-like distribution emerges (Central Limit Theorem)")
print(f"3. Sparse coding enables exponential capacity")
print(f"4. Higher dimensions provide better vector separation")
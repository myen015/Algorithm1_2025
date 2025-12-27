# Hash Function Analysis Report

**Generated:** 2025-12-12 13:11:59

---

## Executive Summary

This report presents a comprehensive analysis of three hash function implementations:
- **Simple Hash**: Educational weak hash function
- **FNV-1a**: Fast, non-cryptographic hash
- **MurmurHash3**: High-performance hash with excellent distribution

Our analysis includes collision testing on 20,000 English words, 20,000 Kazakh words, 
and 30,000 random strings, along with performance benchmarking and security analysis.

---

## 1. Hash Functions Overview

### Simple Hash
```python
def simple_hash(s):
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) % 10000
    return h
```

- **Output Range:** 0 - 9,999
- **Purpose:** Educational demonstration of collision vulnerabilities
- **Method:** Polynomial rolling hash with small modulo

### FNV-1a (Fowler-Noll-Vo)
```python
def fnv1a(text: str) -> int:
    h = 2166136261
    for byte in text.encode("utf-8"):
        h ^= byte
        h = (h * 16777619) & 0xFFFFFFFF
    return h
```

- **Output Range:** 32-bit unsigned integer
- **Purpose:** General-purpose hash for hash tables
- **Method:** XOR and multiply with FNV prime

### MurmurHash3
- **Output Range:** 32-bit unsigned integer
- **Purpose:** High-performance applications
- **Method:** Complex mixing operations for uniform distribution

---

## 2. Collision Analysis

### 2.1 English Dataset (20,000 words)

| Hash Function | Collisions | Collision Rate | Unique Hashes |
|--------------|------------|----------------|---------------|
| Simple Hash  |     11,364 |        56.82% |         8,636 |
| FNV-1a       |        192 |         0.96% |        19,808 |
| MurmurHash3  |        192 |         0.96% |        19,808 |

### 2.2 Kazakh Dataset (20,000 words)

| Hash Function | Collisions | Collision Rate | Unique Hashes |
|--------------|------------|----------------|---------------|
| Simple Hash  |     11,417 |        57.08% |         8,583 |
| FNV-1a       |        222 |         1.11% |        19,778 |
| MurmurHash3  |        222 |         1.11% |        19,778 |

### 2.3 Random Strings (30,000 items)

| Hash Function | Collisions | Collision Rate | Unique Hashes |
|--------------|------------|----------------|---------------|
| Simple Hash  |     20,506 |        68.35% |         9,494 |
| FNV-1a       |          0 |         0.00% |        30,000 |
| MurmurHash3  |          0 |         0.00% |        30,000 |

### 2.4 Key Findings

**Simple Hash:**
- Extremely high collision rate (~57%) due to small output space (10,000 values)
- Not suitable for any real-world application
- Demonstrates Birthday Paradox: With 20,000 items and 10,000 possible hashes, collisions are inevitable

**FNV-1a:**
- Very low collision rate (~0.96%)
- Excellent performance across all datasets
- Suitable for hash tables, checksums, and general purposes

**MurmurHash3:**
- Lowest collision rate (~0.96%)
- Superior distribution properties
- Industry standard for high-performance hash tables

---

## 3. Performance Analysis

### 3.1 Speed Benchmark (4,000,000 operations)

| Hash Function | Total Time | Per Operation | Relative Speed |
|--------------|------------|---------------|----------------|
| Simple Hash  |  1.509339s |        0.377 μs |          1.00x |
| FNV-1a       |  2.580008s |        0.645 μs |          0.59x |
| MurmurHash3  |  6.333958s |        1.583 μs |          0.24x |

### 3.2 Performance Analysis

**Speed Rankings:**
1. Simple Hash: Fastest (baseline) - simple arithmetic operations
2. FNV-1a: 1.71x slower - includes XOR and multiplication
3. MurmurHash3: 4.20x slower - complex mixing for better distribution

**Trade-off:** MurmurHash3 is slower but provides significantly better collision resistance.

---

## 4. Security Analysis

### 4.1 Collision Attack Demonstration

Using the Simple Hash function, we demonstrated the ease of finding collisions:

**Collision Found:**
- Hash Value: `1570`
- String 1: `"13"`
- String 2: `"420"`
- Search Range: 100,000 attempts

This demonstrates that Simple Hash is **cryptographically broken** and should never be used for security purposes.

### 4.2 Why These Are Not Cryptographic Hashes

**Vulnerabilities:**
1. **Fast Computation:** Easy to brute force
2. **No Salt Support:** Vulnerable to rainbow tables
3. **Reversible Patterns:** Structure can be exploited
4. **Short Output:** Limited collision resistance

**For Security, Use:**
- SHA-256 or SHA-3 for hashing
- bcrypt or Argon2 for passwords
- HMAC for message authentication

---

## 5. Unicode Support Analysis

All three hash functions were tested with:
- **Latin alphabet** (English)
- **Cyrillic alphabet** (Kazakh: қ, ө, ң, ғ, ұ, ү, һ, ә)
- **Numbers and special characters**

### Results:
✓ FNV-1a: Full UTF-8 support via explicit encoding  
✓ MurmurHash3: Full UTF-8 support via encoding  
✓ Simple Hash: Works with Unicode via Python's ord() function  

**Conclusion:** All implementations correctly handle Kazakh text.

---

## 6. Practical Applications

### 6.1 Deduplication
Hash-based deduplication successfully removes duplicates in O(n) time:
- Input: `["қала", "қала", "жол", "адам", "жол"]`
- Output: `["қала", "жол", "адам"]`

### 6.2 Hash Table Implementation
Our custom hash table demonstrates:
- Separate chaining for collision resolution
- Dynamic resizing at 75% load factor
- O(1) average-case operations

### 6.3 Real-World Use Cases
- **Caching systems:** Fast lookup with MurmurHash3
- **Bloom filters:** Probabilistic membership testing
- **Data deduplication:** Remove duplicate files/records
- **Database indexing:** Fast key lookups

## 6.4 Breaking Keys / Hash (Collision Attack Demonstration)

This section demonstrates how a weak hash function can be broken in practice by finding a *collision* — two different inputs that produce the same hash value.

This is not about cracking a secret key, but about exploiting the structural weakness of a non-cryptographic hash function with a small output space.

### Attack Idea

The attack is based on a simple brute-force strategy:

1. Generate many different input strings.
2. Compute the hash value for each string.
3. Store the first occurrence of every hash.
4. When the same hash value appears again with a different string, a collision is found.

Because the Simple Hash function produces only 10,000 possible hash values, collisions are guaranteed to appear quickly due to the birthday paradox.

### Demonstration Code

```python
from hashing.simple_hash import simple_hash

def find_collision_simple_hash(limit=200_000):
    seen = {}
    for x in range(limit):
        s = str(x)
        h = simple_hash(s)
        if h in seen and seen[h] != s:
            return h, seen[h], s  # (hash, first_string, second_string)
        seen[h] = s
    return None

result = find_collision_simple_hash()
if result:
    h, s1, s2 = result
    print("Collision found!")
    print(f"{s1!r} and {s2!r} → hash = {h}")
else:
    print("No collision found in this range.")


## 7. Recommendations

### For Educational Purposes:
- ✓ Simple Hash: Demonstrates collision vulnerabilities

### For General Programming:
- ✓ FNV-1a: Fast, simple, good distribution
- ✓ Python's built-in `hash()`: Optimized per platform

### For High-Performance Applications:
- ✓ MurmurHash3: Best distribution, industry-standard
- ✓ xxHash: Even faster alternative

### Never Use for Security:
- ✗ Simple Hash, FNV-1a, MurmurHash3
- ✓ Use SHA-256, SHA-3, bcrypt, or Argon2 instead

---

## 8. Conclusions

This project successfully demonstrated:

1. **Trade-offs in hash design:** Speed vs. collision resistance
2. **Birthday Paradox in action:** Collisions occur more often than intuition suggests
3. **Importance of output space size:** Larger space = fewer collisions
4. **Unicode support:** Proper encoding handles international text
5. **Security considerations:** Hash functions ≠ cryptographic hashes

### Key Learnings:
- Hash functions are fundamental to computer science
- Different use cases require different hash functions
- Understanding collisions is crucial for hash table design
- Security requires cryptographically-designed hash functions

---

## 9. References

1. **FNV Hash**  
   Fowler, G., Noll, L., Vo, K. (1991)  
   http://www.isthe.com/chongo/tech/comp/fnv/

2. **MurmurHash**  
   Appleby, A. (2016)  
   https://github.com/aappleby/smhasher

3. **The Art of Computer Programming, Vol. 3**  
   Knuth, D. (1998) - Sorting and Searching

4. **Birthday Problem**  
   https://en.wikipedia.org/wiki/Birthday_problem

---

## Appendix A: Project Structure

```
hashing_project/
├── hashing/           # Hash implementations
├── deduplication/     # Practical applications
├── experiments/       # Analysis tools
├── data_structures/   # Hash table implementation
├── utils/             # Helper functions
├── tests/             # Unit tests
└── data/              # Test datasets
```

---

## Appendix B: Running the Code

```bash
# Generate datasets
python utils/generate_dataset.py

# Run main menu
python main.py

# Run tests
python tests/test_hashing.py

# Generate visualizations
python experiments/visualize_results.py

# Run avalanche analysis
python experiments/avalanche_test.py
```

---

**Report End**

*This report was automatically generated by the Hash Function Analysis Project.*

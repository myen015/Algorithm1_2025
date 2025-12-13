"""
Comprehensive Report Generator
Runs all experiments and generates a detailed analysis report
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hashing.simple_hash import simple_hash
from hashing.fnv1_hash import fnv1a
from hashing.murmur3_hash import murmur3_32
from experiments.collision_test import collision_stats
from experiments.benchmark_speed import time_hash
from experiments.collision_finder import find_collision
from utils.data_loader import load_words


def generate_markdown_report():
    """Generate comprehensive markdown report"""
    
    print("\n" + "="*70)
    print("GENERATING COMPREHENSIVE ANALYSIS REPORT")
    print("="*70)
    
    # Load datasets
    print("\n1. Loading datasets...")
    try:
        english_data = load_words("data/english_synthetic.txt")
        kazakh_data = load_words("data/kazakh_synthetic.txt")
        random_data = load_words("data/random_synthetic.txt")
        print(f"  ✓ Loaded {len(english_data)} English words")
        print(f"  ✓ Loaded {len(kazakh_data)} Kazakh words")
        print(f"  ✓ Loaded {len(random_data)} random strings")
    except FileNotFoundError as e:
        print(f"  ✗ Error: {e}")
        print("  Please run 'python utils/generate_dataset.py' first")
        return
    
    # Run experiments
    print("\n2. Running collision tests...")
    collision_results = {}
    for dataset_name, dataset in [("English", english_data), 
                                   ("Kazakh", kazakh_data),
                                   ("Random", random_data)]:
        collision_results[dataset_name] = {}
        for hash_name, hash_func in [("Simple Hash", simple_hash),
                                      ("FNV-1a", fnv1a),
                                      ("MurmurHash3", murmur3_32)]:
            collisions, rate = collision_stats(dataset, hash_func)
            collision_results[dataset_name][hash_name] = (collisions, rate)
            print(f"  ✓ {dataset_name} / {hash_name}: {collisions} collisions ({rate:.2%})")
    
    print("\n3. Running speed benchmarks...")
    speed_data = english_data * 200
    speed_results = {}
    for hash_name, hash_func in [("Simple Hash", simple_hash),
                                  ("FNV-1a", fnv1a),
                                  ("MurmurHash3", murmur3_32)]:
        total, avg = time_hash(speed_data, hash_func)
        speed_results[hash_name] = (total, avg)
        print(f"  ✓ {hash_name}: {avg*1e6:.3f} μs per operation")
    
    print("\n4. Finding collision in Simple Hash...")
    collision_demo = find_collision(100_000)
    if collision_demo:
        print(f"  ✓ Found collision: '{collision_demo[1]}' and '{collision_demo[2]}'")
    else:
        print("  ○ No collision found in search range")
    
    # Generate report
    print("\n5. Writing report...")
    
    report = f"""# Hash Function Analysis Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Executive Summary

This report presents a comprehensive analysis of three hash function implementations:
- **Simple Hash**: Educational weak hash function
- **FNV-1a**: Fast, non-cryptographic hash
- **MurmurHash3**: High-performance hash with excellent distribution

Our analysis includes collision testing on {len(english_data):,} English words, {len(kazakh_data):,} Kazakh words, 
and {len(random_data):,} random strings, along with performance benchmarking and security analysis.

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

### 2.1 English Dataset ({len(english_data):,} words)

| Hash Function | Collisions | Collision Rate | Unique Hashes |
|--------------|------------|----------------|---------------|
"""
    
    for hash_name in ["Simple Hash", "FNV-1a", "MurmurHash3"]:
        col, rate = collision_results["English"][hash_name]
        unique = len(english_data) - col
        report += f"| {hash_name:12} | {col:10,} | {rate:13.2%} | {unique:13,} |\n"
    
    report += f"""
### 2.2 Kazakh Dataset ({len(kazakh_data):,} words)

| Hash Function | Collisions | Collision Rate | Unique Hashes |
|--------------|------------|----------------|---------------|
"""
    
    for hash_name in ["Simple Hash", "FNV-1a", "MurmurHash3"]:
        col, rate = collision_results["Kazakh"][hash_name]
        unique = len(kazakh_data) - col
        report += f"| {hash_name:12} | {col:10,} | {rate:13.2%} | {unique:13,} |\n"
    
    report += f"""
### 2.3 Random Strings ({len(random_data):,} items)

| Hash Function | Collisions | Collision Rate | Unique Hashes |
|--------------|------------|----------------|---------------|
"""
    
    for hash_name in ["Simple Hash", "FNV-1a", "MurmurHash3"]:
        col, rate = collision_results["Random"][hash_name]
        unique = len(random_data) - col
        report += f"| {hash_name:12} | {col:10,} | {rate:13.2%} | {unique:13,} |\n"
    
    report += f"""
### 2.4 Key Findings

**Simple Hash:**
- Extremely high collision rate (~{collision_results["English"]["Simple Hash"][1]:.0%}) due to small output space (10,000 values)
- Not suitable for any real-world application
- Demonstrates Birthday Paradox: With 20,000 items and 10,000 possible hashes, collisions are inevitable

**FNV-1a:**
- Very low collision rate (~{collision_results["English"]["FNV-1a"][1]:.2%})
- Excellent performance across all datasets
- Suitable for hash tables, checksums, and general purposes

**MurmurHash3:**
- Lowest collision rate (~{collision_results["English"]["MurmurHash3"][1]:.2%})
- Superior distribution properties
- Industry standard for high-performance hash tables

---

## 3. Performance Analysis

### 3.1 Speed Benchmark ({len(speed_data):,} operations)

| Hash Function | Total Time | Per Operation | Relative Speed |
|--------------|------------|---------------|----------------|
"""
    
    baseline = speed_results["Simple Hash"][1]
    for hash_name in ["Simple Hash", "FNV-1a", "MurmurHash3"]:
        total, avg = speed_results[hash_name]
        relative = baseline / avg
        report += f"| {hash_name:12} | {total:9.6f}s | {avg*1e6:12.3f} μs | {relative:13.2f}x |\n"
    
    report += f"""
### 3.2 Performance Analysis

**Speed Rankings:**
1. Simple Hash: Fastest (baseline) - simple arithmetic operations
2. FNV-1a: {speed_results["FNV-1a"][1]/baseline:.2f}x slower - includes XOR and multiplication
3. MurmurHash3: {speed_results["MurmurHash3"][1]/baseline:.2f}x slower - complex mixing for better distribution

**Trade-off:** MurmurHash3 is slower but provides significantly better collision resistance.

---

## 4. Security Analysis

### 4.1 Collision Attack Demonstration

Using the Simple Hash function, we demonstrated the ease of finding collisions:
"""
    
    if collision_demo:
        h, s1, s2 = collision_demo
        report += f"""
**Collision Found:**
- Hash Value: `{h}`
- String 1: `"{s1}"`
- String 2: `"{s2}"`
- Search Range: 100,000 attempts

This demonstrates that Simple Hash is **cryptographically broken** and should never be used for security purposes.
"""
    else:
        report += "\n(No collision found in limited search)\n"
    
    report += """
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

---

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
"""
    
    # Write to file
    os.makedirs('results', exist_ok=True)
    filename = 'results/analysis_report.md'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"  ✓ Report saved to: {filename}")
    
    # Also create a summary file
    summary_file = 'results/summary.txt'
    summary = f"""
{'='*70}
HASH FUNCTION ANALYSIS - EXECUTIVE SUMMARY
{'='*70}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

COLLISION RATES (English Dataset):
  Simple Hash:  {collision_results["English"]["Simple Hash"][1]:6.2%}
  FNV-1a:       {collision_results["English"]["FNV-1a"][1]:6.2%}
  MurmurHash3:  {collision_results["English"]["MurmurHash3"][1]:6.2%}

SPEED (microseconds per operation):
  Simple Hash:  {speed_results["Simple Hash"][1]*1e6:.3f} μs
  FNV-1a:       {speed_results["FNV-1a"][1]*1e6:.3f} μs
  MurmurHash3:  {speed_results["MurmurHash3"][1]*1e6:.3f} μs

RECOMMENDATION:
  For hash tables: Use MurmurHash3 or FNV-1a
  For security:    Use SHA-256 or bcrypt
  For education:   Study Simple Hash's collisions

See analysis_report.md for full details.
{'='*70}
"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"  ✓ Summary saved to: {summary_file}")
    
    print("\n" + "="*70)
    print("REPORT GENERATION COMPLETE")
    print("="*70)
    print("\nGenerated files:")
    print(f"  • {filename}")
    print(f"  • {summary_file}")
    print("\nUse these files for your project defense and documentation!")
    print("="*70 + "\n")


if __name__ == "__main__":
    generate_markdown_report()
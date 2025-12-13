"""
Visualization module for hash function analysis
Generates charts and graphs to visualize results
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

from hashing.simple_hash import simple_hash
from hashing.fnv1_hash import fnv1a
from hashing.murmur3_hash import murmur3_32
from utils.data_loader import load_words
from experiments.collision_test import collision_stats
from experiments.benchmark_speed import time_hash


def plot_hash_distribution(data, hash_func, title, filename):
    """
    Plot distribution of hash values.
    
    Args:
        data: List of strings to hash
        hash_func: Hash function to use
        title: Plot title
        filename: Output filename
    """
    # Compute hashes
    hashes = [hash_func(s) for s in data[:1000]]  # Use subset for clarity
    
    # Create histogram
    plt.figure(figsize=(12, 6))
    plt.hist(hashes, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    plt.title(f'Hash Distribution: {title}', fontsize=14, fontweight='bold')
    plt.xlabel('Hash Value', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    # Save
    plt.savefig(f'results/{filename}', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: results/{filename}")


def plot_collision_comparison(results, filename):
    """
    Compare collision rates across hash functions.
    
    Args:
        results: Dict of {hash_name: (collisions, rate)}
        filename: Output filename
    """
    names = list(results.keys())
    rates = [results[name][1] * 100 for name in names]  # Convert to percentage
    
    # Create bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, rates, color=['#e74c3c', '#3498db', '#2ecc71'], 
                   edgecolor='black', linewidth=1.5)
    
    plt.title('Collision Rate Comparison', fontsize=14, fontweight='bold')
    plt.ylabel('Collision Rate (%)', fontsize=12)
    plt.xlabel('Hash Function', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%',
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'results/{filename}', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: results/{filename}")


def plot_speed_comparison(results, filename):
    """
    Compare hash computation speed.
    
    Args:
        results: Dict of {hash_name: (total_time, avg_time)}
        filename: Output filename
    """
    names = list(results.keys())
    times = [results[name][1] * 1_000_000 for name in names]  # Convert to microseconds
    
    # Create bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, times, color=['#9b59b6', '#e67e22', '#1abc9c'],
                   edgecolor='black', linewidth=1.5)
    
    plt.title('Hash Function Speed Comparison', fontsize=14, fontweight='bold')
    plt.ylabel('Time per Hash (μs)', fontsize=12)
    plt.xlabel('Hash Function', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}μs',
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'results/{filename}', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: results/{filename}")


def plot_bucket_distribution(data, hash_func, num_buckets, title, filename):
    """
    Show how items distribute across hash table buckets.
    
    Args:
        data: List of strings
        hash_func: Hash function
        num_buckets: Number of buckets in hash table
        title: Plot title
        filename: Output filename
    """
    # Compute bucket indices
    bucket_counts = Counter(hash_func(s) % num_buckets for s in data)
    
    # Create bar chart
    plt.figure(figsize=(14, 6))
    buckets = range(num_buckets)
    counts = [bucket_counts.get(i, 0) for i in buckets]
    
    plt.bar(buckets, counts, color='teal', edgecolor='black', alpha=0.7)
    plt.title(f'Bucket Distribution: {title}', fontsize=14, fontweight='bold')
    plt.xlabel('Bucket Index', fontsize=12)
    plt.ylabel('Number of Items', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    
    # Add statistics
    avg = sum(counts) / num_buckets
    plt.axhline(y=avg, color='red', linestyle='--', linewidth=2, label=f'Average: {avg:.1f}')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f'results/{filename}', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: results/{filename}")


def plot_collision_growth(hash_func, max_items, title, filename):
    """
    Show how collisions grow as items are added.
    
    Args:
        hash_func: Hash function to test
        max_items: Maximum number of items to test
        title: Plot title
        filename: Output filename
    """
    items_list = []
    collision_rates = []
    
    # Test at different sizes
    for n in range(100, max_items + 1, 100):
        data = [str(i) for i in range(n)]
        collisions, rate = collision_stats(data, hash_func)
        items_list.append(n)
        collision_rates.append(rate * 100)
    
    # Create line plot
    plt.figure(figsize=(10, 6))
    plt.plot(items_list, collision_rates, marker='o', linewidth=2, 
             markersize=4, color='crimson')
    
    plt.title(f'Collision Growth: {title}', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Items', fontsize=12)
    plt.ylabel('Collision Rate (%)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig(f'results/{filename}', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: results/{filename}")


def generate_all_visualizations():
    """Generate all visualizations"""
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    # Load datasets
    print("\n1. Loading datasets...")
    try:
        english_data = load_words("data/english_synthetic.txt")
        kazakh_data = load_words("data/kazakh_synthetic.txt")
        print(f"  Loaded {len(english_data)} English words")
        print(f"  Loaded {len(kazakh_data)} Kazakh words")
    except FileNotFoundError as e:
        print(f"  Error: {e}")
        print("  Please run 'python utils/generate_dataset.py' first")
        return
    
    # Hash distribution plots
    print("\n2. Creating hash distribution plots...")
    plot_hash_distribution(english_data, simple_hash, 
                          "Simple Hash", "distribution_simple.png")
    plot_hash_distribution(english_data, fnv1a, 
                          "FNV-1a", "distribution_fnv1a.png")
    plot_hash_distribution(english_data, murmur3_32, 
                          "MurmurHash3", "distribution_murmur3.png")
    
    # Collision comparison
    print("\n3. Creating collision comparison chart...")
    collision_results = {}
    for name, func in [("Simple Hash", simple_hash), 
                       ("FNV-1a", fnv1a), 
                       ("MurmurHash3", murmur3_32)]:
        collision_results[name] = collision_stats(english_data, func)
    
    plot_collision_comparison(collision_results, "collision_comparison.png")
    
    # Speed comparison
    print("\n4. Creating speed comparison chart...")
    speed_data = english_data * 200  # Larger dataset for timing
    speed_results = {}
    for name, func in [("Simple Hash", simple_hash), 
                       ("FNV-1a", fnv1a), 
                       ("MurmurHash3", murmur3_32)]:
        speed_results[name] = time_hash(speed_data, func)
    
    plot_speed_comparison(speed_results, "speed_comparison.png")
    
    # Bucket distribution
    print("\n5. Creating bucket distribution plots...")
    plot_bucket_distribution(english_data[:500], murmur3_32, 50,
                            "MurmurHash3 (500 items, 50 buckets)",
                            "bucket_distribution_murmur3.png")
    
    plot_bucket_distribution(english_data[:500], simple_hash, 50,
                            "Simple Hash (500 items, 50 buckets)",
                            "bucket_distribution_simple.png")
    
    # Collision growth
    print("\n6. Creating collision growth plots...")
    plot_collision_growth(simple_hash, 5000, "Simple Hash", 
                         "collision_growth_simple.png")
    plot_collision_growth(fnv1a, 10000, "FNV-1a", 
                         "collision_growth_fnv1a.png")
    
    # Summary
    print("\n" + "="*60)
    print("VISUALIZATION COMPLETE")
    print("="*60)
    print("\nGenerated files in 'results/' directory:")
    print("  - distribution_simple.png")
    print("  - distribution_fnv1a.png")
    print("  - distribution_murmur3.png")
    print("  - collision_comparison.png")
    print("  - speed_comparison.png")
    print("  - bucket_distribution_murmur3.png")
    print("  - bucket_distribution_simple.png")
    print("  - collision_growth_simple.png")
    print("  - collision_growth_fnv1a.png")
    print("\nUse these charts in your presentation and report!")
    print("="*60 + "\n")


if __name__ == "__main__":
    generate_all_visualizations()
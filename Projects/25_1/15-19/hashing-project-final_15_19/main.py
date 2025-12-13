import os

from hashing.simple_hash import simple_hash
from hashing.fnv1_hash import fnv1a
from hashing.murmur3_hash import murmur3_32

from deduplication.remove_duplicates import deduplicate

from experiments.collision_test import collision_stats
from experiments.benchmark_speed import time_hash
from experiments.collision_finder import find_collision

from utils.data_loader import load_words


def print_menu():
    print("\n" + "="*50)
    print("HASHING PROJECT MENU")
    print("="*50)
    print("1. Run deduplication demo")
    print("2. Collision test (Kazakh dataset)")
    print("3. Collision test (English dataset)")
    print("4. Speed benchmark")
    print("5. Break hash (find collisions for simple_hash)")
    print("6. Show all hash values for sample words")
    print("0. Exit")
    print("="*50)


def run_dedup_demo():
    words = ["қала", "қала", "жол", "адам", "жол"]
    print("\n--- Deduplication Demo ---")
    print("Original:", words)

    unique = deduplicate(words, murmur3_32)
    print("Unique:", unique)
    print(f"Removed {len(words) - len(unique)} duplicates")


def collision_test_kazakh():
    print("\n--- Collision Test: Kazakh Dataset ---")
    data = load_words("data/kazakh_synthetic.txt")
    print(f"Dataset size: {len(data)} words\n")

    for name, func in [
        ("Simple Hash", simple_hash),
        ("FNV-1a", fnv1a),
        ("MurmurHash3", murmur3_32),
    ]:
        col, rate = collision_stats(data, func)
        print(f"{name:15} | Collisions: {col:4d} | Rate: {rate:.4%}")


def collision_test_english():
    print("\n--- Collision Test: English Dataset ---")
    data = load_words("data/english_synthetic.txt")
    print(f"Dataset size: {len(data)} words\n")

    for name, func in [
        ("Simple Hash", simple_hash),
        ("FNV-1a", fnv1a),
        ("MurmurHash3", murmur3_32),
    ]:
        col, rate = collision_stats(data, func)
        print(f"{name:15} | Collisions: {col:4d} | Rate: {rate:.4%}")


def run_speed_benchmark():
    print("\n--- Speed Benchmark ---")
    data = load_words("data/english_synthetic.txt") * 200  # enlarge the dataset
    print(f"Testing with {len(data)} hash operations\n")

    for name, func in [
        ("Simple Hash", simple_hash),
        ("FNV-1a", fnv1a),
        ("MurmurHash3", murmur3_32),
    ]:
        total, avg = time_hash(data, func)
        print(f"{name:15} | Total: {total:.6f}s | Per item: {avg:.8f}s")


def break_hash():
    print("\n--- Hash Breaking Demonstration ---")
    print("Searching for collision in simple_hash...")
    result = find_collision(200_000)
    if result:
        h, s1, s2 = result
        print(f"\n✓ Collision found!")
        print(f"  Hash value: {h}")
        print(f"  String 1: '{s1}'")
        print(f"  String 2: '{s2}'")
        print(f"\nVerification:")
        print(f"  simple_hash('{s1}') = {simple_hash(s1)}")
        print(f"  simple_hash('{s2}') = {simple_hash(s2)}")
    else:
        print("✗ No collision found in 200,000 attempts.")


def show_hash_values():
    words = ["қала", "жол", "адам", "алгоритм", "Kazakhstan", "Hash"]
    print("\n--- Hash Values Comparison ---")
    for w in words:
        print(f"\n'{w}':")
        print(f"  Simple Hash:  {simple_hash(w):10d}")
        print(f"  FNV-1a:       {fnv1a(w):10d}")
        print(f"  MurmurHash3:  {murmur3_32(w):10d}")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("HASH FUNCTION ANALYSIS PROJECT")
    print("="*50)
    print("Working directory:", os.getcwd())

    while True:
        print_menu()
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            run_dedup_demo()
        elif choice == "2":
            collision_test_kazakh()
        elif choice == "3":
            collision_test_english()
        elif choice == "4":
            run_speed_benchmark()
        elif choice == "5":
            break_hash()
        elif choice == "6":
            show_hash_values()
        elif choice == "0":
            print("\nExiting... Goodbye!")
            break
        else:
            print("\n✗ Invalid input. Please try again.")
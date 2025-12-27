"""
Avalanche Effect Analysis
Tests how much the hash changes when input changes by one bit
Good hash functions should change ~50% of output bits for 1-bit input change
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hashing.simple_hash import simple_hash
from hashing.fnv1_hash import fnv1a
from hashing.murmur3_hash import murmur3_32


def count_bit_differences(hash1: int, hash2: int) -> int:
    """
    Count number of different bits between two hash values.
    
    Args:
        hash1: First hash value
        hash2: Second hash value
        
    Returns:
        Number of bits that differ
    """
    xor_result = hash1 ^ hash2
    return bin(xor_result).count('1')


def test_single_bit_change(test_string: str, hash_func, bit_position: int = 0) -> int:
    """
    Change one bit in input and measure hash difference.
    
    Args:
        test_string: Original string
        hash_func: Hash function to test
        bit_position: Which bit to flip in first character
        
    Returns:
        Number of bits changed in hash
    """
    if not test_string:
        return 0
    
    original_hash = hash_func(test_string)
    
    # Flip one bit in first character
    modified_char = chr(ord(test_string[0]) ^ (1 << bit_position))
    modified_string = modified_char + test_string[1:]
    
    modified_hash = hash_func(modified_string)
    
    return count_bit_differences(original_hash, modified_hash)


def test_single_char_change(test_string: str, hash_func, position: int = 0) -> int:
    """
    Change one character and measure hash difference.
    
    Args:
        test_string: Original string
        hash_func: Hash function to test
        position: Which character to change
        
    Returns:
        Number of bits changed in hash
    """
    if not test_string or position >= len(test_string):
        return 0
    
    original_hash = hash_func(test_string)
    
    # Change one character
    modified = list(test_string)
    modified[position] = chr((ord(modified[position]) + 1) % 256)
    modified_string = ''.join(modified)
    
    modified_hash = hash_func(modified_string)
    
    return count_bit_differences(original_hash, modified_hash)


def avalanche_effect_single_bit(test_string: str, hash_func) -> dict:
    """
    Test avalanche effect by flipping individual bits.
    
    Args:
        test_string: Test string
        hash_func: Hash function to test
        
    Returns:
        Dictionary with statistics
    """
    bit_changes = []
    
    # Test flipping each bit in first character
    for bit_pos in range(8):
        changes = test_single_bit_change(test_string, hash_func, bit_pos)
        bit_changes.append(changes)
    
    avg_changes = sum(bit_changes) / len(bit_changes) if bit_changes else 0
    
    return {
        'test_string': test_string,
        'bit_changes': bit_changes,
        'avg_bit_changes': avg_changes,
        'percentage': (avg_changes / 32) * 100,  # Assuming 32-bit hash
        'min_changes': min(bit_changes) if bit_changes else 0,
        'max_changes': max(bit_changes) if bit_changes else 0
    }


def avalanche_effect_chars(test_string: str, hash_func) -> dict:
    """
    Test avalanche effect by changing individual characters.
    
    Args:
        test_string: Test string
        hash_func: Hash function to test
        
    Returns:
        Dictionary with statistics
    """
    char_changes = []
    
    # Test changing each character
    for pos in range(min(len(test_string), 10)):  # Test first 10 chars
        changes = test_single_char_change(test_string, hash_func, pos)
        char_changes.append(changes)
    
    avg_changes = sum(char_changes) / len(char_changes) if char_changes else 0
    
    return {
        'test_string': test_string,
        'char_changes': char_changes,
        'avg_bit_changes': avg_changes,
        'percentage': (avg_changes / 32) * 100,  # Assuming 32-bit hash
        'min_changes': min(char_changes) if char_changes else 0,
        'max_changes': max(char_changes) if char_changes else 0
    }


def comprehensive_avalanche_test(hash_func, hash_name: str):
    """
    Run comprehensive avalanche effect tests.
    
    Args:
        hash_func: Hash function to test
        hash_name: Name of hash function for display
    """
    print(f"\n{'='*70}")
    print(f"AVALANCHE EFFECT TEST: {hash_name}")
    print(f"{'='*70}")
    
    test_strings = [
        "hello",
        "Kazakhstan",
        "Қазақстан",
        "algorithm",
        "test1234",
        "a" * 20
    ]
    
    print("\n1. Single Bit Flip Tests")
    print("-" * 70)
    total_percentage = 0
    
    for test_str in test_strings[:3]:  # Test first 3
        result = avalanche_effect_single_bit(test_str, hash_func)
        print(f"\nTest string: '{result['test_string']}'")
        print(f"  Average bit changes: {result['avg_bit_changes']:.2f} / 32")
        print(f"  Percentage: {result['percentage']:.2f}%")
        print(f"  Range: {result['min_changes']} - {result['max_changes']} bits")
        
        total_percentage += result['percentage']
    
    avg_percentage = total_percentage / 3
    print(f"\n  Overall average: {avg_percentage:.2f}%")
    
    if avg_percentage >= 45 and avg_percentage <= 55:
        print("  ✓ EXCELLENT avalanche effect (~50% is ideal)")
    elif avg_percentage >= 35 and avg_percentage <= 65:
        print("  ○ GOOD avalanche effect")
    else:
        print("  ✗ POOR avalanche effect")
    
    print("\n2. Character Change Tests")
    print("-" * 70)
    total_percentage = 0
    
    for test_str in test_strings[:3]:
        result = avalanche_effect_chars(test_str, hash_func)
        print(f"\nTest string: '{result['test_string']}'")
        print(f"  Average bit changes: {result['avg_bit_changes']:.2f} / 32")
        print(f"  Percentage: {result['percentage']:.2f}%")
        
        total_percentage += result['percentage']
    
    avg_percentage = total_percentage / 3
    print(f"\n  Overall average: {avg_percentage:.2f}%")


def compare_avalanche_effects():
    """Compare avalanche effects across all hash functions"""
    print("\n" + "="*70)
    print("AVALANCHE EFFECT COMPARISON")
    print("="*70)
    print("\nTesting how hash output changes when input changes slightly...")
    print("Ideal result: ~50% of bits change (shows good mixing)")
    
    hash_functions = [
        (simple_hash, "Simple Hash"),
        (fnv1a, "FNV-1a"),
        (murmur3_32, "MurmurHash3")
    ]
    
    for hash_func, name in hash_functions:
        comprehensive_avalanche_test(hash_func, name)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("\nKey Takeaways:")
    print("  - Simple Hash: Poor avalanche effect due to simple formula")
    print("  - FNV-1a: Good avalanche effect with XOR and multiplication")
    print("  - MurmurHash3: Excellent avalanche effect by design")
    print("\nAvalanche effect is crucial for:")
    print("  • Uniform distribution in hash tables")
    print("  • Collision resistance")
    print("  • Security properties (for cryptographic hashes)")
    print("="*70 + "\n")


def run_quick_test():
    """Quick avalanche test for demonstration"""
    print("\n" + "="*70)
    print("QUICK AVALANCHE DEMONSTRATION")
    print("="*70)
    
    test_str1 = "hello"
    test_str2 = "iello"  # Changed first character
    
    print(f"\nOriginal: '{test_str1}'")
    print(f"Modified: '{test_str2}' (changed 'h' → 'i')")
    print("\nHash values:")
    
    for hash_func, name in [(simple_hash, "Simple Hash"),
                            (fnv1a, "FNV-1a"),
                            (murmur3_32, "MurmurHash3")]:
        h1 = hash_func(test_str1)
        h2 = hash_func(test_str2)
        bits_changed = count_bit_differences(h1, h2)
        percentage = (bits_changed / 32) * 100
        
        print(f"\n{name}:")
        print(f"  '{test_str1}' → {h1:10d} (0x{h1:08x})")
        print(f"  '{test_str2}' → {h2:10d} (0x{h2:08x})")
        print(f"  Bits changed: {bits_changed}/32 ({percentage:.1f}%)")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_test()
    else:
        compare_avalanche_effects()
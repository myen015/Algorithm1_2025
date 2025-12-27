import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hashing.simple_hash import simple_hash
from hashing.fnv1_hash import fnv1a
from hashing.murmur3_hash import murmur3_32
from deduplication.remove_duplicates import deduplicate


class TestHashConsistency(unittest.TestCase):
    """Test that hash functions produce consistent results"""
    
    def test_simple_hash_consistency(self):
        """Same input should always produce same hash"""
        test_string = "Kazakhstan"
        hash1 = simple_hash(test_string)
        hash2 = simple_hash(test_string)
        self.assertEqual(hash1, hash2, "Simple hash should be deterministic")
    
    def test_fnv1a_consistency(self):
        """FNV-1a should be deterministic"""
        test_string = "Қазақстан"
        hash1 = fnv1a(test_string)
        hash2 = fnv1a(test_string)
        self.assertEqual(hash1, hash2, "FNV-1a should be deterministic")
    
    def test_murmur3_consistency(self):
        """MurmurHash3 should be deterministic"""
        test_string = "алгоритм"
        hash1 = murmur3_32(test_string)
        hash2 = murmur3_32(test_string)
        self.assertEqual(hash1, hash2, "MurmurHash3 should be deterministic")


class TestHashDifferentiation(unittest.TestCase):
    """Test that different inputs produce different hashes (usually)"""
    
    def test_different_strings_different_hashes(self):
        """Different strings should produce different hashes (usually)"""
        s1 = "hello"
        s2 = "world"
        
        # For good hash functions, these should be different
        self.assertNotEqual(fnv1a(s1), fnv1a(s2))
        self.assertNotEqual(murmur3_32(s1), murmur3_32(s2))
    
    def test_case_sensitivity(self):
        """Hash functions should be case-sensitive"""
        lower = "kazakh"
        upper = "KAZAKH"
        
        for hash_func in [simple_hash, fnv1a, murmur3_32]:
            self.assertNotEqual(
                hash_func(lower), 
                hash_func(upper),
                f"{hash_func.__name__} should be case-sensitive"
            )


class TestUnicodeSupport(unittest.TestCase):
    """Test handling of Unicode characters"""
    
    def test_kazakh_cyrillic(self):
        """Should handle Kazakh Cyrillic characters"""
        kazakh_words = ["Қазақстан", "қала", "жол", "адам"]
        
        for word in kazakh_words:
            for hash_func in [fnv1a, murmur3_32]:
                try:
                    h = hash_func(word)
                    self.assertIsInstance(h, int, f"{hash_func.__name__} should return int")
                except Exception as e:
                    self.fail(f"{hash_func.__name__} failed on '{word}': {e}")
    
    def test_empty_string(self):
        """Should handle empty strings"""
        for hash_func in [simple_hash, fnv1a, murmur3_32]:
            try:
                h = hash_func("")
                self.assertIsInstance(h, int)
            except Exception as e:
                self.fail(f"{hash_func.__name__} failed on empty string: {e}")
    
    def test_special_characters(self):
        """Should handle special characters"""
        special = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        for hash_func in [simple_hash, fnv1a, murmur3_32]:
            try:
                h = hash_func(special)
                self.assertIsInstance(h, int)
            except Exception as e:
                self.fail(f"{hash_func.__name__} failed on special chars: {e}")


class TestHashRange(unittest.TestCase):
    """Test that hash values are within expected ranges"""
    
    def test_simple_hash_range(self):
        """Simple hash should be in range [0, 9999]"""
        test_strings = ["a", "test", "Kazakhstan", "Қазақстан" * 10]
        
        for s in test_strings:
            h = simple_hash(s)
            self.assertGreaterEqual(h, 0, "Hash should be >= 0")
            self.assertLess(h, 10000, "Hash should be < 10000")
    
    def test_fnv1a_range(self):
        """FNV-1a should be 32-bit unsigned integer"""
        test_strings = ["short", "medium length string", "very " * 100 + "long"]
        
        for s in test_strings:
            h = fnv1a(s)
            self.assertGreaterEqual(h, 0, "Hash should be >= 0")
            self.assertLessEqual(h, 0xFFFFFFFF, "Hash should fit in 32 bits")
    
    def test_murmur3_range(self):
        """MurmurHash3 should be 32-bit unsigned integer"""
        test_strings = ["a", "test string", "Қазақстан"]
        
        for s in test_strings:
            h = murmur3_32(s)
            self.assertGreaterEqual(h, 0, "Hash should be >= 0")
            self.assertLessEqual(h, 0xFFFFFFFF, "Hash should fit in 32 bits")


class TestDeduplication(unittest.TestCase):
    """Test deduplication functionality"""
    
    def test_basic_deduplication(self):
        """Should remove duplicate strings"""
        input_list = ["apple", "banana", "apple", "cherry", "banana"]
        result = deduplicate(input_list, murmur3_32)
        
        # Should have only unique items
        self.assertEqual(len(result), 3, "Should have 3 unique items")
        self.assertIn("apple", result)
        self.assertIn("banana", result)
        self.assertIn("cherry", result)
    
    def test_no_duplicates(self):
        """Should handle list with no duplicates"""
        input_list = ["one", "two", "three"]
        result = deduplicate(input_list, fnv1a)
        
        self.assertEqual(len(result), 3)
    
    def test_all_duplicates(self):
        """Should handle list with all duplicates"""
        input_list = ["same", "same", "same", "same"]
        result = deduplicate(input_list, murmur3_32)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "same")
    
    def test_order_preservation(self):
        """Should preserve first occurrence order"""
        input_list = ["first", "second", "first", "third"]
        result = deduplicate(input_list, fnv1a)
        
        self.assertEqual(result[0], "first")
        self.assertEqual(result[1], "second")
        self.assertEqual(result[2], "third")
    
    def test_kazakh_deduplication(self):
        """Should handle Kazakh text deduplication"""
        input_list = ["қала", "жол", "қала", "адам"]
        result = deduplicate(input_list, murmur3_32)
        
        self.assertEqual(len(result), 3)
        self.assertIn("қала", result)
        self.assertIn("жол", result)
        self.assertIn("адам", result)


class TestCollisionResistance(unittest.TestCase):
    """Test collision resistance properties"""
    
    def test_simple_hash_has_collisions(self):
        """Simple hash SHOULD have collisions (by design)"""
        hashes = set()
        collisions = 0
        
        for i in range(20000):
            h = simple_hash(str(i))
            if h in hashes:
                collisions += 1
            hashes.add(h)
        
        # Simple hash should definitely have collisions
        self.assertGreater(collisions, 100, "Simple hash should have many collisions")
    
    def test_fnv1a_few_collisions(self):
        """FNV-1a should have very few collisions on small dataset"""
        hashes = set()
        collisions = 0
        
        for i in range(10000):
            h = fnv1a(str(i))
            if h in hashes:
                collisions += 1
            hashes.add(h)
        
        # FNV-1a should have very few collisions
        self.assertLess(collisions, 10, "FNV-1a should have few collisions")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_very_long_string(self):
        """Should handle very long strings"""
        long_string = "a" * 100000
        
        for hash_func in [simple_hash, fnv1a, murmur3_32]:
            try:
                h = hash_func(long_string)
                self.assertIsInstance(h, int)
            except Exception as e:
                self.fail(f"{hash_func.__name__} failed on long string: {e}")
    
    def test_numeric_strings(self):
        """Should handle numeric strings"""
        numbers = ["0", "123", "999999", "-42"]
        
        for num in numbers:
            for hash_func in [simple_hash, fnv1a, murmur3_32]:
                h = hash_func(num)
                self.assertIsInstance(h, int)
    
    def test_whitespace_handling(self):
        """Different whitespace should produce different hashes"""
        s1 = "hello world"
        s2 = "helloworld"
        s3 = "hello  world"  # Two spaces
        
        for hash_func in [fnv1a, murmur3_32]:
            h1 = hash_func(s1)
            h2 = hash_func(s2)
            h3 = hash_func(s3)
            
            self.assertNotEqual(h1, h2, "Space should matter")
            self.assertNotEqual(h1, h3, "Number of spaces should matter")


class TestMurmurHash3Seed(unittest.TestCase):
    """Test MurmurHash3 seed parameter"""
    
    def test_different_seeds_different_hashes(self):
        """Different seeds should produce different hashes"""
        text = "test"
        h1 = murmur3_32(text, seed=0)
        h2 = murmur3_32(text, seed=42)
        h3 = murmur3_32(text, seed=999)
        
        self.assertNotEqual(h1, h2, "Different seeds should give different hashes")
        self.assertNotEqual(h2, h3, "Different seeds should give different hashes")
        self.assertNotEqual(h1, h3, "Different seeds should give different hashes")
    
    def test_same_seed_same_hash(self):
        """Same seed should give consistent results"""
        text = "Kazakhstan"
        seed = 12345
        
        h1 = murmur3_32(text, seed=seed)
        h2 = murmur3_32(text, seed=seed)
        
        self.assertEqual(h1, h2, "Same seed should give same hash")


def run_tests():
    """Run all tests with detailed output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHashConsistency))
    suite.addTests(loader.loadTestsFromTestCase(TestHashDifferentiation))
    suite.addTests(loader.loadTestsFromTestCase(TestUnicodeSupport))
    suite.addTests(loader.loadTestsFromTestCase(TestHashRange))
    suite.addTests(loader.loadTestsFromTestCase(TestDeduplication))
    suite.addTests(loader.loadTestsFromTestCase(TestCollisionResistance))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestMurmurHash3Seed))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from typing import Any, Optional, Callable, List, Tuple
from hashing.murmur3_hash import murmur3_32


class HashTable:
    def __init__(self, initial_size: int = 16, hash_func: Callable = murmur3_32):
    
        self.size = initial_size
        self.hash_func = hash_func
        self.count = 0
        
        # Each bucket is a list of (key, value) tuples
        self.buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(self.size)]
        
        # Statistics
        self.collisions = 0
        self.resizes = 0
    
    def _hash(self, key: str) -> int:
        return self.hash_func(key) % self.size
    
    def _load_factor(self) -> float:
       
        return self.count / self.size if self.size > 0 else 0
    
    def _resize(self):
       
        old_buckets = self.buckets
        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0
        self.resizes += 1
        
        # Rehash all existing items
        for bucket in old_buckets:
            for key, value in bucket:
                self.insert(key, value)
    
    def insert(self, key: str, value: Any) -> None:
       
        # Resize if load factor too high
        if self._load_factor() > 0.75:
            self._resize()
        
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing
                return
        
        # Add new key-value pair
        if len(bucket) > 0:
            self.collisions += 1  # Track collision
        
        bucket.append((key, value))
        self.count += 1
    
    def search(self, key: str) -> Optional[Any]:
    
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return None
    
    def delete(self, key: str) -> bool:
     
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.count -= 1
                return True
        
        return False
    
    def contains(self, key: str) -> bool:
      
        return self.search(key) is not None
    
    def keys(self) -> List[str]:
       
        all_keys = []
        for bucket in self.buckets:
            for key, _ in bucket:
                all_keys.append(key)
        return all_keys
    
    def values(self) -> List[Any]:
      
        all_values = []
        for bucket in self.buckets:
            for _, value in bucket:
                all_values.append(value)
        return all_values
    
    def items(self) -> List[Tuple[str, Any]]:
       
        all_items = []
        for bucket in self.buckets:
            all_items.extend(bucket)
        return all_items
    
    def get_statistics(self) -> dict:
       
        # Calculate bucket utilization
        non_empty_buckets = sum(1 for bucket in self.buckets if len(bucket) > 0)
        
        # Find longest chain
        max_chain_length = max(len(bucket) for bucket in self.buckets) if self.buckets else 0
        
        # Average chain length (for non-empty buckets)
        avg_chain_length = (self.count / non_empty_buckets) if non_empty_buckets > 0 else 0
        
        return {
            'total_items': self.count,
            'table_size': self.size,
            'load_factor': self._load_factor(),
            'collisions': self.collisions,
            'resizes': self.resizes,
            'non_empty_buckets': non_empty_buckets,
            'bucket_utilization': non_empty_buckets / self.size if self.size > 0 else 0,
            'max_chain_length': max_chain_length,
            'avg_chain_length': avg_chain_length
        }
    
    def __len__(self) -> int:
        """Return number of items in table"""
        return self.count
    
    def __contains__(self, key: str) -> bool:
        """Support 'in' operator"""
        return self.contains(key)
    
    def __getitem__(self, key: str) -> Any:
        """Support table[key] syntax"""
        value = self.search(key)
        if value is None:
            raise KeyError(f"Key not found: {key}")
        return value
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Support table[key] = value syntax"""
        self.insert(key, value)
    
    def __delitem__(self, key: str) -> None:
        """Support del table[key] syntax"""
        if not self.delete(key):
            raise KeyError(f"Key not found: {key}")
    
    def __repr__(self) -> str:
        """String representation"""
        return f"HashTable(size={self.size}, items={self.count}, load_factor={self._load_factor():.2f})"


def demo_hash_table():
    print("="*60)
    print("HASH TABLE DEMONSTRATION")
    print("="*60)
    
    # Create hash table
    table = HashTable(initial_size=8)
    
    print("\n1. Inserting items...")
    # Insert some items
    countries = {
        "KZ": "Kazakhstan",
        "US": "United States",
        "GB": "United Kingdom",
        "JP": "Japan",
        "DE": "Germany",
        "FR": "France",
        "CN": "China",
        "RU": "Russia",
        "IN": "India",
        "BR": "Brazil"
    }
    
    for code, name in countries.items():
        table.insert(code, name)
        print(f"  Inserted: {code} -> {name}")
    
    print(f"\n  {table}")
    
    # Search for items
    print("\n2. Searching for items...")
    search_codes = ["KZ", "US", "XX"]
    for code in search_codes:
        result = table.search(code)
        if result:
            print(f"  {code}: {result}")
        else:
            print(f"  {code}: Not found")
    
    # Check existence
    print("\n3. Checking existence...")
    print(f"  'JP' in table: {'JP' in table}")
    print(f"  'XX' in table: {'XX' in table}")
    
    # Update value
    print("\n4. Updating value...")
    print(f"  Before: KZ -> {table['KZ']}")
    table['KZ'] = "Қазақстан"
    print(f"  After:  KZ -> {table['KZ']}")
    
    # Delete item
    print("\n5. Deleting item...")
    print(f"  Before delete: {len(table)} items")
    table.delete("FR")
    print(f"  After delete:  {len(table)} items")
    print(f"  'FR' in table: {'FR' in table}")
    
    # Show statistics
    print("\n6. Performance Statistics:")
    stats = table.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
    
    # Test with Kazakh text
    print("\n7. Testing with Kazakh text...")
    kazakh_table = HashTable()
    kazakh_words = {
        "қала": "city",
        "жол": "road",
        "адам": "person",
        "кітап": "book",
        "үй": "house"
    }
    
    for kz, en in kazakh_words.items():
        kazakh_table[kz] = en
    
    print("  Kazakh-English dictionary:")
    for key in kazakh_table.keys():
        print(f"    {key} -> {kazakh_table[key]}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    demo_hash_table()
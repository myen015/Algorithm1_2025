from collections import defaultdict

def collision_stats(strings, hash_func):
    table = defaultdict(int)
    for s in strings:
        table[hash_func(s)] += 1

    total = len(strings)
    unique = len(table)
    collisions = total - unique
    return collisions, collisions / total

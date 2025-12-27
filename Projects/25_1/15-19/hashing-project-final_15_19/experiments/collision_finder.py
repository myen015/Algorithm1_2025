from hashing.simple_hash import simple_hash

def find_collision(limit=200000):
    seen = {}
    for i in range(limit):
        s = str(i)
        h = simple_hash(s)
        if h in seen and seen[h] != s:
            return h, seen[h], s
        seen[h] = s
    return None

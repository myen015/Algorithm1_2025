from hashing.simple_hash import simple_hash

def find_collision_simple_hash(limit=100000):
    seen = {}
    for x in range(limit):
        s = str(x)
        h = simple_hash(s)
        if h in seen and seen[h] != s:
            return h, seen[h], s  # (hash, first_string, second_string)
        else:
            seen[h] = s
    return None

result = find_collision_simple_hash()
if result:
    h, s1, s2 = result
    print("Collision found!")
    print(f"{s1!r} and {s2!r} → hash = {h}")
else:
    print("No collision found in this range.")

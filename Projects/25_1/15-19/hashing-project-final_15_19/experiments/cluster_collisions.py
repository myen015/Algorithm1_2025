from collections import defaultdict
from hashing.simple_hash import simple_hash

def cluster(limit=100000):
    bucket = defaultdict(list)
    for i in range(limit):
        s = "x" + str(i)
        h = simple_hash(s)
        bucket[h].append(s)

    return [b for b in bucket.values() if len(b) > 1]

import time

def time_hash(strings, hash_func):
    start = time.perf_counter()
    for s in strings:
        hash_func(s)
    end = time.perf_counter()
    total_time = end - start
    return total_time, total_time / len(strings)

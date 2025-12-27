def deduplicate(strings, hash_func):
    seen = set()
    result = []
    for s in strings:
        h = hash_func(s)
        if h not in seen:
            seen.add(h)
            result.append(s)
    return result

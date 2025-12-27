def simple_hash(s: str) -> int:
 
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) % 10000
    return h
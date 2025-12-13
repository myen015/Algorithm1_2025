import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import string
import itertools
from typing import Callable, Optional, Tuple

from hashing.simple_hash import simple_hash
from hashing.fnv1_hash import fnv1a
from hashing.murmur3_hash import murmur3_32

ALPHABET = string.ascii_lowercase + string.digits


def generate_strings(max_len: int):
 
    for length in range(1, max_len + 1):
        for tup in itertools.product(ALPHABET, repeat=length):
            yield "".join(tup)


def find_collision(
    hash_func: Callable[[str], int],
    max_len: int = 4,
    limit: int = 500_000,
) -> Optional[Tuple[int, str, str]]:

    seen = {}
    tried = 0

    for s in generate_strings(max_len):
        h = hash_func(s)

        # Collision found: same hash but different string
        if h in seen and seen[h] != s:
            return h, seen[h], s

        seen[h] = s
        tried += 1
        if tried >= limit:
            break

    return None


def find_preimage(
    hash_func: Callable[[str], int],
    target_hash: int,
    max_len: int = 4,
    limit: int = 500_000,
) -> Optional[str]:
  
    tried = 0

    for s in generate_strings(max_len):
        if hash_func(s) == target_hash:
            return s

        tried += 1
        if tried >= limit:
            break

    return None


def hack_simple_collision():
    result = find_collision(simple_hash, max_len=4, limit=500_000)
    if result is None:
        print("[simple_hash] No collision found within search limits.")
    else:
        h, s1, s2 = result
        print("[simple_hash] Collision found!")
        print(f"  hash = {h}")
        print(f"  s1   = {s1!r}")
        print(f"  s2   = {s2!r}")


def hack_fnv_collision():
    result = find_collision(fnv1a, max_len=4, limit=500_000)
    if result is None:
        print("[fnv1a] No collision found within search limits.")
    else:
        h, s1, s2 = result
        print("[fnv1a] Collision found!")
        print(f"  hash = {h}")
        print(f"  s1   = {s1!r}")
        print(f"  s2   = {s2!r}")


def hack_murmur_collision():
    result = find_collision(murmur3_32, max_len=4, limit=500_000)
    if result is None:
        print("[murmur3_32] No collision found within search limits.")
    else:
        h, s1, s2 = result
        print("[murmur3_32] Collision found!")
        print(f"  hash = {h}")
        print(f"  s1   = {s1!r}")
        print(f"  s2   = {s2!r}")

def hack_simple_preimage():
    raw = input("Enter target hash for simple_hash (e.g. 12345 or 0x1a2b3c): ").strip()
    try:
        target = int(raw, 0)
    except ValueError:
        print("Invalid hash format. Use decimal (12345) or hex (0x1a2b3c).")
        return

    s = find_preimage(simple_hash, target_hash=target, max_len=4, limit=1_000_000)
    if s is None:
        print("[simple_hash] Preimage not found within search limits.")
    else:
        print(f"[simple_hash] Preimage found: {s!r}")


def hack_fnv_preimage():
    raw = input("Enter target hash for fnv1a (e.g. 12345 or 0x1a2b3c): ").strip()
    try:
        target = int(raw, 0)
    except ValueError:
        print("Invalid hash format. Use decimal (12345) or hex (0x1a2b3c).")
        return

    s = find_preimage(fnv1a, target_hash=target, max_len=4, limit=1_000_000)
    if s is None:
        print("[fnv1a] Preimage not found within search limits.")
    else:
        print(f"[fnv1a] Preimage found: {s!r}")


def hack_murmur_preimage():
    raw = input("Enter target hash for murmur3_32 (e.g. 12345 or 0x1a2b3c): ").strip()
    try:
        target = int(raw, 0)
    except ValueError:
        print("Invalid hash format. Use decimal (12345) or hex (0x1a2b3c).")
        return

    s = find_preimage(murmur3_32, target_hash=target, max_len=4, limit=1_000_000)
    if s is None:
        print("[murmur3_32] Preimage not found within search limits.")
    else:
        print(f"[murmur3_32] Preimage found: {s!r}")

# ---- Menu launcher ---- #

if __name__ == "__main__":
    while True:
        print("\n=== Hash Cracking Lab (Educational Only) ===")
        print("1 — Find collision (simple_hash)")
        print("2 — Find collision (fnv1a)")
        print("3 — Find collision (murmur3_32)")
        print("4 — Find preimage (simple_hash)")
        print("5 — Find preimage (fnv1a)")
        print("6 — Find preimage (murmur3_32)")
        print("0 — Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            hack_simple_collision()
        elif choice == "2":
            hack_fnv_collision()
        elif choice == "3":
            hack_murmur_collision()
        elif choice == "4":
            hack_simple_preimage()
        elif choice == "5":
            hack_fnv_preimage()
        elif choice == "6":
            hack_murmur_preimage()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")
            
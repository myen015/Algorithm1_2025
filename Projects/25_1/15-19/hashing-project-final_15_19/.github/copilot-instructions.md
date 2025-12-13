# Copilot Instructions for Hashing Project

## Project Overview
This project explores hash functions and deduplication techniques for lists of words, with a focus on benchmarking and collision analysis. The codebase is organized for experimentation and modularity.

## Architecture & Key Components
- **src/hashing/**: Implements hash functions (`fnv1_hash.py`, `murmur3_hash.py`, `simple_hash.py`) and main orchestration (`main.py`).
- **src/deduplication/remove_duplicates.py**: Provides deduplication logic, typically using a hash function as a parameter.
- **src/experiments/**: Contains scripts for benchmarking speed, finding and clustering collisions, and testing hash function behavior.
- **data/**: Intended for input datasets (e.g., word lists).

## Developer Workflows
- **Run main script**: `python3 src/hashing/main.py` (not `main.py` in root)
- **Experimentation**: Run scripts in `src/experiments/` directly for benchmarks and collision analysis.
- **Deduplication**: Use `deduplicate(words, hash_func)` pattern, where `hash_func` is a function from `src/hashing/`.

## Import Conventions
- Relative imports are used within `src/` (e.g., `from simple_hash import simple_hash`).
- When moving or refactoring files, ensure import paths remain correct.

## Patterns & Examples
- Hash functions are stateless and take a single string argument.
- Deduplication expects a list and a hash function, returns a list of unique items.
- Example usage (see `main.py`):
  ```python
  from remove_duplicates import deduplicate
  from murmur3_hash import murmur3_32
  words = ["қала", "қала", "адам", "жол", "жол", "жол"]
  unique = deduplicate(words, murmur3_32)
  ```

## Testing & Debugging
- No formal test suite detected; validate changes by running experiment scripts and checking output.
- For debugging, print intermediate results in scripts (see `main.py`).

## External Dependencies
- No third-party dependencies detected; all hashing logic is implemented in-house.

## Project-Specific Notes
- Unicode and non-Latin text is used in examples; ensure hash functions handle these correctly.
- Scripts are modular—add new hash functions or experiments by following existing file patterns.

## Key Files
- `src/hashing/main.py`: Entry point for deduplication demo.
- `src/deduplication/remove_duplicates.py`: Core deduplication logic.
- `src/hashing/{fnv1_hash.py,murmur3_hash.py,simple_hash.py}`: Hash function implementations.
- `src/experiments/`: Benchmarking and collision analysis scripts.

---

_If any section is unclear or missing, please provide feedback to improve these instructions._

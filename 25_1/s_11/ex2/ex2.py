import random
import time
import matplotlib.pyplot as plt

# -----------------------------
# Sorting Algorithms
# -----------------------------

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def quick_sort_standard(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_standard(left) + middle + quick_sort_standard(right)


def quick_sort_random(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_random(left) + middle + quick_sort_random(right)


def quick_sort_average(arr):
    if len(arr) <= 1:
        return arr
    low = arr[0]
    high = arr[-1]
    mid = arr[len(arr) // 2]
    pivot = (low + mid + high) // 3
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_average(left) + middle + quick_sort_average(right)


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = merge_sort(arr[:mid])
        R = merge_sort(arr[mid:])
        merged = []
        i = j = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                merged.append(L[i])
                i += 1
            else:
                merged.append(R[j])
                j += 1
        merged.extend(L[i:])
        merged.extend(R[j:])
        return merged
    else:
        return arr


def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        heapify(a, n, i)
    for i in range(n - 1, 0, -1):
        a[i], a[0] = a[0], a[i]
        heapify(a, i, 0)
    return a


# -----------------------------
# Utility and Benchmark
# -----------------------------

def measure_time(func, arr):
    start = time.perf_counter()
    func(arr)
    return time.perf_counter() - start


def main():
    size = 2000
    arr = [random.randint(0, 10000) for _ in range(size)]
    print(f"Array size: {size}\n")

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Quick Sort (Standard)": quick_sort_standard,
        "Quick Sort (Random Pivot)": quick_sort_random,
        "Quick Sort (Average Pivot)": quick_sort_average,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort
    }

    results = {}
    for name, func in algorithms.items():
        print(f"Running {name}...")
        elapsed = measure_time(func, arr)
        results[name] = elapsed

    print("\n=== Results ===")
    for name, t in results.items():
        print(f"{name}: {t:.6f} sec")

    # -----------------------------
    # Visualization
    # -----------------------------
    algorithms = list(results.keys())
    times = list(results.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, times, color='skyblue')

    best_idx = times.index(min(times))
    bars[best_idx].set_color('green')

    plt.title(f"Sorting Algorithm Performance (Array size: {size})")
    plt.xlabel("Algorithm")
    plt.ylabel("Execution Time (seconds)")
    plt.xticks(rotation=25, ha='right')

    for i, time_val in enumerate(times):
        plt.text(i, time_val + 0.00002, f"{time_val:.6f}", ha='center', fontsize=9)

    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.show()


if __name__ == "__main__":
    main()

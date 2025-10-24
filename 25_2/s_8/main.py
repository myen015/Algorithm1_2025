# main.py
# Sorting algorithms: Heap Sort, Quick Sort, Merge Sort, Bubble Sort
# Simple benchmark included.

import random
import time

# ===== 1. Heap Sort =====
def heapify(arr, n, i, counter):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    counter[0] += 1
    if l < n and arr[l] > arr[largest]:
        largest = l
    counter[0] += 1
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, counter)

def heap_sort(arr):
    n = len(arr)
    counter = [0]
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, counter)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, counter)
    return counter[0]

# ===== 2. Quick Sort =====
def quick_sort(arr):
    counter = [0]
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            counter[0] += 1
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def qsort(low, high):
        if low < high:
            pi = partition(low, high)
            qsort(low, pi - 1)
            qsort(pi + 1, high)
    qsort(0, len(arr) - 1)
    return counter[0]

# ===== 3. Merge Sort =====
def merge_sort(arr):
    counter = [0]
    def merge_sort_inner(lst):
        if len(lst) > 1:
            mid = len(lst)//2
            L = lst[:mid]
            R = lst[mid:]

            merge_sort_inner(L)
            merge_sort_inner(R)

            i = j = k = 0
            while i < len(L) and j < len(R):
                counter[0] += 1
                if L[i] < R[j]:
                    lst[k] = L[i]
                    i += 1
                else:
                    lst[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                lst[k] = L[i]
                i += 1
                k += 1
            while j < len(R):
                lst[k] = R[j]
                j += 1
                k += 1
    merge_sort_inner(arr)
    return counter[0]

# ===== 4. Bubble Sort (O(n^2)) =====
def bubble_sort(arr):
    n = len(arr)
    counter = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            counter += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return counter

# ===== Benchmark =====
def benchmark():
    algorithms = {
        "Heap Sort": heap_sort,
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
        "Bubble Sort": bubble_sort
    }

    n = 1000
    data = [random.randint(0, 10000) for _ in range(n)]

    results = []
    for name, func in algorithms.items():
        arr_copy = data.copy()
        start = time.time()
        iterations = func(arr_copy)
        duration = time.time() - start
        results.append((name, duration, iterations))

    print("\n=== Benchmark Results ===")
    print(f"{'Algorithm':<15} {'Time (s)':<12} {'Iterations'}")
    print("-" * 40)
    for name, t, c in results:
        print(f"{name:<15} {t:<12.6f} {c}")

if __name__ == "__main__":
    benchmark()

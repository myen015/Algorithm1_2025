import random
import time


# 1. Selection Sort
def selection_sort(data):
    n = len(data)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if data[j] < data[min_index]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]
    return data


# 2. Quick Sort (Random Pivot)
def quick_sort_random(lst):
    if len(lst) < 2:
        return lst
    pivot = random.choice(lst)
    less = [x for x in lst if x < pivot]
    equal = [x for x in lst if x == pivot]
    greater = [x for x in lst if x > pivot]
    return quick_sort_random(less) + equal + quick_sort_random(greater)


# 3. Quick Sort (Median Pivot)
def median(a, b, c):
    return sorted([a, b, c])[1]


def quick_sort_median(lst):
    if len(lst) < 2:
        return lst
    mid = len(lst) // 2
    pivot = median(lst[0], lst[mid], lst[-1])
    left = [x for x in lst if x < pivot]
    center = [x for x in lst if x == pivot]
    right = [x for x in lst if x > pivot]
    return quick_sort_median(left) + center + quick_sort_median(right)


# 4. Merge Sort
def merge(left, right):
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(lst):
    if len(lst) < 2:
        return lst
    mid = len(lst) // 2
    return merge(merge_sort(lst[:mid]), merge_sort(lst[mid:]))


# 5. Heap Sort
def sift_down(arr, n, root):
    largest = root
    left = 2 * root + 1
    right = 2 * root + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != root:
        arr[root], arr[largest] = arr[largest], arr[root]
        sift_down(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        sift_down(arr, i, 0)
    return arr


# Utility: Measure execution time
def measure(func, dataset):
    start = time.perf_counter()
    func(dataset.copy())
    return time.perf_counter() - start


if __name__ == "__main__":
    big_data = [random.randint(0, 10000) for _ in range(10000)]
    small_data = [12, 45, 7, 33, 21, 90, 18, 4, 77, 55]

    algorithms = {
        "Selection Sort": selection_sort,
        "Quick Sort (rand)": quick_sort_random,
        "Quick Sort (median)": quick_sort_median,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort,
    }

    print(f"{'Algorithm':20s} | {'Large (10k)':>12s} | {'Small (10)':>10s}")
    print("-" * 50)

    for name, func in algorithms.items():
        t_large = measure(func, big_data)
        t_small = measure(func, small_data)
        print(f"{name:20s} | {t_large:12.5f}s | {t_small:10.5f}s")

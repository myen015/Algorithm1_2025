import random
import time




# Selection Sort
def selection_sort(data):
    n = len(data)
    for pos in range(n - 1):
        min_pos = pos
        for nxt in range(pos + 1, n):
            if data[nxt] < data[min_pos]:
                min_pos = nxt
        data[pos], data[min_pos] = data[min_pos], data[pos]
    return data


# 2. Quick Sort
def quick_sort_random(lst):
    if len(lst) < 2:
        return lst
    pivot = random.choice(lst)
    less = [x for x in lst if x < pivot]
    equal = [x for x in lst if x == pivot]
    greater = [x for x in lst if x > pivot]
    return quick_sort_random(less) + equal + quick_sort_random(greater)


# 3. Quick Sort
def median(a, b, c):
    if a <= b <= c or c <= b <= a:
        return b
    elif b <= a <= c or c <= a <= b:
        return a
    return c


def quick_sort_median(lst):
    if len(lst) < 2:
        return lst
    mid = len(lst) // 2
    pivot = median(lst[0], lst[mid], lst[-1])
    left = [x for x in lst if x < pivot]
    center = [x for x in lst if x == pivot]
    right = [x for x in lst if x > pivot]
    return quick_sort_median(left) + center + quick_sort_median(right)


# Merge Sort
def merge(left, right):
    merged = []
    i = j = 0
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


# 5.Heap Sort
def sift_down(arr, n, root):
    largest = root
    l = 2 * root + 1
    r = 2 * root + 2

    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r

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




def measure(func, dataset):
    start = time.perf_counter()
    func(dataset.copy())
    return time.perf_counter() - start


if __name__ == "__main__":
    big_data = [random.randint(0, 10000) for _ in range(10000)]
    small_data = [12, 45, 7, 33, 21, 90, 18, 4, 77, 55]

    tests = {
        "Selection Sort": selection_sort,
        "Quick Sort (rand)": quick_sort_random,
        "Quick Sort (median)": quick_sort_median,
        "Merge Sort": merge_sort,
        "Heap Sort": heap_sort,
    }

    for name, func in tests.items():
        t1 = measure(func, big_data)
        t2 = measure(func, small_data)
        print(f"{name:20s} | Large: {t1:.5f}s | Small: {t2:.5f}s")

import time

# ==============================
# 🧪 Данные
# ==============================
arr1 = ["pdf", "apk", "mp3", "docx", "csv", "json", "py", "zip"]
arr2 = ["pdf", "apk", "mp3", "zip", "docx", "csv", "bmp"]
arr3 = ["pdf", "apk", "mp3", "zip", "docx", "csv", "bmp"]

# ==============================
# 🐢 O(n^2) sort (bad algo)
# ==============================
def first_char_ext(filename):
    ext = filename
    return ext[0] if ext else ''

def bad_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(i+1,n):
            if first_char_ext(arr[i]) > first_char_ext(arr[j]):
                arr[i],arr[j] = arr[j],arr[i]
    return arr

# ==============================
# 🪄 Merge sort
# ==============================
def get_ext(filename):
    return filename[0].lower() if filename else ''

def merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if get_ext(left[i]) <= get_ext(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

# ==============================
# ⛰️ Heap sort
# ==============================
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and get_ext(arr[left]) > get_ext(arr[largest]):
        largest = left
    if right < n and get_ext(arr[right]) > get_ext(arr[largest]):
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

# ==============================
# ⏱️ Сравнение времени
# ==============================
def compare():
    # Bad sort
    data = arr1.copy()
    start = time.perf_counter()
    bad_sort(data)
    end = time.perf_counter()
    print(f"Bad sort result: {data}, time: {end - start:.8f} sec")

    # Merge sort
    data = arr2.copy()
    start = time.perf_counter()
    merge_sort(data)
    end = time.perf_counter()
    print(f"Merge sort result: {data}, time: {end - start:.8f} sec")

    # Heap sort
    data = arr3.copy()
    start = time.perf_counter()
    heap_sort(data)
    end = time.perf_counter()
    print(f"Heap sort result: {data}, time: {end - start:.8f} sec")

compare()

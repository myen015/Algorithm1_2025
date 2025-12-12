import random

def bad_sort(arr):
    for i in range(len(arr)-1):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]

def rand_partition(arr, l, r):
    pivot_index = random.randint(l, r)
    arr[r], arr[pivot_index] = arr[pivot_index], arr[r]
    pivot = arr[r]
    i = l
    for j in range(l, r):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i = i + 1
    arr[i], arr[r] = arr[r], arr[i]
    return i

def avg_partition(arr, l, r):
    down = l
    up = r
    mid = l +  (r - l) // 2
    if arr[mid] > arr[up]:
        arr[up], arr[mid] = arr[mid], arr[up]
    if arr[up] < arr[down]:
        arr[up], arr[down] = arr[down], arr[up]
    if arr[mid] < arr[down]:
        arr[down], arr[mid] = arr[mid], arr[down]

    arr[mid], arr[r] = arr[r], arr[mid]
    pivot = arr[r]
    i = l
    for j in range(l, r):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i = i + 1
    arr[i], arr[r] = arr[r], arr[i]
    return i


def quick_sort(arr, l, r):
    if l >= r:
        return
    pivot_index = rand_partition(arr, l, r)
    quick_sort(arr, l, pivot_index-1)
    quick_sort(arr, pivot_index+1, r)

def merge(v, l, m, r, tmp):
    i = l
    j = m + 1
    k = l

    if v[m] <= v[m + 1]:
        return

    while i <= m and j <= r:
        if v[i] <= v[j]:
            tmp[k] = v[i]
            i += 1
        else:
            tmp[k] = v[j]
            j += 1
        k += 1

    while i <= m:
        tmp[k] = v[i]
        i += 1
        k += 1

    while j <= r:
        tmp[k] = v[j]
        j += 1
        k += 1

    for t in range(l, r + 1):
        v[t] = tmp[t]


def merge_sort(v, l, r, tmp):
    if l >= r:
        return
    m = l + (r - l) // 2
    merge_sort(v, l, m, tmp)
    merge_sort(v, m + 1, r, tmp)
    merge(v, l, m, r, tmp)



def heapify(v, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and v[l] > v[largest]:
        largest = l

    if r < n and v[r] > v[largest]:
        largest = r

    if largest != i:
        v[i], v[largest] = v[largest], v[i]
        heapify(v, n, largest)


def heap_sort(v):
    n = len(v)

    for i in range(n // 2 - 1, -1, -1):
        heapify(v, n, i)

    for i in range(n - 1, -1, -1):
        v[0], v[i] = v[i], v[0]
        heapify(v, i, 0)


n = int(input())
a = list(map(int, input().split()))
k = int(input())
tmp = [0] * len(a)
match k:
    case 1:
        bad_sort(a)
        for i in a:
            print(i, end=' ')
    case 2:
        quick_sort(a, 0, len(a)-1)
        for i in a:
            print(i, end=' ')
    case 3:
        heap_sort(a)
        for i in a:
            print(i, end=' ')
    case 4:
        merge_sort(a, 0, len(a)-1, tmp)
        for i in a:
            print(i, end=' ')
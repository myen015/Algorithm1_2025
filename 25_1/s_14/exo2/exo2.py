#Karimov Dias, CSAT-2501

# bad O(n^2) sorting algorithm
s = [4, 5, 2, 1, 6, 7]

def badsort(s):
    count = 0
    n = len(s)
    for i in range(n-1):
        for j in range(n-1-i):
            if s[j] > s[j+1]:
                count += 1
                s[j], s[j+1] = s[j+1], s[j]

badsort(s)
print(*s)


#  quick sort (with random and average pivot)

import random

def quick_sort(s, pivot_type='first'):
    if len(s) <= 1:
        return s

    if pivot_type == 'random':
        elem = random.choice(s)
    elif pivot_type == 'average':
        down, middle, up = min(s), s[len(s)//2], max(s) # initially used: "down, middle, up = partition(s)", but wrote this...
        elem = (down + middle + up) / 3
    else:
        elem = s[0]
    print(f"Pivot ({pivot_type}) = {elem}") # ... and this with the help of chatgpt c:

    left = list(filter(lambda x: x < elem, s))
    center = [i for i in s if i == elem]
    right = list(filter(lambda x: x > elem, s))

    return quick_sort(left, pivot_type) + center + quick_sort(right, pivot_type)

s = random.sample(range(10), 10)
print("Random pivot:", quick_sort(s, 'random'))
print("Average pivot:", quick_sort(s, 'average'))




#  merge sort

def merge(left, right):
    c = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            c.append(left[i])
            i += 1
        else:
            c.append(right[j])
            j += 1
    if i < len(left):
        c += left[i:]
    if j < len(right):
        c += right[j:]
    return c


def merge_sort(s):
    if len(s) == 1:
        return s
    middle = len(s) // 2
    left = merge_sort(s[:middle])
    right = merge_sort(s[middle:])
    return merge(left, right)

print(merge_sort([6, 8, 10, 4, 5, 1, 7]))
# or if you would like to see more clean output, then:
# print(*merge_sort([6, 8, 10, 4, 5, 1, 7]))


#  heap sort

import random #it's way much easier to use random numbers than writing them on ur own

def swap(s, i, j):
    s[i], s[j] = s[j], s[i]


def shiftDown(s, i, upper):
    while(True):
        left, right = i*2+1, i*2+2
        if max(left ,right) < upper:
            if s[i] >= max(s[left], s[right]) : break
            elif s[left] > s[right]:
                swap (s, i, left)
                i = left
            else:
                swap (s, i, right)
                i = right
        elif left < upper:
            if s[left] > s[i]:
                swap (s, i, left)
                i = left
            else: break
        elif right < upper:
            if s[right] > s[i]:
                swap (s, i, right)
                i = right
            else: break
        else: break

def heapsort(s):
    for j in range((len(s)-2)//2, -1, -1):
        shiftDown(s, j, len(s))

    for end in range(len(s)-1, 0, -1):
        swap(s, 0, end)
        shiftDown(s, 0, end)

s=random.sample(range(15), 15) #decided to derive this from the previous algorithm
print("initially s =", *s) # and now i decided to use *
heapsort(s)
print("after heap sorting, s =", *s)



# ==============================================
#  ANALYSIS OF SORTING ALGORITHMS
#  (Using Master theore)
# ==============================================

# ------------------------------
# 1. Badsort or Bubble Sort
# ------------------------------
# Time Complexity:
#   Best Case:      O(n)
#   Average Case:   O(n^2)
#   Worst Case:     O(n^2)
#
# Space Complexity: O(1)
# Master theorem:
#   it's not recursive, so master theorem is not applicable.

# 2. Quick Sort

# Recurrence Relation:
#   T(n) = T(k) + T(n - k - 1) + O(n)

# Time Complexity:
#   Best or average:    O(n log n)
#   Worst Case:         O(n^2)

# Space Complexity:
#   O(log n) on average, O(n) is in worst case

# Master theorem:
#   If partition divides array evenly ==> T(n) = 2T(n/2) + O(n), then: T(n) = O(n log n)

# 3. Merge Sort

# Recurrence Relation:
#   T(n) = 2T(n/2) + O(n)
#
# Time Complexity:
#   Best / Average / Worst: O(n log n)
#
# Space Complexity: O(n)
#
# Master theorem:
#   a = 2, b = 2, f(n) = O(n); ==> n^(log_b a) = n^(log_2 2) = n; ==> T(n) = Θ(n log n)

# 4. Heap Sort
# Time Complexity:
#   Building heap:          O(n)
#   Extracting elements:    O(n log n)
#   Total:                  O(n log n)

# Space Complexity: O(1)

# Master theorem:
#   Not recursive and works by maintaining heap property.
#   Master theorem is not applicable

# Summary Table
# ============================================================================================
# | Algorithm         | Best       | Average     | Worst       | Space      | Master Theorem |
# |------------------:|------------|-------------|-------------|--------    |----------------|
# | Badsort (Bubble)  | O(n)       | O(n^2)      | O(n^2)      | O(1)       | No             |
# | Quick Sort        | O(n log n) | O(n log n)  | O(n^2)      | O(log n)   | Yes            |
# | Merge Sort        | O(n log n) | O(n log n)  | O(n log n)  | O(n)       | Yes            |
# | Heap Sort         | O(n log n) | O(n log n)  | O(n log n)  | O(1)       | No             |
# ============================================================================================
# also, when i was tabulating everything, i was wondering if you are using tabulation or spacing.


def merge_sort(arr):
    # Merge sort
    # Idea: split array to pieces, sort small pieces, then glue back
    # Works fast: O(n log n)

    # If array size is 0 or 1 then nothing to do
    if len(arr) <= 1:
        return arr

    # Find middle to cut array into two parts
    middle = len(arr) // 2

    # Left and right parts
    left_half = arr[:middle]
    right_half = arr[middle:]

    # Sort each part again (recursion)
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    # Join two sorted parts
    return merge(left_sorted, right_sorted)


def merge(left, right):
    # Merge two sorted arrays to one sorted array

    merged = []  # result goes here
    i = 0        # index for left
    j = 0        # index for right

    # Compare items and push smaller one
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i = i + 1
        else:
            merged.append(right[j])
            j = j + 1

    # If something left on the left side, add it
    while i < len(left):
        merged.append(left[i])
        i = i + 1

    # If something left on the right side, add it
    while j < len(right):
        merged.append(right[j])
        j = j + 1

    return merged


def quick_sort(arr):
    # Quick sort
    # Usually fast in real life, but worst case O(n^2)
    # Average is O(n log n)

    # Small arrays are already sorted
    if len(arr) <= 1:
        return arr

    # I pick middle as pivot because simple
    pivot = arr[len(arr) // 2]

    # Make three lists: < pivot, = pivot, > pivot
    smaller = []
    equal = []
    larger = []

    for element in arr:
        if element < pivot:
            smaller.append(element)
        elif element == pivot:
            equal.append(element)
        else:
            larger.append(element)

    # Sort left and right parts and then join all
    return quick_sort(smaller) + equal + quick_sort(larger)


def insertion_sort(arr):
    # Insertion sort
    # Not fast for big arrays (O(n^2))
    # But nice when array is small or almost sorted

    # Start from second element (first is like sorted)
    for i in range(1, len(arr)):
        current_value = arr[i]  # the value we want to insert to correct place
        position = i - 1

        # Move big elements to the right side to make space
        while position >= 0 and arr[position] > current_value:
            arr[position + 1] = arr[position]
            position = position - 1

        # Put current value to its place
        arr[position + 1] = current_value

    return arr


def heap_sort(arr):
    # Heap sort
    # Uses binary heap (max-heap here)
    # Time is O(n log n)

    def heapify(array, size, root_index):
        # Keep heap rule: parent should be >= children
        largest = root_index
        left_child = 2 * root_index + 1
        right_child = 2 * root_index + 2

        # If left child exists and bigger than current largest
        if left_child < size and array[left_child] > array[largest]:
            largest = left_child

        # Same for right child
        if right_child < size and array[right_child] > array[largest]:
            largest = right_child

        # If root is not the largest, swap and fix below
        if largest != root_index:
            array[root_index], array[largest] = array[largest], array[root_index]
            # Fix the sub-tree after swap
            heapify(array, size, largest)

    n = len(arr)

    # 1) Build max-heap from the array
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # 2) Take max to the end one by one
    for i in range(n - 1, 0, -1):
        # Swap first (max) with last unsorted
        arr[0], arr[i] = arr[i], arr[0]
        # Fix the heap for the smaller size
        heapify(arr, i, 0)

    return arr


# ============================================
# TESTING THE ALGORITHMS
# ============================================

# My test array
my_test_array = [64, 34, 25, 12, 22, 11, 90]

print("Original array:", my_test_array)
print("-" * 50)

# Test merge sort
result1 = merge_sort(my_test_array.copy())
print("Merge Sort result:    ", result1)

# Test quick sort
result2 = quick_sort(my_test_array.copy())
print("Quick Sort result:    ", result2)

# Test insertion sort
result3 = insertion_sort(my_test_array.copy())
print("Insertion Sort result:", result3)

# Test heap sort
result4 = heap_sort(my_test_array.copy())
print("Heap Sort result:     ", result4)

print("-" * 50)

# One more test: already sorted array
sorted_array = [1, 2, 3, 4, 5]
print("\nTesting with already sorted array:", sorted_array)
print("Insertion sort (should be fast):", insertion_sort(sorted_array.copy()))

# Reverse sorted array (some algorithms hate this case)
reverse_array = [9, 7, 5, 3, 1]
print("\nTesting with reverse sorted array:", reverse_array)
print("Quick sort:", quick_sort(reverse_array.copy()))
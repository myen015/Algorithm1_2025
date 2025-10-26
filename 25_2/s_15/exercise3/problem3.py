def find_min_linear(arr):
    min_val = arr[0]
    for x in arr:
        if x < min_val:
            min_val = x
    return min_val

def find_min_dc(arr, left, right):
    if left == right:
        return arr[left]
    if right == left + 1:
        return arr[left] if arr[left] < arr[right] else arr[right]
    mid = (left + right) // 2
    left_min = find_min_dc(arr, left, mid)
    right_min = find_min_dc(arr, mid + 1, right)
    return left_min if left_min < right_min else right_min

arr = [12, 5, 7, -3, 9, 0, 4]
print("Array:", arr)
print("Linear Search Min:", find_min_linear(arr))
print("Divide & Conquer Min:", find_min_dc(arr, 0, len(arr) - 1))

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
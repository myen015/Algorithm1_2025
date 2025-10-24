import random

def quick_sort(s, pivot_type='first'):
    if len(s) <= 1:
        return s

    if pivot_type == 'random':
        elem = random.choice(s)
    elif pivot_type == 'average':
        down, middle, up = min(s), s[len(s)//2], max(s)
        elem = (down + middle + up) / 3
    else:
        elem = s[0]
    print(f"Pivot ({pivot_type}) = {elem}")

    left = list(filter(lambda x: x < elem, s))
    center = [i for i in s if i == elem]
    right = list(filter(lambda x: x > elem, s))

    return quick_sort(left, pivot_type) + center + quick_sort(right, pivot_type)

#Testing:

s = random.sample(range(10), 10)
print("Random pivot:", quick_sort(s, 'random'))
print("Average pivot:", quick_sort(s, 'average'))

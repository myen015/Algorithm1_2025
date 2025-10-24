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

s=random.sample(range(15), 15)
print("initially s =", *s)
heapsort(s)
print("after heap sorting, s =", *s)
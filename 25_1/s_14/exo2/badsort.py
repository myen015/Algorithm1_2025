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

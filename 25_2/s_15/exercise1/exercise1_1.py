def divide2(v, L=0, R=None):
    if R is None:
        R = len(v) - 1
    if L == R:
        return v[L]
    M = (L + R) // 2
    divide2(v, L, M)
    divide2(v, M + 1, R)


def divide3(v, L=0, R=None):
    if R is None:
        R = len(v) - 1
    if L == R:
        return v[L]
    size = (R - L + 1) // 3
    M1 = L + size
    M2 = L + 2 * size
    divide3(v, L, M1)
    divide3(v, M1 + 1, M2)
    divide3(v, M2 + 1, R)


def dividefind2(v, L=0, R=None):
    if R is None:
        R = len(v) - 1
    if L == R:
        return L if v[L] == 1 else None

    M = (L + R) // 2
    res_left = dividefind2(v, L, M)
    if res_left is not None:
        return res_left
    return dividefind2(v, M + 1, R)


if __name__ == "__main__":
    v = [0,0,0,0,1,0,0,0]
    print("Index of 1 =", dividefind2(v))

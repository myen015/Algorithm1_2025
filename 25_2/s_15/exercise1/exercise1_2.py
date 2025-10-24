def classical_mult(a, b):
    """Recursive multiplication with 4 subcalls: O(n^2)"""
    a, b = str(a), str(b)
    n = max(len(a), len(b))
    if n == 1:
        return int(a) * int(b)

    n2 = n // 2
    a = a.zfill(n)
    b = b.zfill(n)

    a0, a1 = int(a[:-n2]), int(a[-n2:])
    b0, b1 = int(b[:-n2]), int(b[-n2:])

    p1 = classical_mult(a0, b0)
    p2 = classical_mult(a0, b1)
    p3 = classical_mult(a1, b0)
    p4 = classical_mult(a1, b1)

    return p1 * 10**(2*n2) + (p2+p3) * 10**n2 + p4


def karatsuba(a, b):
    """Karatsuba multiplication: 3 subcalls → O(n^(log2(3)))"""
    a, b = str(a), str(b)
    n = max(len(a), len(b))
    if n == 1:
        return int(a) * int(b)

    n2 = n // 2
    a = a.zfill(n)
    b = b.zfill(n)

    a0, a1 = int(a[:-n2]), int(a[-n2:])
    b0, b1 = int(b[:-n2]), int(b[-n2:])

    p1 = karatsuba(a0, b0)
    p2 = karatsuba(a1, b1)
    p3 = karatsuba(a0+a1, b0+b1)

    return p1 * 10**(2*n2) + (p3 - p1 - p2) * 10**n2 + p2


if __name__ == "__main__":
    a = 123456
    b = 789123
    print("Classical =", classical_mult(a, b))
    print("Karatsuba =", karatsuba(a, b))

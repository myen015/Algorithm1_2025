import random, time

# ---------- Bubble Sort (O(n²)) ----------
def bubble_sort(a):
    a = a[:]
    n = len(a)
    it = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            it += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a, it


# ---------- Merge Sort (O(n log n)) ----------
def merge_sort(a):
    it = [0]
    def merge(L, R):
        i = j = 0
        out = []
        while i < len(L) and j < len(R):
            it[0] += 1
            if L[i] <= R[j]:
                out.append(L[i]); i += 1
            else:
                out.append(R[j]); j += 1
        out.extend(L[i:]); out.extend(R[j:])
        return out
    def divide(x):
        if len(x) <= 1:
            return x
        m = len(x)//2
        return merge(divide(x[:m]), divide(x[m:]))
    return divide(a[:]), it[0]


# ---------- Quick Sort (O(n log n) avg) ----------
def quick_sort(a):
    it = [0]
    def qs(x):
        if len(x) <= 1:
            return x
        p = x[len(x)//2]
        L = [v for v in x if v < p]
        E = [v for v in x if v == p]
        G = [v for v in x if v > p]
        it[0] += len(x)
        return qs(L) + E + qs(G)
    return qs(a[:]), it[0]


# ---------- Heap Sort (O(n log n)) ----------
def heap_sort(a):
    a = a[:]
    it = [0]
    def heapify(n, i):
        largest = i
        l, r = 2*i+1, 2*i+2
        if l < n and a[l] > a[largest]: largest = l
        if r < n and a[r] > a[largest]: largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            heapify(n, largest)
        it[0] += 1
    n = len(a)
    for i in range(n//2-1, -1, -1): heapify(n, i)
    for i in range(n-1, 0, -1):
        a[0], a[i] = a[i], a[0]
        heapify(i, 0)
    return a, it[0]


# ---------- Benchmark ----------
def benchmark():
    arr = [random.randint(0, 10000) for _ in range(1000)]
    algos = [("Bubble", bubble_sort), ("Merge", merge_sort), ("Quick", quick_sort), ("Heap", heap_sort)]
    for name, fn in algos:
        start = time.time()
        _, it = fn(arr)
        dur = time.time() - start
        print(f"{name:6} | time={dur:.4f}s | iterations={it}")

if __name__ == "__main__":
    benchmark()

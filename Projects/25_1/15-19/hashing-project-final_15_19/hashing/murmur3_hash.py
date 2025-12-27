def murmur3_32(text: str, seed: int = 0) -> int:
    data = text.encode("utf-8")
    length = len(data)
    h = seed

    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    rounded = length & ~0x3
    for i in range(0, rounded, 4):
        k = (data[i] |
             (data[i+1] << 8) |
             (data[i+2] << 16) |
             (data[i+3] << 24))

        k = (k * c1) & 0xFFFFFFFF
        k = ((k << 15) | (k >> 17)) & 0xFFFFFFFF
        k = (k * c2) & 0xFFFFFFFF

        h ^= k
        h = ((h << 13) | (h >> 19)) & 0xFFFFFFFF
        h = (h * 5 + 0xe6546b64) & 0xFFFFFFFF

    k = 0
    tail = length & 3
    if tail == 3:
        k ^= data[rounded+2] << 16
    if tail >= 2:
        k ^= data[rounded+1] << 8
    if tail >= 1:
        k ^= data[rounded]

        k = (k * c1) & 0xFFFFFFFF
        k = ((k << 15) | (k >> 17)) & 0xFFFFFFFF
        k = (k * c2) & 0xFFFFFFFF
        h ^= k

    h ^= length
    h ^= (h >> 16)
    h = (h * 0x85ebca6b) & 0xFFFFFFFF
    h ^= (h >> 13)
    h = (h * 0xc2b2ae35) & 0xFFFFFFFF
    h ^= (h >> 16)

    return h

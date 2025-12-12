import heapq
from collections import Counter



#  Build Huffman Tree

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    # For priority queue
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(ch, fr) for ch, fr in freq.items()]
    heapq.heapify(heap)

    # Combine nodes until one remains
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]  # root



# Generate Huffman Codes

def build_codes(root):
    codes = {}

    def traverse(node, current_code):
        if not node:
            return
        if node.char is not None:
            codes[node.char] = current_code
            return
        traverse(node.left, current_code + "0")
        traverse(node.right, current_code + "1")

    traverse(root, "")
    return codes



# Encoding

def huffman_encode(text, codes):
    return "".join(codes[ch] for ch in text)



# Decoding

def huffman_decode(encoded_text, root):
    decoded = ""
    node = root

    for bit in encoded_text:
        node = node.left if bit == "0" else node.right

        if node.char is not None:
            decoded += node.char
            node = root

    return decoded



# MAIN PROGRAM

text = input("Enter any text: ")

# Build tree
root = build_huffman_tree(text)

#  Build code table
codes = build_codes(root)

print("\nHuffman Codes:")
for ch, code in codes.items():
    print(f"{repr(ch)} : {code}")

# Encode
encoded = huffman_encode(text, codes)
print("\nEncoded bitstring:")
print(encoded)

# Decode
decoded = huffman_decode(encoded, root)
print("\nDecoded text:")
print(decoded)

# Check correctness
print("\n--------------------------------")
if decoded == text:
    print("✔ Decoding successful: output matches the original!")
else:
    print("✘ ERROR: Decoded text does NOT match the original!")
print("--------------------------------")

# Show efficiency
original_bits = len(text) * 8
compressed_bits = len(encoded)

print(f"\nOriginal size:    {original_bits} bits")
print(f"Compressed size:  {compressed_bits} bits")
print(f"Compression ratio: {original_bits / compressed_bits:.2f}x")

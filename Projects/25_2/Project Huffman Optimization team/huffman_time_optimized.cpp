// Member IDs 3, 10, 16, 19

#include <iostream>
#include <vector>
#include <array>
#include <queue>
#include <string>
#include <chrono>
#include <windows.h>
#include <psapi.h>

using namespace std;
using Clock = chrono::high_resolution_clock;

size_t getMemoryBytes() {
    PROCESS_MEMORY_COUNTERS_EX pmc;
    GetProcessMemoryInfo(
        GetCurrentProcess(),
        (PROCESS_MEMORY_COUNTERS*)&pmc,
        sizeof(pmc)
    );
    return pmc.PrivateUsage;
}

double getMemoryMB() {
    return getMemoryBytes() / (1024.0 * 1024.0);
}

struct Node {
    int left;
    int right;
    int freq;
    unsigned char ch;
    bool is_leaf;
    Node() : left(-1), right(-1), freq(0), ch(0), is_leaf(false) {}
};

// Структура для хранения кода: биты и длина
struct CodeInfo {
    uint32_t bits;
    int len;
    CodeInfo() : bits(0), len(0) {}
};

// Подсчет частоты символов
array<int,256> countFrequencies(const string& text) {
    array<int,256> freq;
    freq.fill(0);
    for (unsigned char c : text) ++freq[c];
    return freq;
}

// Построение дерева Хаффмана
int buildHuffmanTreeIndices(const array<int,256>& freq, vector<Node>& nodes) {
    struct Item { int freq; int idx; };
    struct Cmp { bool operator()(const Item& a, const Item& b) const { return a.freq > b.freq; } };
    priority_queue<Item, vector<Item>, Cmp> pq;

    nodes.clear();
    nodes.reserve(512);

    for (int i = 0; i < 256; ++i) {
        if (freq[i] > 0) {
            Node n;
            n.left = -1; n.right = -1; n.freq = freq[i];
            n.ch = static_cast<unsigned char>(i);
            n.is_leaf = true;
            nodes.push_back(n);
            pq.push({n.freq, static_cast<int>(nodes.size()-1)});
        }
    }
    if (pq.empty()) return -1;
    if (pq.size() == 1) {
        Item only = pq.top(); pq.pop();
        Node parent;
        parent.left = only.idx;
        parent.right = -1;
        parent.freq = nodes[only.idx].freq;
        parent.is_leaf = false;
        nodes.push_back(parent);
        return static_cast<int>(nodes.size()-1);
    }

    while (pq.size() > 1) {
        Item a = pq.top(); pq.pop();
        Item b = pq.top(); pq.pop();
        Node parent;
        parent.left = a.idx;
        parent.right = b.idx;
        parent.freq = a.freq + b.freq;
        parent.is_leaf = false;
        nodes.push_back(parent);
        int pidx = static_cast<int>(nodes.size()-1);
        pq.push({parent.freq, pidx});
    }
    return pq.top().idx;
}

// Генерация кодов в виде битовых паттернов
void generateCodesFast(const vector<Node>& nodes, int root, array<CodeInfo,256>& codes) {
    for (auto &c : codes) { c.bits = 0; c.len = 0; }
    if (root < 0) return;
    
    struct StackItem {
        int idx;
        uint32_t code;
        int len;
    };
    vector<StackItem> stack;
    stack.reserve(512);
    stack.push_back({root, 0, 0});
    
    while (!stack.empty()) {
        StackItem item = stack.back();
        stack.pop_back();
        const Node& node = nodes[item.idx];
        
        if (node.is_leaf && node.left == -1 && node.right == -1) {
            if (item.len == 0) {
                codes[node.ch].bits = 0;
                codes[node.ch].len = 1;
            } else {
                codes[node.ch].bits = item.code;
                codes[node.ch].len = item.len;
            }
            continue;
        }
        
        if (node.right != -1) {
            stack.push_back({node.right, (item.code << 1) | 1, item.len + 1});
        }
        if (node.left != -1) {
            stack.push_back({node.left, item.code << 1, item.len + 1});
        }
    }
}

// Запись битов
struct BitWriter {
    vector<uint8_t> out;
    uint32_t buf = 0;
    int bitpos = 0;
    
    BitWriter(size_t reserveBytes = 0) {
        if (reserveBytes) out.reserve(reserveBytes);
    }
    
    // Запись нескольких битов сразу
    void write_bits(uint32_t bits, int len) {
        buf |= (bits << bitpos);
        bitpos += len;
        while (bitpos >= 8) {
            out.push_back(static_cast<uint8_t>(buf & 0xFF));
            buf >>= 8;
            bitpos -= 8;
        }
    }
    
    void flush() {
        if (bitpos > 0) {
            out.push_back(static_cast<uint8_t>(buf & 0xFF));
            buf = 0;
            bitpos = 0;
        }
    }
};

// Чтение битов
struct BitReader {
    const uint8_t* data = nullptr;
    size_t byteCount = 0;
    size_t byteIdx = 0;
    uint32_t buf = 0;
    int bitsInBuf = 0;
    
    void init(const vector<uint8_t>& packed) {
        data = packed.data();
        byteCount = packed.size();
        byteIdx = 0;
        buf = 0;
        bitsInBuf = 0;
    }
    
    void ensure(int k) {
        while (bitsInBuf < k && byteIdx < byteCount) {
            buf |= (uint32_t(data[byteIdx++]) << bitsInBuf);
            bitsInBuf += 8;
        }
    }
    
    inline int read_bit() {
        if (bitsInBuf == 0) ensure(1);
        if (bitsInBuf == 0) return -1;
        int b = buf & 1u;
        buf >>= 1;
        --bitsInBuf;
        return b;
    }
};

// Быстрое кодирование
vector<uint8_t> encodeFast(const string& text, const array<CodeInfo,256>& codes, const array<int,256>& freq, size_t& outBits) {
    size_t totalBits = 0;
    for (int i = 0; i < 256; ++i) {
        if (freq[i] > 0) {
            totalBits += static_cast<size_t>(freq[i]) * codes[i].len;
        }
    }
    
    size_t bytesReserve = (totalBits + 7) / 8;
    BitWriter bw(bytesReserve ? bytesReserve : 1);

    for (unsigned char c : text) {
        const CodeInfo& code = codes[c];
        bw.write_bits(code.bits, code.len);
    }
    
    bw.flush();
    outBits = totalBits;
    return move(bw.out);
}

// Быстрое декодирование
string decodeFast(const vector<uint8_t>& packed, size_t bitCount, const vector<Node>& nodes, int root) {
    if (root < 0) return {};
    if (nodes[root].is_leaf && nodes[root].left != -1 && nodes[root].right == -1) {
        unsigned char ch = nodes[nodes[root].left].ch;
        return string(bitCount, (char)ch);
    }
    
    string decoded;
    decoded.reserve(bitCount / 4 + 1);
    
    BitReader br;
    br.init(packed);
    br.ensure(1);

    int cur = root;
    size_t produced = 0;
    while (produced < bitCount) {
        br.ensure(1);
        if (br.bitsInBuf == 0) break;
        int bit = br.read_bit();
        if (bit < 0) break;
        ++produced;
        
        cur = (bit == 0) ? nodes[cur].left : nodes[cur].right;
        if (cur == -1) break;
        
        if (nodes[cur].is_leaf && nodes[cur].left == -1 && nodes[cur].right == -1) {
            decoded.push_back((char)nodes[cur].ch);
            cur = root;
        }
    }
    return decoded;
}

int main() {
    // Готовим большой тест
    string base = "huffman coding is fun ";
    int repeats = 200000;
    string text;
    text.reserve(base.size() * repeats);
    for (int i = 0; i < repeats; ++i) text += base;

    cout << "Time-optimized program running on " << text.size() << " chars\n";
    cout << "Start memory: " << getMemoryMB() << " MB\n\n";

    auto t0 = Clock::now();
    auto freq = countFrequencies(text);
    auto t1 = Clock::now();
    cout << "Frequencies: " << chrono::duration_cast<chrono::milliseconds>(t1 - t0).count() << " ms\n";
    cout << "Memory after freq: " << getMemoryMB() << " MB\n\n";

    vector<Node> nodes;
    auto root = buildHuffmanTreeIndices(freq, nodes);
    auto t2 = Clock::now();
    cout << "Tree build: " << chrono::duration_cast<chrono::milliseconds>(t2 - t1).count() << " ms\n";
    cout << "Memory after tree: " << getMemoryMB() << " MB\n\n";

    array<CodeInfo,256> codes;
    generateCodesFast(nodes, root, codes);
    auto t3 = Clock::now();
    cout << "Codes generation: " << chrono::duration_cast<chrono::milliseconds>(t3 - t2).count() << " ms\n";
    cout << "Memory after codes: " << getMemoryMB() << " MB\n\n";

    size_t outBits = 0;
    auto packed = encodeFast(text, codes, freq, outBits);
    auto t4 = Clock::now();
    cout << "Encode (fast bitwriter): " << chrono::duration_cast<chrono::milliseconds>(t4 - t3).count() << " ms\n";
    cout << "Memory after encode: " << getMemoryMB() << " MB\n\n";

    auto decoded = decodeFast(packed, outBits, nodes, root);
    auto t5 = Clock::now();
    cout << "Decode (fast walk): " << chrono::duration_cast<chrono::milliseconds>(t5 - t4).count() << " ms\n";
    cout << "Memory after decode: " << getMemoryMB() << " MB\n\n";

    cout << "Total: " << chrono::duration_cast<chrono::milliseconds>(t5 - t0).count() << " ms\n";
    cout << "Memory final: " << getMemoryMB() << " MB\n";

    return 0;
}

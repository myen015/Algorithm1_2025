// Member IDs 3, 10, 16, 19

#include <iostream>
#include <queue>
#include <unordered_map>
#include <string>
#include <chrono>
#include <windows.h>
#include <psapi.h>
using namespace std;

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
    char character;           
    int frequency;           
    Node* left;              
    Node* right;         
    
    Node(char ch, int freq) {
        character = ch;
        frequency = freq;
        left = nullptr;
        right = nullptr;
    }
    
    Node(int freq, Node* l, Node* r) {
        character = '\0';    
        frequency = freq;
        left = l;
        right = r;
    }
};


struct CompareNodes {
    bool operator()(Node* a, Node* b) {
        return a->frequency > b->frequency;  
    }
};

unordered_map<char, int> countFrequencies(string text) {
    unordered_map<char, int> freqMap;
    
    for (char ch : text) {
        freqMap[ch]++;  
    }
    
    return freqMap;
}

Node* buildHuffmanTree(unordered_map<char, int>& frequencies) {
    priority_queue<Node*, vector<Node*>, CompareNodes> pq;
    
    for (auto pair : frequencies) {
        Node* newNode = new Node(pair.first, pair.second);
        pq.push(newNode);
    }
    
    while (pq.size() > 1) {
        Node* left = pq.top();
        pq.pop();
        Node* right = pq.top();
        pq.pop();
        
        int combinedFreq = left->frequency + right->frequency;
        Node* parent = new Node(combinedFreq, left, right);
        
        pq.push(parent);
    }
    
    return pq.top();
}


void generateCodes(Node* root, string code, unordered_map<char, string>& huffmanCodes) {
    if (root == nullptr) {
        return;
    }
    
    if (root->left == nullptr && root->right == nullptr) {
        huffmanCodes[root->character] = code;
        return;
    }
    
    generateCodes(root->left, code + "0", huffmanCodes);
    
    generateCodes(root->right, code + "1", huffmanCodes);
}

string encode(string text, unordered_map<char, string>& huffmanCodes) {
    string encoded = "";
    
    for (char ch : text) {
        encoded += huffmanCodes[ch];
    }
    
    return encoded;
}

string decode(string encoded, Node* root) {
    string decoded = "";
    Node* current = root;
    
    for (char bit : encoded) {
        if (bit == '0') {
            current = current->left;
        } else {
            current = current->right;
        }
        
        if (current->left == nullptr && current->right == nullptr) {
            decoded += current->character;
            current = root;  
        }
    }
    
    return decoded;
}

void printCodes(unordered_map<char, string>& codes) {
    cout << "\nHuffman Codes:\n";
    cout << "Character | Code\n";
    cout << "----------|-------\n";
    for (auto pair : codes) {
        cout << "    " << pair.first << "     | " << pair.second << "\n";
    }
}

int main() {
    using Clock = chrono::high_resolution_clock; 

    // Готовим большой тест
    string base = "huffman coding is fun ";
    int repeats = 200000;
    string text;
    text.reserve(base.size() * repeats);
    for (int i = 0; i < repeats; ++i) text += base;

    cout << "Original program running on " << text.size() << " chars\n";
    cout << "Start memory: " << getMemoryMB() << " MB\n\n";

    auto t0 = Clock::now();
    auto freq = countFrequencies(text);
    auto t1 = Clock::now();
    cout << "Frequencies: " << chrono::duration_cast<chrono::milliseconds>(t1 - t0).count() << " ms\n";
    cout << "Memory after freq: " << getMemoryMB() << " MB\n\n";

    auto root = buildHuffmanTree(freq);
    auto t2 = Clock::now();
    cout << "Tree build: " << chrono::duration_cast<chrono::milliseconds>(t2 - t1).count() << " ms\n";
    cout << "Memory after tree: " << getMemoryMB() << " MB\n\n";

    unordered_map<char, string> codes;
    generateCodes(root, "", codes);
    auto t3 = Clock::now();
    cout << "Codes generation: " << chrono::duration_cast<chrono::milliseconds>(t3 - t2).count() << " ms\n";
    cout << "Memory after codes: " << getMemoryMB() << " MB\n\n";

    string encoded = encode(text, codes);
    auto t4 = Clock::now();
    cout << "Encode: " << chrono::duration_cast<chrono::milliseconds>(t4 - t3).count() << " ms\n";
    cout << "Memory after encode: " << getMemoryMB() << " MB\n\n";

    string decoded = decode(encoded, root);
    auto t5 = Clock::now();
    cout << "Decode: " << chrono::duration_cast<chrono::milliseconds>(t5 - t4).count() << " ms\n";
    cout << "Memory after decode: " << getMemoryMB() << " MB\n\n";

    cout << "Total: " << chrono::duration_cast<chrono::milliseconds>(t5 - t0).count() << " ms\n";
    cout << "Total: " << getMemoryMB() << " MB\n";

    return 0;
}
#include <bits/stdc++.h>
using namespace std;

struct Node {
    double weight;
    vector<Node*> children;
    Node(double w = 0.0) : weight(w) {}
};

Node* GenerateTree(int depth, int n, double initialWeight) {
    Node* node = new Node(initialWeight);
    if (depth == 0) return node;
    node->children.resize(n);
    double childWeight = initialWeight / static_cast<double>(n);
    for (int i = 0; i < n; ++i) node->children[i] = GenerateTree(depth - 1, n, childWeight);
    return node;
}

double DFSRecursive(Node* node) {
    if (!node) return 0.0;
    double sum = node->weight;
    for (auto c : node->children) sum += DFSRecursive(c);
    return sum;
}

double DFSFlipSign(Node* node) {
    if (!node) return 0.0;
    node->weight = -node->weight;
    double sum = node->weight;
    for (auto c : node->children) sum += DFSFlipSign(c);
    return sum;
}

double BFSIterative(Node* root) {
    if (!root) return 0.0;
    double sum = 0.0;
    deque<Node*> q;
    q.push_back(root);
    while (!q.empty()) {
        Node* node = q.front(); q.pop_front();
        sum += node->weight;
        for (auto c : node->children) if (c) q.push_back(c);
    }
    return sum;
}

double BFSFlipSign(Node* root) {
    if (!root) return 0.0;
    double sum = 0.0;
    deque<Node*> q;
    q.push_back(root);
    while (!q.empty()) {
        Node* node = q.front(); q.pop_front();
        node->weight = -node->weight;
        sum += node->weight;
        for (auto c : node->children) if (c) q.push_back(c);
    }
    return sum;
}

double BFSRecursiveHelper(deque<Node*> q, double sum) {
    if (q.empty()) return sum;
    Node* node = q.front(); q.pop_front();
    sum += node->weight;
    for (auto c : node->children) if (c) q.push_back(c);
    return BFSRecursiveHelper(q, sum);
}

double BFSRecursive(Node* root) {
    if (!root) return 0.0;
    deque<Node*> q;
    q.push_back(root);
    return BFSRecursiveHelper(q, 0.0);
}

void PrintTree(Node* node, const string& prefix, bool isLast) {
    if (!node) return;
    string connector = isLast ? "+--" : "|--";
    cout << prefix << connector << " " << fixed << setprecision(6) << node->weight << "\n";
    string newPrefix = prefix + (isLast ? "    " : "|   ");
    for (size_t i = 0; i < node->children.size(); ++i) PrintTree(node->children[i], newPrefix, i + 1 == node->children.size());
}

bool approxEqual(double a, double b) {
    return fabs(a - b) < 1e-9;
}

int main() {
    cout << "PROBLEM 1: N-ary Tree with Weight Distribution\n";
    cout << string(50, '=') << "\n\n";
    vector<int> testCases = {2, 3, 4, 5};
    const int depth = 3; // levels below root: depth. total levels = depth + 1
    for (int n : testCases) {
        cout << "--- Test Case: n = " << n << " (depth = " << depth << ") ---\n\n";
        double initialWeight = 1.0 / static_cast<double>(depth + 1); // so total sum == 1.0
        Node* tree = GenerateTree(depth, n, initialWeight);
        cout << "Tree Structure:" << endl;
        PrintTree(tree, "", true);

        double dfsSum = DFSRecursive(tree);
        cout << "\n3. DFS Recursive Sum: " << fixed << setprecision(10) << dfsSum << "\n";
        cout << (approxEqual(dfsSum, 1.0) ? "   OK: Sum equals 1\n" : "   ERROR\n");

        double bfsIterSum = BFSIterative(tree);
        cout << "\n4. BFS Iterative Sum: " << fixed << setprecision(10) << bfsIterSum << "\n";
        cout << (approxEqual(bfsIterSum, 1.0) ? "   OK: Sum equals 1\n" : "   ERROR\n");

        double bfsRecSum = BFSRecursive(tree);
        cout << "\n6. BFS Recursive Sum: " << fixed << setprecision(10) << bfsRecSum << "\n";
        cout << (approxEqual(bfsRecSum, 1.0) ? "   OK: Sum equals 1\n" : "   ERROR\n");

        Node* tree2 = GenerateTree(depth, n, initialWeight);
        cout << "\n5. Testing Sign Flip:" << endl;
        double dfsFlip1 = DFSFlipSign(tree2);
        cout << "   First DFS (flip signs): " << fixed << setprecision(10) << dfsFlip1 << "\n";
        cout << (approxEqual(dfsFlip1, -1.0) ? "   OK: Sum equals -1\n" : "   ERROR\n");
        double dfsFlip2 = DFSFlipSign(tree2);
        cout << "   Second DFS (flip again): " << fixed << setprecision(10) << dfsFlip2 << "\n";
        cout << (approxEqual(dfsFlip2, 1.0) ? "   OK: Sum equals 1\n" : "   ERROR\n");

        Node* tree3 = GenerateTree(depth, n, initialWeight);
        double bfsFlip1 = BFSFlipSign(tree3);
        cout << "\n   First BFS (flip signs): " << fixed << setprecision(10) << bfsFlip1 << "\n";
        cout << (approxEqual(bfsFlip1, -1.0) ? "   OK: Sum equals -1\n" : "   ERROR\n");
        double bfsFlip2 = BFSFlipSign(tree3);
        cout << "   Second BFS (flip again): " << fixed << setprecision(10) << bfsFlip2 << "\n";
        cout << (approxEqual(bfsFlip2, 1.0) ? "   OK: Sum equals 1\n" : "   ERROR\n");

        cout << "\n";
    }
    cout << string(50, '=') << "\n";
    cout << "7. Why BFS Recursive is NOT Recommended:\n";
    cout << string(50, '=') << "\n";
    cout << "DFS is naturally recursive; BFS uses a queue and iterative form is clearer and more efficient.\n";
}

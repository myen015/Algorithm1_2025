#include <iostream>
#include <vector>
#include <queue>
#include <iomanip>

using namespace std;

class Node {
public:
    double weight;
    vector<Node*> children;

    Node(double w) : weight(w) {}
};


Node* buildTree(int depth, double w, int n) {
    Node* root = new Node(w);

    if (depth == 0)
        return root;

    for (int i = 0; i < n; i++)
        root->children.push_back(buildTree(depth - 1, w / n, n));

    return root;
}

// DFS суммирование
double dfsSum(Node* root) {
    double sum = root->weight;
    for (auto child : root->children)
        sum += dfsSum(child);
    return sum;
}

// BFS суммирование
double bfsSum(Node* root) {
    queue<Node*> q;
    q.push(root);
    double sum = 0;

    while (!q.empty()) {
        Node* current = q.front(); q.pop();
        sum += current->weight;
        for (auto child : current->children)
            q.push(child);
    }
    return sum;
}

// DFS с инвертированием весов
double dfsFlip(Node* root) {
    root->weight = -root->weight;
    double sum = root->weight;
    for (auto child : root->children)
        sum += dfsFlip(child);
    return sum;
}

// BFS с инвертированием весов
double bfsFlip(Node* root) {
    queue<Node*> q;
    q.push(root);
    double sum = 0;

    while (!q.empty()) {
        Node* current = q.front(); q.pop();
        current->weight = -current->weight;
        sum += current->weight;
        for (auto child : current->children)
            q.push(child);
    }
    return sum;
}

// Рекурсивный BFS (уровень за уровнем)
double bfsRecursive(vector<Node*> level) {
    if (level.empty())
        return 0;

    vector<Node*> nextLevel;
    double sum = 0;

    for (auto node : level) {
        sum += node->weight;
        for (auto child : node->children)
            nextLevel.push_back(child);
    }

    return sum + bfsRecursive(nextLevel);
}


void printTree(Node* node, string prefix = "", bool isLast = true) {
   
    cout << prefix;

    cout << (isLast ? "└── " : "├── ") << node->weight << endl;

   
    string childPrefix = prefix + (isLast ? "    " : "│   ");

    for (size_t i = 0; i < node->children.size(); i++) {
        printTree(node->children[i], childPrefix, i == node->children.size() - 1);
    }
}

int main() {
    int n = 5;
    int depth = 3;
    double rootWeight = 1.0 / (depth + 1);

    Node* root = buildTree(depth, rootWeight, n);

    cout << fixed << setprecision(8);

    cout << "\nTree structure:\n";
    printTree(root);

    cout << "\n---------------------------------\n";
    cout << "DFS sum: " << dfsSum(root) << endl;
    cout << "BFS sum: " << bfsSum(root) << endl;

    cout << "\nDFS flip #1: " << dfsFlip(root) << endl;
    cout << "BFS flip #1: " << bfsFlip(root) << endl;

    cout << "\nDFS flip #2: " << dfsFlip(root) << endl;
    cout << "BFS flip #2: " << bfsFlip(root) << endl;

    cout << "\nRecursive BFS sum: " << bfsRecursive({root}) << endl;
    cout << "\n---------------------------------\n";

    return 0;
}

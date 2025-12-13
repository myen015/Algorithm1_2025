#include <bits/stdc++.h>
using namespace std;

//1
struct Node {
    double weight;
    vector<Node*> children;

    Node(double w = 0.0) : weight(w) {}
};

Node* buildTree(int depth, int n, double rootWeight) {
    Node* root = new Node(rootWeight);
    if (depth == 0) {
        // лист
        return root;
    }
    double childWeight = rootWeight / n;
    root->children.reserve(n);
    for (int i = 0; i < n; ++i) {
        root->children.push_back(buildTree(depth - 1, n, childWeight));
    }
    return root;
}

void deleteTree(Node* root) {
    if (!root) return;
    for (Node* ch : root->children) {
        deleteTree(ch);
    }
    delete root;
}

bool isLeaf(Node* node) {
    return node->children.empty();
}

//3
void dfsSumLeaves(Node* node, double& sum) {
    if (!node) return;
    if (isLeaf(node)) {
        sum += node->weight;
    } else {
        for (Node* ch : node->children) {
            dfsSumLeaves(ch, sum);
        }
    }
}

double dfsSumLeaves(Node* root) {
    double sum = 0.0;
    dfsSumLeaves(root, sum);
    return sum;
}

//4
double bfsSumLeaves(Node* root) {
    if (!root) return 0.0;
    double sum = 0.0;
    queue<Node*> q;
    q.push(root);
    while (!q.empty()) {
        Node* node = q.front();
        q.pop();
        if (isLeaf(node)) {
            sum += node->weight;
        } else {
            for (Node* ch : node->children) {
                q.push(ch);
            }
        }
    }
    return sum;
}

//5
void dfsFlipAndSumLeaves(Node* node, double& sum) {
    if (!node) return;

    node->weight = -node->weight;

    if (isLeaf(node)) {
        sum += node->weight;
    } else {
        for (Node* ch : node->children) {
            dfsFlipAndSumLeaves(ch, sum);
        }
    }
}

double dfsFlipAndSumLeaves(Node* root) {
    double sum = 0.0;
    dfsFlipAndSumLeaves(root, sum);
    return sum;
}

double bfsFlipAndSumLeaves(Node* root) {
    if (!root) return 0.0;
    double sum = 0.0;
    queue<Node*> q;
    q.push(root);
    while (!q.empty()) {
        Node* node = q.front();
        q.pop();

        node->weight = -node->weight;

        if (isLeaf(node)) {
            sum += node->weight;
        } else {
            for (Node* ch : node->children) {
                q.push(ch);
            }
        }
    }
    return sum;
}

// 6
void bfsRecursiveLevel(vector<Node*>& level, double& sum) {
    if (level.empty()) return;

    vector<Node*> nextLevel;
    for (Node* node : level) {
        if (isLeaf(node)) {
            sum += node->weight;
        } else {
            for (Node* ch : node->children) {
                nextLevel.push_back(ch);
            }
        }
    }

    bfsRecursiveLevel(nextLevel, sum);
}

double bfsSumLeavesRecursive(Node* root) {
    if (!root) return 0.0;
    double sum = 0.0;
    vector<Node*> firstLevel = {root};
    bfsRecursiveLevel(firstLevel, sum);
    return sum;
}


void bfsRecursiveLevelFlip(vector<Node*>& level, double& sum) {
    if (level.empty()) return;

    vector<Node*> nextLevel;
    for (Node* node : level) {
        node->weight = -node->weight;

        if (isLeaf(node)) {
            sum += node->weight;
        } else {
            for (Node* ch : node->children) {
                nextLevel.push_back(ch);
            }
        }
    }

    bfsRecursiveLevelFlip(nextLevel, sum);
}

double bfsFlipAndSumLeavesRecursive(Node* root) {
    if (!root) return 0.0;
    double sum = 0.0;
    vector<Node*> firstLevel = {root};
    bfsRecursiveLevelFlip(firstLevel, sum);
    return sum;
}



void solve() {
	
    //2
    int depth = 3;
    int n = 3;
    double rootWeight = 1.0;
    
    Node* root = buildTree(depth, n, rootWeight);

    cout << "n = " << n << ", depth = " << depth << "\n";

    // 3 dfs sum of leaves
    double dfsSum = dfsSumLeaves(root);
    cout << "DFS sum of leaves (no flip) = " << dfsSum << "  (expect 1)\n";

    // 4 bfs sum of leaves
    double bfsSum = bfsSumLeaves(root);
    cout << "BFS sum of leaves (no flip) = " << bfsSum << "  (expect 1)\n";

    // 5 flip sign dfs first flip
    double dfsFlip1 = dfsFlipAndSumLeaves(root);
    cout << "DFS flip #1, sum of leaves = " << dfsFlip1 << "  (expect -1)\n";

    // dfs second flip
    double dfsFlip2 = dfsFlipAndSumLeaves(root);
    cout << "DFS flip #2, sum of leaves = " << dfsFlip2 << "  (expect +1)\n";

    // bfs flip
    double bfsFlip1 = bfsFlipAndSumLeaves(root);
    cout << "BFS flip #1, sum of leaves = " << bfsFlip1 << "\n";

    double bfsFlip2 = bfsFlipAndSumLeaves(root);
    cout << "BFS flip #2, sum of leaves = " << bfsFlip2 << "\n";

    // 6 recursive bfs without flip
    double bfsRecSum = bfsSumLeavesRecursive(root);
    cout << "BFS recursive sum of leaves (no flip) = " << bfsRecSum << "\n";

    // 6 recursive bfs with flip
    double bfsRecFlip1 = bfsFlipAndSumLeavesRecursive(root);
    cout << "BFS recursive flip #1 sum of leaves = " << bfsRecFlip1 << "\n";

    deleteTree(root);

    // 7 
    cout << "Answer to seventh question\n";
	cout << "BFS is logically based on a queue of levels\nA recursive implementation of BFS relies on the call stack and can easily\ncause stack overflow on large trees, while an iterative implementation\nwith an explicit queue scales much better";
}


int main(){
	int t = 1;
	while(t--){
		solve();
	}
}

	
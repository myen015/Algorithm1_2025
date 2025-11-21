#include <bits/stdc++.h>
using namespace std;

struct Node {
    double w;
    vector<Node*> c;
    Node(double w): w(w) {}
};

Node* build(int depth, double w, int n) {
    Node* r = new Node(w);
    if(depth == 0) return r;
    for(int i = 0; i < n; i++) r->c.push_back(build(depth - 1, w / n, n));
    return r;
}

double dfs(Node* r) {
    double s = r->w;
    for(auto x : r->c) s += dfs(x);
    return s;
}

double bfs(Node* r) {
    queue<Node*> q;
    q.push(r);
    double s = 0;
    while(!q.empty()) {
        Node* x = q.front(); q.pop();
        s += x->w;
        for(auto y : x->c) q.push(y);
    }
    return s;
}

double dfs_flip(Node* r) {
    r->w = -r->w;
    double s = r->w;
    for(auto x : r->c) s += dfs_flip(x);
    return s;
}

double bfs_flip(Node* r) {
    queue<Node*> q;
    q.push(r);
    double s = 0;
    while(!q.empty()) {
        Node* x = q.front(); q.pop();
        x->w = -x->w;
        s += x->w;
        for(auto y : x->c) q.push(y);
    }
    return s;
}

double bfs_recursive(vector<Node*> level) {
    if(level.empty()) return 0;
    vector<Node*> next;
    double s = 0;
    for(Node* x : level) {
        s += x->w;
        for(auto y : x->c) next.push_back(y);
    }
    return s + bfs_recursive(next);
}

int main() {
    int n = 5;
    int depth = 3;
    double root_weight = 1.0 / (depth + 1);
    Node* root = build(depth, root_weight, n);

    cout << "DFS sum: " << dfs(root) << endl;
    cout << "BFS sum: " << bfs(root) << endl;

    cout << "DFS flip: " << dfs_flip(root) << endl;
    cout << "BFS flip: " << bfs_flip(root) << endl;

    cout << "DFS flip again: " << dfs_flip(root) << endl;
    cout << "BFS flip again: " << bfs_flip(root) << endl;

    cout << "Recursive BFS sum: " << bfs_recursive({root}) << endl;

    return 0;
}

#include <bits/stdc++.h>
using namespace std;

struct CSC {
    vector<int> colptr;
    vector<int> rowidx;
    vector<int> vals;
    vector<string> names;
    bool directed;
    CSC(const vector<int>& c, const vector<int>& r, const vector<int>& v,
        const vector<string>& nm, bool dir)
        : colptr(c), rowidx(r), vals(v), names(nm), directed(dir) {}
    vector<vector<int>> toAdjMatrix() const {
        int m = names.size();
        vector<vector<int>> mat(m, vector<int>(m, 0));
        for (int col = 0; col < m; ++col) {
            int st = colptr[col];
            int en = colptr[col+1];
            for (int k = st; k < en; ++k) {
                int row = rowidx[k];
                int val = vals[k];
                if (row >= 0 && row < m) mat[row][col] = val;
            }
        }
        return mat;
    }
    unordered_map<string, vector<string>> adjacencyList() const {
        auto mat = toAdjMatrix();
        unordered_map<string, vector<string>> out;
        int m = names.size();
        for (int i = 0; i < m; ++i) {
            out[names[i]] = {};
            for (int j = 0; j < m; ++j) {
                if (mat[i][j] != 0) out[names[i]].push_back(names[j]);
            }
        }
        return out;
    }
    void printAdjMatrixPretty() const {
        auto mat = toAdjMatrix();
        int m = names.size();
        cout << "\nAdjacency matrix:\n    ";
        for (int j = 0; j < m; ++j) cout << setw(3) << names[j];
        cout << "\n";
        for (int i = 0; i < m; ++i) {
            cout << setw(3) << names[i] << ":";
            for (int j = 0; j < m; ++j) cout << setw(3) << mat[i][j];
            cout << "\n";
        }
    }
    void printAdjListDiagram() const {
        auto al = adjacencyList();
        cout << (directed ? "\nDirected adjacency list:\n" : "\nUndirected adjacency list:\n");
        for (auto &nm : names) {
            cout << nm << " -> ";
            auto &vec = al.at(nm);
            if (vec.empty()) cout << "(isolated)";
            else {
                for (size_t i = 0; i < vec.size(); ++i) {
                    if (i) cout << ", ";
                    cout << vec[i];
                }
            }
            cout << "\n";
        }
    }
    vector<string> findDirectedCycle() const {
        if (!directed) return {};
        int m = names.size();
        auto al = adjacencyList();
        unordered_map<string,int> idx;
        for (int i = 0; i < m; ++i) idx[names[i]] = i;
        vector<char> vis(m, 0), onstack(m, 0);
        vector<int> parent(m, -1);
        vector<string> cycle;
        function<bool(int)> dfs = [&](int u)->bool {
            vis[u] = 1;
            onstack[u] = 1;
            string su = names[u];
            for (auto &sv : al[su]) {
                int v = idx[sv];
                if (!vis[v]) {
                    parent[v] = u;
                    if (dfs(v)) return true;
                } else if (onstack[v]) {
                    vector<int> path;
                    int cur = u;
                    path.push_back(v);
                    while (cur != v && cur != -1) { path.push_back(cur); cur = parent[cur]; }
                    path.push_back(v);
                    reverse(path.begin(), path.end());
                    for (int id : path) cycle.push_back(names[id]);
                    return true;
                }
            }
            onstack[u] = 0;
            return false;
        };
        for (int i = 0; i < m; ++i) if (!vis[i]) {
            if (dfs(i)) return cycle;
        }
        return {};
    }
    void printVisualEdges() const {
        auto al = adjacencyList();
        cout << "\nEdges (visual):\n";
        if (directed) {
            for (auto &u : names) for (auto &v : al[u]) cout << "   " << u << " -> " << v << "\n";
        } else {
            set<pair<string,string>> printed;
            for (auto &u : names) {
                for (auto &v : al[u]) {
                    auto e = make_pair(min(u,v), max(u,v));
                    if (!printed.count(e)) {
                        cout << "   " << e.first << " -- " << e.second << "\n";
                        printed.insert(e);
                    }
                }
            }
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "=== PROBLEM 2: CSC (Compressed Sparse Column) ===\n";

    vector<string> names = {"A","B","C","D","E"};

    cout << "\n-- Graph 1 (undirected) --\n";
    vector<int> colptr1 = {0,2,5,8,11,12};
    vector<int> rowidx1 = {1,2,0,2,3,0,1,3,1,2,4,3};
    vector<int> vals1   = {1,1,1,1,1,1,1,1,1,1,1,1};
    CSC c1(colptr1, rowidx1, vals1, names, false);
    c1.printAdjMatrixPretty();
    c1.printAdjListDiagram();
    c1.printVisualEdges();

    cout << "\n-- Graph 2 (directed) --\n";
    vector<int> colptr2 = {0,0,2,4,5,7};
    vector<int> rowidx2 = {0,3,0,1,2,1,3};
    vector<int> vals2   = {1,1,1,1,1,1,1};
    CSC c2(colptr2, rowidx2, vals2, names, true);
    c2.printAdjMatrixPretty();
    c2.printAdjListDiagram();
    c2.printVisualEdges();

    auto cycle = c2.findDirectedCycle();
    if (cycle.empty()) {
        cout << "\nDirected graph: no directed cycle found.\n";
    } else {
        cout << "\nDirected graph: cycle found: ";
        for (size_t i = 0; i < cycle.size(); ++i) {
            if (i) cout << " -> ";
            cout << cycle[i];
        }
        cout << "\n";
    }

    cout << "\n=== SUMMARY ===\n";
    cout << "Graph1 (undirected): vertices A..E; edges listed above.\n";
    cout << "Graph2 (directed): vertices A..E; directed cycle (if any) printed above.\n";
    return 0;
}

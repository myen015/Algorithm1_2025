#include <bits/stdc++.h>
using namespace std;

struct SimpleGraph {
    int n;
    vector<pair<int,int>> edges;
    vector<vector<int>> adj;
    SimpleGraph(int n_ = 0) : n(n_), adj(n_) {}
    void addEdge(int u, int v) {
        edges.emplace_back(u,v);
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    bool isConnected() const {
        if (n == 0) return true;
        vector<char> vis(n, 0);
        function<void(int)> dfs = [&](int u) {
            vis[u] = 1;
            for (int w : adj[u]) if (!vis[w]) dfs(w);
        };
        dfs(0);
        for (int i = 0; i < n; ++i) if (!vis[i]) return false;
        return true;
    }
    bool hasCycleUtil(int u, int parent, vector<char>& vis) const {
        vis[u] = 1;
        for (int w : adj[u]) {
            if (!vis[w]) {
                if (hasCycleUtil(w, u, vis)) return true;
            } else if (w != parent) {
                return true;
            }
        }
        return false;
    }
    bool isAcyclic() const {
        vector<char> vis(n, 0);
        for (int i = 0; i < n; ++i) {
            if (!vis[i]) {
                if (hasCycleUtil(i, -1, vis)) return false;
            }
        }
        return true;
    }
    bool edgeExists(int u, int v) const {
        for (int w : adj[u]) if (w == v) return true;
        return false;
    }
    bool removalDisconnects(int edgeIndex) const {
        if (edgeIndex < 0 || edgeIndex >= (int)edges.size()) return false;
        vector<vector<int>> a(n);
        for (int i = 0; i < (int)edges.size(); ++i) {
            if (i == edgeIndex) continue;
            auto [u,v] = edges[i];
            a[u].push_back(v);
            a[v].push_back(u);
        }
        vector<char> vis(n, 0);
        function<void(int)> dfs = [&](int u) {
            vis[u] = 1;
            for (int w : a[u]) if (!vis[w]) dfs(w);
        };
        dfs(0);
        for (int i = 0; i < n; ++i) if (!vis[i]) return true;
        return false;
    }
    bool hasPath(int u, int v) const {
        if (u == v) return true;
        vector<char> vis(n, 0);
        function<bool(int)> dfs = [&](int cur) -> bool {
            vis[cur] = 1;
            for (int w : adj[cur]) if (!vis[w]) {
                if (w == v) return true;
                if (dfs(w)) return true;
            }
            return false;
        };
        return dfs(u);
    }
    int countSimplePaths(int u, int v, int cap = 2) const {
        vector<char> vis(n, 0);
        int cnt = 0;
        function<void(int)> dfs = [&](int cur) {
            if (cnt >= cap) return;
            if (cur == v) { ++cnt; return; }
            vis[cur] = 1;
            for (int w : adj[cur]) if (!vis[w]) dfs(w);
            vis[cur] = 0;
        };
        dfs(u);
        return cnt;
    }
    bool connectedAndAcyclic() const { return isConnected() && isAcyclic(); }
    bool isComponentOfForest() const { return isConnected() && isAcyclic(); }
    bool connectedWithVminusOneEdges() const { return isConnected() && ((int)edges.size() == n-1); }
    bool minimallyConnected() const {
        if (!isConnected()) return false;
        for (int i = 0; i < (int)edges.size(); ++i) {
            if (!removalDisconnects(i)) return false;
        }
        return true;
    }
    bool acyclicWithAtLeastVminusOneEdges() const {
        return isAcyclic() && ((int)edges.size() >= n-1);
    }
    bool maximallyAcyclic() const {
        if (!isAcyclic()) return false;
        for (int u = 0; u < n; ++u) {
            for (int v = u+1; v < n; ++v) {
                if (!edgeExists(u,v)) {
                    if (!hasPath(u,v)) return false;
                }
            }
        }
        return true;
    }
    bool uniquePathBetweenAllPairs() const {
        for (int u = 0; u < n; ++u) {
            for (int v = u+1; v < n; ++v) {
                int ct = countSimplePaths(u,v, 2);
                if (ct != 1) return false;
            }
        }
        return true;
    }
};

void verifyTreeLike(SimpleGraph &g, const string &title) {
    cout << "=== " << title << " ===\n";
    cout << "Vertices: " << g.n << ", Edges: " << g.edges.size() << "\n";
    bool p1 = g.connectedAndAcyclic();
    bool p2 = g.isComponentOfForest();
    bool p3 = g.connectedWithVminusOneEdges();
    bool p4 = g.minimallyConnected();
    bool p5 = g.acyclicWithAtLeastVminusOneEdges();
    bool p6 = g.maximallyAcyclic();
    bool p7 = g.uniquePathBetweenAllPairs();
    cout << "1) Connected & acyclic:              " << (p1 ? "YES" : "NO") << "\n";
    cout << "2) Component of a forest:            " << (p2 ? "YES" : "NO") << "\n";
    cout << "3) Connected and |E| = V-1:          " << (p3 ? "YES" : "NO") << "\n";
    cout << "4) Minimally connected (remove edge disconnects): " << (p4 ? "YES" : "NO") << "\n";
    cout << "5) Acyclic and |E| >= V-1:           " << (p5 ? "YES" : "NO") << "\n";
    cout << "6) Maximally acyclic (add any missing edge => cycle): " << (p6 ? "YES" : "NO") << "\n";
    cout << "7) Unique simple path between every pair: " << (p7 ? "YES" : "NO") << "\n";
    bool allEqual = (p1==p2 && p2==p3 && p3==p4 && p4==p5 && p5==p6 && p6==p7);
    cout << "All properties agree: " << (allEqual ? "YES" : "NO") << "\n\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "=== PROBLEM 1: Trees / Equivalent Definitions ===\n\n";

    SimpleGraph g1(5);
    g1.addEdge(0,1);
    g1.addEdge(0,2);
    g1.addEdge(1,3);
    g1.addEdge(1,4);
    verifyTreeLike(g1, "Test A: proper tree (5 nodes)");

    SimpleGraph g2(4);
    g2.addEdge(0,1); g2.addEdge(1,2); g2.addEdge(2,3); g2.addEdge(3,0);
    verifyTreeLike(g2, "Test B: 4-cycle (not tree)");

    SimpleGraph g3(4);
    g3.addEdge(0,1); g3.addEdge(2,3);
    verifyTreeLike(g3, "Test C: disconnected");

    SimpleGraph g4(4);
    g4.addEdge(0,1); g4.addEdge(0,2); g4.addEdge(1,2); g4.addEdge(1,3);
    verifyTreeLike(g4, "Test D: too many edges");

    cout << "=== End of Problem 1 ===\n";
    return 0;
}

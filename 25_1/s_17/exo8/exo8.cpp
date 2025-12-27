#include <bits/stdc++.h>
using namespace std;


struct DirectedGraph {
    int V;
    vector<vector<int>> adj;
    vector<int> indeg, outdeg;

    DirectedGraph(int n = 0) { init(n); }

    void init(int n) {
        V = n;
        adj.assign(V, {});
        indeg.assign(V, 0);
        outdeg.assign(V, 0);
    }

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        outdeg[u]++;
        indeg[v]++;
    }
};


DirectedGraph reverseGraph(const DirectedGraph& g) {
    DirectedGraph rg(g.V);
    for (int u = 0; u < g.V; ++u)
        for (int v : g.adj[u])
            rg.addEdge(v, u);
    return rg;
}


void dfs1(const DirectedGraph& g, int u, vector<char>& used, vector<int>& order) {
    used[u] = 1;
    for (int v : g.adj[u])
        if (!used[v]) dfs1(g, v, used, order);
    order.push_back(u);
}

void dfs2(const DirectedGraph& rg, int u, int compId, vector<int>& comp) {
    comp[u] = compId;
    for (int v : rg.adj[u])
        if (comp[v] == -1) dfs2(rg, v, compId, comp);
}

pair<vector<int>, int> kosarajuSCC(const DirectedGraph& g) {
    int n = g.V;
    vector<char> used(n, 0);
    vector<int> order;
    order.reserve(n);

    for (int i = 0; i < n; ++i)
        if (!used[i]) dfs1(g, i, used, order);

    DirectedGraph rg = reverseGraph(g);

    vector<int> comp(n, -1);
    int compId = 0;
    for (int i = n - 1; i >= 0; --i) {
        int v = order[i];
        if (comp[v] == -1) {
            dfs2(rg, v, compId, comp);
            compId++;
        }
    }
    return {comp, compId};
}


DirectedGraph buildCondensation(const DirectedGraph& g,
                                const vector<int>& comp,
                                int compCount) {
    DirectedGraph dag(compCount);
    set<pair<int,int>> usedEdges;

    for (int u = 0; u < g.V; ++u) {
        for (int v : g.adj[u]) {
            int cu = comp[u], cv = comp[v];
            if (cu != cv && !usedEdges.count({cu, cv})) {
                usedEdges.insert({cu, cv});
                dag.addEdge(cu, cv);
            }
        }
    }
    return dag;
}

bool isAcyclic(const DirectedGraph& g) {
    int n = g.V;
    vector<int> indeg = g.indeg;
    queue<int> q;
    for (int i = 0; i < n; ++i)
        if (indeg[i] == 0) q.push(i);

    int cnt = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        cnt++;
        for (int v : g.adj[u])
            if (--indeg[v] == 0) q.push(v);
    }
    return cnt == n;
}


bool canReach(const DirectedGraph& g, int u, int v) {
    vector<char> used(g.V, 0);
    queue<int> q;
    q.push(u);
    used[u] = 1;
    while (!q.empty()) {
        int x = q.front(); q.pop();
        if (x == v) return true;
        for (int y : g.adj[x]) {
            if (!used[y]) {
                used[y] = 1;
                q.push(y);
            }
        }
    }
    return false;
}

bool canReachSCC(const DirectedGraph& dag, int cu, int cv) {
    vector<char> used(dag.V, 0);
    queue<int> q;
    q.push(cu);
    used[cu] = 1;
    while (!q.empty()) {
        int x = q.front(); q.pop();
        if (x == cv) return true;
        for (int y : dag.adj[x]) {
            if (!used[y]) {
                used[y] = 1;
                q.push(y);
            }
        }
    }
    return false;
}


bool checkEulerCondition(const DirectedGraph& g) {
    for (int v = 0; v < g.V; ++v)
        if (g.indeg[v] != g.outdeg[v]) return false;
    return true;
}

bool isStronglyConnectedByEdges(const DirectedGraph& g) {
    int n = g.V;
    int start = -1;
    for (int i = 0; i < n; ++i) {
        if (g.outdeg[i] > 0 || g.indeg[i] > 0) { start = i; break; }
    }
    if (start == -1) return true;


    vector<char> used(n, 0);
    stack<int> st;
    st.push(start);
    used[start] = 1;
    while (!st.empty()) {
        int u = st.top(); st.pop();
        for (int v : g.adj[u]) {
            if (!used[v]) {
                used[v] = 1;
                st.push(v);
            }
        }
    }
    for (int i = 0; i < n; ++i)
        if ((g.outdeg[i] > 0 || g.indeg[i] > 0) && !used[i]) return false;


    DirectedGraph rg = reverseGraph(g);
    used.assign(n, 0);
    st.push(start);
    used[start] = 1;
    while (!st.empty()) {
        int u = st.top(); st.pop();
        for (int v : rg.adj[u]) {
            if (!used[v]) {
                used[v] = 1;
                st.push(v);
            }
        }
    }
    for (int i = 0; i < n; ++i)
        if ((g.outdeg[i] > 0 || g.indeg[i] > 0) && !used[i]) return false;

    return true;
}

vector<int> eulerTour(const DirectedGraph& g) {
    if (!checkEulerCondition(g)) return {};
    if (!isStronglyConnectedByEdges(g)) return {};

    int n = g.V;
    vector<int> idx(n, 0);

    int start = 0;
    for (int i = 0; i < n; ++i)
        if (g.outdeg[i] > 0) { start = i; break; }

    vector<int> path;
    stack<int> st;
    st.push(start);

    while (!st.empty()) {
        int u = st.top();
        if (idx[u] < (int)g.adj[u].size()) {
            int v = g.adj[u][idx[u]++];
            st.push(v);
        } else {
            path.push_back(u);
            st.pop();
        }
    }
    reverse(path.begin(), path.end());
    return path;
}


vector<int> topoSort(const DirectedGraph& g) {
    int n = g.V;
    vector<int> indeg = g.indeg;
    queue<int> q;
    for (int i = 0; i < n; ++i)
        if (indeg[i] == 0) q.push(i);

    vector<int> res;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        res.push_back(u);
        for (int v : g.adj[u])
            if (--indeg[v] == 0) q.push(v);
    }
    if ((int)res.size() != n) return {}; // cycle
    return res;
}


DirectedGraph readGraphDirected() {
    int V, E;
    cout << "Enter V (vertices) and E (edges): " << flush;
    cin >> V >> E;

    DirectedGraph g(V);

    cout << "Enter edges as: u v (0-indexed, directed u->v)\n" << flush;
    for (int i = 0; i < E; ++i) {
        int u, v;
        cin >> u >> v;
        if (u < 0 || u >= V || v < 0 || v >= V) {
            cout << "Invalid edge (" << u << "," << v << "), skipped.\n" << flush;
            continue;
        }
        g.addEdge(u, v);
    }
    return g;
}

void printAdj(const DirectedGraph& g, const string& title) {
    cout << "\n" << title << ":\n";
    for (int u = 0; u < g.V; ++u) {
        cout << u << ": ";
        for (int v : g.adj[u]) cout << v << " ";
        cout << "\n";
    }
}

void printSCCResult(const vector<int>& comp, int compCount) {
    cout << "\nSCC count = " << compCount << "\n";
    for (int i = 0; i < (int)comp.size(); ++i)
        cout << "vertex " << i << " in SCC " << comp[i] << "\n";
}


void solve() {
    while (true) {
        cout << "\n================ MENU ================\n";
        cout << "1) Reverse graph rev(G)\n";
        cout << "2) SCC (Kosaraju) + Condensation DAG + Acyclic check\n";
        cout << "3) Reachability u -> v in G\n";
        cout << "4) Reachability SCC(u) -> SCC(v) in condensation\n";
        cout << "5) Euler Tour (Hierholzer)\n";
        cout << "6) Topological Sort (Kahn)\n";
        cout << "0) Exit\n";
        cout << "Choose option: " << flush;

        int op;
        cin >> op;
        if (!cin) return;
        if (op == 0) break;

        DirectedGraph g = readGraphDirected();
        printAdj(g, "Input graph");

        if (op == 1) {
            DirectedGraph rg = reverseGraph(g);
            printAdj(rg, "Reversed graph rev(G)");
        }
        else if (op == 2) {
            auto [comp, compCount] = kosarajuSCC(g);
            printSCCResult(comp, compCount);

            DirectedGraph dag = buildCondensation(g, comp, compCount);
            printAdj(dag, "Condensation DAG scc(G)");
            cout << "Is condensation DAG acyclic? " << (isAcyclic(dag) ? "YES" : "NO") << "\n";
        }
        else if (op == 3) {
            int u, v;
            cout << "Enter u and v: " << flush;
            cin >> u >> v;
            if (u < 0 || u >= g.V || v < 0 || v >= g.V) {
                cout << "Invalid vertices.\n";
                continue;
            }
            cout << (canReach(g, u, v) ? "YES, u can reach v\n" : "NO, u cannot reach v\n");
        }
        else if (op == 4) {
            auto [comp, compCount] = kosarajuSCC(g);
            DirectedGraph dag = buildCondensation(g, comp, compCount);

            int u, v;
            cout << "Enter u and v (in original graph): " << flush;
            cin >> u >> v;
            if (u < 0 || u >= g.V || v < 0 || v >= g.V) {
                cout << "Invalid vertices.\n";
                continue;
            }

            int cu = comp[u], cv = comp[v];
            cout << "SCC(u) = " << cu << ", SCC(v) = " << cv << "\n";
            cout << (canReachSCC(dag, cu, cv) ? "YES, SCC(u) can reach SCC(v)\n"
                                             : "NO, SCC(u) cannot reach SCC(v)\n");
        }
        else if (op == 5) {
            cout << "\nEuler tour requirements:\n";
            cout << "1) indeg[v] == outdeg[v] for all v\n";
            cout << "2) strongly connected among vertices with non-zero degree\n";
            cout << "Check indeg==outdeg? " << (checkEulerCondition(g) ? "YES" : "NO") << "\n";
            cout << "Check strong connectivity (by edges)? " << (isStronglyConnectedByEdges(g) ? "YES" : "NO") << "\n";

            vector<int> tour = eulerTour(g);
            if (tour.empty()) {
                cout << "No Euler tour found.\n";
            } else {
                cout << "Euler tour (vertex sequence):\n";
                for (int x : tour) cout << x << " ";
                cout << "\nEdges used = " << (int)tour.size() - 1 << "\n";
            }
        }
        else if (op == 6) {
            vector<int> order = topoSort(g);
            if (order.empty()) {
                cout << "Topological sort is impossible (graph has a cycle).\n";
            } else {
                cout << "Topological ordering:\n";
                for (int x : order) cout << x << " ";
                cout << "\n";
            }
        }
        else {
            cout << "Unknown option.\n";
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    solve();
    return 0;
}

/*
Problem 1.2

The graph scc(G) is acyclic.
If it has a cycle, then all components in this cycle can reach each other.
This means they should be one single strongly connected component, which is contradiction.
So scc(G) has no cycles.

Problem 1.3

Strongly connected components are defined by mutual reachability.
When we reverse all edges, this property does not changes.
So SCCs in G and in rev(G) are the same.
Edges between components are just reversed, therefore
scc(rev(G)) = rev(scc(G)).

Problem 1.4

If u can reach v in G, then SCC(u) can reach SCC(v) in scc(G).
If SCC(u) can reach SCC(v), then u can reach v in G by moving inside components.
So reachability is preserved in both graphs.

*/
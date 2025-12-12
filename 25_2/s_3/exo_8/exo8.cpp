#include <bits/stdc++.h>
using namespace std;

void print_vec(const vector<int>& v, const string& sep = " ") {
    for (size_t i = 0; i < v.size(); ++i) {
        if (i) cout << sep;
        cout << v[i];
    }
    cout << "\n";
}

vector<vector<int>> reverse_graph(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<vector<int>> radj(n);
    for (int u = 0; u < n; ++u) {
        for (int v : adj[u]) {
            radj[v].push_back(u);
        }
    }
    return radj;
}

void dfs1(int u, const vector<vector<int>>& adj, vector<char>& used, vector<int>& order) {
    used[u] = 1;
    for (int v : adj[u]) if (!used[v]) dfs1(v, adj, used, order);
    order.push_back(u);
}
void dfs2(int u, const vector<vector<int>>& radj, vector<char>& used, vector<int>& comp, int cid) {
    used[u] = 1;
    comp[u] = cid;
    for (int v : radj[u]) if (!used[v]) dfs2(v, radj, used, comp, cid);
}
vector<int> kosaraju(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<char> used(n, 0);
    vector<int> order;
    order.reserve(n);
    for (int i = 0; i < n; ++i) if (!used[i]) dfs1(i, adj, used, order);
    vector<vector<int>> radj = reverse_graph(adj);
    fill(used.begin(), used.end(), 0);
    vector<int> comp(n, -1);
    int cid = 0;
    for (int i = n-1; i >= 0; --i) {
        int v = order[i];
        if (!used[v]) {
            dfs2(v, radj, used, comp, cid++);
        }
    }
    return comp;
}

vector<vector<int>> build_condensation(const vector<vector<int>>& adj, const vector<int>& comp) {
    int n = adj.size();
    int k = 0;
    for (int x : comp) k = max(k, x+1);
    vector<unordered_set<int>> s(k);
    for (int u = 0; u < n; ++u) {
        for (int v : adj[u]) {
            int cu = comp[u], cv = comp[v];
            if (cu != cv) s[cu].insert(cv);
        }
    }
    vector<vector<int>> cadj(k);
    for (int i = 0; i < k; ++i) {
        for (int x : s[i]) cadj[i].push_back(x);
    }
    return cadj;
}

bool topo_with_priority(const vector<vector<int>>& adj, vector<int>& order, int preferred = -1) {
    int n = adj.size();
    vector<int> indeg(n, 0);
    for (int u = 0; u < n; ++u) for (int v : adj[u]) indeg[v]++;
    set<int> zeros;
    for (int i = 0; i < n; ++i) if (indeg[i] == 0) zeros.insert(i);
    order.clear();
    while (!zeros.empty()) {
        int pick;
        if (preferred != -1 && zeros.count(preferred)) {
            pick = preferred;
        } else {
            pick = *zeros.begin(); 
        }
        zeros.erase(pick);
        order.push_back(pick);
        for (int v : adj[pick]) {
            indeg[v]--;
            if (indeg[v] == 0) zeros.insert(v);
        }
    }
    return ((int)order.size() == n);
}

bool has_euler_tour(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<int> indeg(n, 0), outdeg(n, 0);
    for (int u = 0; u < n; ++u) {
        outdeg[u] = adj[u].size();
        for (int v : adj[u]) indeg[v]++;
    }
    for (int i = 0; i < n; ++i) if (indeg[i] != outdeg[i]) return false;
    int start = -1;
    for (int i = 0; i < n; ++i) if (outdeg[i] > 0) { start = i; break; }
    if (start == -1) return true; 
    vector<int> comp = kosaraju(adj);
    int cid = comp[start];
    for (int i = 0; i < n; ++i) {
        if (outdeg[i] > 0 || indeg[i] > 0) {
            if (comp[i] != cid) return false;
        }
    }
    return true;
}

vector<int> euler_tour_directed(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<int> indeg(n,0);
    vector<int> outdeg(n,0);
    for (int u = 0; u < n; ++u) {
        outdeg[u] = adj[u].size();
        for (int v : adj[u]) indeg[v]++;
    }
    int start = 0;
    for (int i = 0; i < n; ++i) if (outdeg[i] > 0) { start = i; break; }
    vector<int> edge_pos(n, 0);
    vector<vector<int>> g = adj;
    vector<int> st;
    vector<int> circuit; circuit.reserve(1000);
    st.push_back(start);
    while (!st.empty()) {
        int v = st.back();
        if (edge_pos[v] < (int)g[v].size()) {
            int to = g[v][edge_pos[v]++];
            st.push_back(to);
        } else {
            circuit.push_back(v);
            st.pop_back();
        }
    }
    reverse(circuit.begin(), circuit.end()); 
    return circuit; 
}

int idx(char c) { return c - 'A'; }
char chr(int i) { return 'A' + i; }

void demo_course_graph() {
    cout << "=== Demo: course graph (A..G) ===\n";
    int n = 7; 
    vector<vector<int>> adj(n);
    auto add = [&](char a, char b){ adj[idx(a)].push_back(idx(b)); };
    add('A','B'); add('A','C'); add('B','C'); add('B','D'); add('C','E');
    add('D','E'); add('D','F'); add('G','F'); add('G','E');

    cout << "Adjacency:\n";
    for (int i = 0; i < n; ++i) {
        cout << chr(i) << ": ";
        for (int v : adj[i]) cout << chr(v) << ' ';
        cout << "\n";
    }

    auto radj = reverse_graph(adj);
    cout << "Reversed adjacency:\n";
    for (int i = 0; i < n; ++i) {
        cout << chr(i) << ": ";
        for (int v : radj[i]) cout << chr(v) << ' ';
        cout << "\n";
    }

    auto comp = kosaraju(adj);
    cout << "Component ids (Kosaraju):\n";
    for (int i = 0; i < n; ++i) cout << chr(i) << " -> C" << comp[i] << "\n";

    auto cadj = build_condensation(adj, comp);
    cout << "Condensation graph adjacency (components):\n";
    for (int i = 0; i < (int)cadj.size(); ++i) {
        cout << "C" << i << ": ";
        for (int v : cadj[i]) cout << "C" << v << ' ';
        cout << "\n";
    }

    vector<int> order;
    bool ok = topo_with_priority(adj, order, idx('A'));
    cout << "Topological order (prefer A): ";
    if (ok) {
        for (int x : order) cout << chr(x) << ' ';
        cout << "\n";
    } else cout << "Graph has cycle\n";

    ok = topo_with_priority(adj, order, idx('G'));
    cout << "Topological order (prefer G): ";
    if (ok) {
        for (int x : order) cout << chr(x) << ' ';
        cout << "\n";
    } else cout << "Graph has cycle\n";

    ok = topo_with_priority(adj, order, -1);
    cout << "Topological order (smallest-first tie-break): ";
    if (ok) {
        for (int x : order) cout << chr(x) << ' ';
        cout << "\n";
    } else cout << "Graph has cycle\n";

    cout << "\n";
}

void demo_euler() {
    cout << "=== Demo: Euler tour ===\n";
    int n = 3;
    vector<vector<int>> adj(n);
    adj[0] = {1,2};
    adj[1] = {2,0};
    adj[2] = {0,1};
    cout << "Adjacency (Euler demo):\n";
    for (int i = 0; i < n; ++i) {
        cout << i << ": ";
        for (int v : adj[i]) cout << v << ' ';
        cout << "\n";
    }
    bool ok = has_euler_tour(adj);
    cout << "Has Euler tour? " << (ok ? "Yes" : "No") << "\n";
    if (ok) {
        auto circuit = euler_tour_directed(adj);
        cout << "Euler circuit (vertices): ";
        for (int v : circuit) cout << v << ' ';
        cout << "\n";
    }
    cout << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    demo_course_graph();
    demo_euler();


    return 0;
}

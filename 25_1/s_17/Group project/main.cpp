#include <bits/stdc++.h>
using namespace std;

struct CSR {
    int n;                          
    vector<int> rowPtr;             
    vector<int> colIdx;             
    vector<int> cost;               
    vector<pair<int,int>> coord;    
};

struct CSC {
    int n;
    vector<int> colPtr;             
    vector<int> rowIdx;             
    vector<int> cost;
};


int manhattan(const pair<int,int>& a, const pair<int,int>& b) {
    return abs(a.first - b.first) + abs(a.second - b.second);
}


CSC buildCSCFromCSR(const CSR& csr) {
    CSC csc;
    csc.n = csr.n;
    int n = csr.n;
    int m = (int)csr.colIdx.size();

    csc.colPtr.assign(n + 1, 0);
    csc.rowIdx.assign(m, 0);
    csc.cost.assign(m, 0);

    for (int k = 0; k < m; ++k) {
        int j = csr.colIdx[k];
        csc.colPtr[j + 1]++;
    }

    for (int j = 0; j < n; ++j) {
        csc.colPtr[j + 1] += csc.colPtr[j];
    }

    vector<int> offset = csc.colPtr;
    for (int i = 0; i < n; ++i) {
        for (int k = csr.rowPtr[i]; k < csr.rowPtr[i + 1]; ++k) {
            int j = csr.colIdx[k];
            int pos = offset[j]++;
            csc.rowIdx[pos] = i;
            csc.cost[pos]   = csr.cost[k];
        }
    }

    return csc;
}


vector<pair<int,int>> aStarCSR(const CSR& g, int startId, int goalId) {
    const int INF = 1e9;
    int n = g.n;

    if (startId < 0 || startId >= n || goalId < 0 || goalId >= n) {
        return {};
    }

    vector<int> gScore(n, INF);
    vector<int> fScore(n, INF);
    vector<int> parent(n, -1);
    vector<char> closed(n, 0);

    struct State {
        int f;
        int g;
        int id;
        bool operator<(const State& other) const {
            return f > other.f; 
        }
    };

    priority_queue<State> openList;

    gScore[startId] = 0;
    fScore[startId] = manhattan(g.coord[startId], g.coord[goalId]);
    openList.push({fScore[startId], gScore[startId], startId});

    while (!openList.empty()) {
        State cur = openList.top();
        openList.pop();

        int u = cur.id;
        if (closed[u]) continue;
        closed[u] = 1;

        if (u == goalId) break;

        for (int e = g.rowPtr[u]; e < g.rowPtr[u + 1]; ++e) {
            int v = g.colIdx[e];
            int w = g.cost[e];

            if (closed[v]) continue;

            int tentative_g = gScore[u] + w;
            if (tentative_g < gScore[v]) {
                gScore[v] = tentative_g;
                int h = manhattan(g.coord[v], g.coord[goalId]);
                fScore[v] = tentative_g + h;
                parent[v] = u;
                openList.push({fScore[v], gScore[v], v});
            }
        }
    }

    if (parent[goalId] == -1 && startId != goalId) {
        return {}; 
    }

    vector<pair<int,int>> path;
    int cur = goalId;
    while (cur != -1) {
        path.push_back(g.coord[cur]);
        cur = parent[cur];
    }
    reverse(path.begin(), path.end());
    return path;
}


int main() {
    const int H = 5;
    const int W = 8;
    const int N = H * W; 

    CSR csr;
    csr.n = N;
    csr.coord.resize(N);

    for (int id = 0; id < N; ++id) {
        int y = id / W;
        int x = id % W;
        csr.coord[id] = {x, y};
    }

    vector<vector<pair<int,int>>> adj(N); 

    const int dx[4] = {0, 0, -1, 1};
    const int dy[4] = {-1, 1, 0, 0};

    for (int id = 0; id < N; ++id) {
        int y = id / W;
        int x = id % W;

        for (int k = 0; k < 4; ++k) {
            int nx = x + dx[k];
            int ny = y + dy[k];
            if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;

            int toId = ny * W + nx;
            adj[id].push_back({toId, 1}); // вес = 1
        }
    }

    csr.rowPtr.assign(N + 1, 0);
    for (int i = 0; i < N; ++i) {
        csr.rowPtr[i + 1] = csr.rowPtr[i] + (int)adj[i].size();
    }

    int M = csr.rowPtr[N]; 
    csr.colIdx.assign(M, 0);
    csr.cost.assign(M, 0);

    int pos = 0;
    for (int i = 0; i < N; ++i) {
        for (auto &e : adj[i]) {
            csr.colIdx[pos] = e.first;
            csr.cost[pos]   = e.second;
            ++pos;
        }
    }

    CSC csc = buildCSCFromCSR(csr);
    (void)csc;

    int startId = 0;
    int goalId  = W * H - 1;

    auto path = aStarCSR(csr, startId, goalId);

    for (auto &p : path) {
        cout << "(" << p.first << ", " << p.second << ")\n";
    }

    return 0;
}

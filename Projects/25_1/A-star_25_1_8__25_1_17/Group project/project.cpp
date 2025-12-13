#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <random>
#include <ctime>
#include <thread>
#include <chrono>
#include <cmath>

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


void drawMaze(const vector<string>& maze,
              pair<int,int> player,
              bool showAlgo = false,
              pair<int,int> algoPos = {-1,-1},
              const vector<pair<int,int>>& algoTrail = {})
{
	

    cout << "\n================ MAZE ================\n";

    int H = (int)maze.size();
    int W = (int)maze[0].size();

    for (int y = 0; y < H; ++y) {
        for (int x = 0; x < W; ++x) {
            char c = maze[y][x];

            bool isTrail = false;
            for (auto &p : algoTrail) {
                if (p.first == x && p.second == y) {
                    isTrail = true;
                    break;
                }
            }

            if (player.first == x && player.second == y) {
                cout << 'P';
            } else if (showAlgo && algoPos.first == x && algoPos.second == y) {
                cout << 'A';
            } else if (isTrail && c == '.') {
                cout << '*';
            } else {
                cout << c;
            }
        }
        cout << "\n";
    }
    cout << "=====================================\n";
}

vector<string> generateMazeDFS(int H, int W) {
    if (H % 2 == 0) H++;
    if (W % 2 == 0) W++;

    vector<string> maze(H, string(W, '#'));

    auto inside = [&](int y, int x) {
        return (y > 0 && y < H - 1 && x > 0 && x < W - 1);
    };

    const int dx[4] = {0, 0, -2, 2};
    const int dy[4] = {-2, 2, 0, 0};

    vector<pair<int,int>> stack;
    stack.push_back({1, 1});
    maze[1][1] = '.';

    mt19937 rng((unsigned)time(nullptr));

    while (!stack.empty()) {
        auto [y, x] = stack.back();

        vector<int> dirs = {0, 1, 2, 3};
        shuffle(dirs.begin(), dirs.end(), rng);

        bool moved = false;
        for (int k : dirs) {
            int ny = y + dy[k];
            int nx = x + dx[k];

            if (inside(ny, nx) && maze[ny][nx] == '#') {
                maze[y + dy[k] / 2][x + dx[k] / 2] = '.';
                maze[ny][nx] = '.';
                stack.push_back({ny, nx});
                moved = true;
                break;
            }
        }

        if (!moved) {
            stack.pop_back();
        }
    }

    uniform_int_distribution<int> prob(0, 99);
    int breakChance = 30;

    for (int y = 1; y < H - 1; ++y) {
        for (int x = 1; x < W - 1; ++x) {
            if (maze[y][x] != '#') continue;

            bool canVertical = (maze[y-1][x] == '.' && maze[y+1][x] == '.');
            bool canHorizontal = (maze[y][x-1] == '.' && maze[y][x+1] == '.');

            if ((canVertical || canHorizontal) && prob(rng) < breakChance) {
                maze[y][x] = '.';
            }
        }
    }

    vector<pair<int,int>> emptyCells;
    for (int y = 1; y < H - 1; ++y) {
        for (int x = 1; x < W - 1; ++x) {
            if (maze[y][x] == '.') {
                emptyCells.push_back({x, y});
            }
        }
    }

    if (emptyCells.size() < 2) {
        maze[1][1] = '.';
        maze[H - 2][W - 2] = '.';
        emptyCells = {{1,1}, {W-2, H-2}};
    }

    shuffle(emptyCells.begin(), emptyCells.end(), rng);

    auto [sx, sy] = emptyCells[0];
    auto [gx, gy] = emptyCells[1];

    maze[sy][sx] = 'S';
    maze[gy][gx] = 'G';

    return maze;
}


int main() {
    int H = 21;
    int W = 31;

    vector<string> maze = generateMazeDFS(H, W);

    const int N = H * W;

    auto idFromCoord = [W](int x, int y) {
        return y * W + x;
    };

    pair<int,int> startPos{-1, -1}, goalPos{-1, -1};

    for (int y = 0; y < H; ++y) {
        for (int x = 0; x < W; ++x) {
            if (maze[y][x] == 'S') startPos = {x, y};
            if (maze[y][x] == 'G') goalPos  = {x, y};
        }
    }

    if (startPos.first == -1 || goalPos.first == -1) {
        cout << "Error: Start (S) or Goal (G) not found in the maze.\n";
        return 0;
    }

    int startId = idFromCoord(startPos.first, startPos.second);
    int goalId  = idFromCoord(goalPos.first, goalPos.second);

    CSR csr;
    csr.n = N;
    csr.coord.resize(N);

    for (int id = 0; id < N; ++id) {
        int y = id / W;
        int x = id % W;
        csr.coord[id] = {x, y};
    }

    vector<vector<pair<int,int>>> adj(N);

    const int dx4[4] = {0, 0, -1, 1};
    const int dy4[4] = {-1, 1, 0, 0};

    for (int id = 0; id < N; ++id) {
        int y = id / W;
        int x = id % W;
        if (maze[y][x] == '#') continue;

        for (int k = 0; k < 4; ++k) {
            int nx = x + dx4[k];
            int ny = y + dy4[k];
            if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
            if (maze[ny][nx] == '#') continue;

            int toId = ny * W + nx;
            adj[id].push_back({toId, 1});
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

    pair<int,int> player = startPos;
    int playerSteps = 0;
	bool reachedGoal = false;
	
    while (true) {
        drawMaze(maze, player);
        cout << "Your steps so far: " << playerSteps << "\n";

        if (player == goalPos) {
            cout << "You reached the goal!\n";
            reachedGoal = true;
            break;
        }

        cout << "Move with WASD (or press 'q' to skip to A*): ";
        char c;
        if (!(cin >> c)) {
            cout << "Input error. Exiting.\n";
            return 0;
        }
        if (c == 'q' || c == 'Q') {
            cout << "Switching to A* algorithm visualization...\n";
            break;
        }

        int nx = player.first;
        int ny = player.second;
        if (c == 'w' || c == 'W') ny--;
        if (c == 's' || c == 'S') ny++;
        if (c == 'a' || c == 'A') nx--;
        if (c == 'd' || c == 'D') nx++;

        if (nx < 0 || ny < 0 || nx >= W || ny >= H) {
            cout << "You cannot move outside the maze.\n";
            continue;
        }
        if (maze[ny][nx] == '#') {
            cout << "There is a wall in that direction.\n";
            continue;
        }

        // Successful move
        player = {nx, ny};
        playerSteps++;
    }

    cout << "\n=== Player summary ===\n";
    cout << "Your total steps: " << playerSteps;
    if (reachedGoal) {
        cout << " (you reached the goal)\n";
    } else {
        cout << " (you did NOT reach the goal)\n";
    }

    auto path = aStarCSR(csr, startId, goalId);

    if (path.empty()) {
        cout << "\nA* could not find any path.\n";
        return 0;
    }

    int aStarSteps = (int)path.size() - 1;

    cout << "\n=== A* summary ===\n";
    cout << "A* path length: " << aStarSteps << " steps.\n";

    cout << "\n=== Comparison ===\n";
    cout << "Your steps: " << playerSteps << "\n";
    cout << "A* steps : " << aStarSteps << "\n";

    if (reachedGoal) {
        int diff = playerSteps - aStarSteps;
        if (diff == 0) {
            cout << "Result: Perfect! You found an optimal path, same as A*.\n";
        } else if (diff > 0 && diff <= 5) {
            cout << "Result: Very good! You are only " << diff
                 << " steps longer than the optimal path.\n";
        } else if (diff > 5) {
            cout << "Result: A* is more efficient by " << diff
                 << " steps. You can try to improve your route!\n";
        } else {
            cout << "Result: Interesting, you somehow did better than A* (or there is a bug).\n";
        }
    } else {
        cout << "Note: You did not reach the goal, so the comparison is not fully fair.\n";
        cout << "Try again and see if you can match or beat A*'s step count!\n";
    }

    cout << "\nAnimating A* path...\n";

    vector<pair<int,int>> trail;
    for (size_t i = 0; i < path.size(); ++i) {
        pair<int,int> algoPos = path[i];
        trail.push_back(algoPos);
        drawMaze(maze, {-1, -1}, true, algoPos, trail);
        this_thread::sleep_for(chrono::milliseconds(200));
    }

    cout << "Done.\n";

    return 0;
}

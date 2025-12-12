#include <bits/stdc++.h>
using namespace std;

string setToStr(const set<string>& s){
    if(s.empty()) return "set()";
    string out = "{";
    bool first=true;
    for(const auto &v: s){
        if(!first) out += ", ";
        out += v;
        first = false;
    }
    out += "}";
    return out;
}

map<string, vector<string>> get_transpose(const map<string, vector<string>>& graph){
    map<string, vector<string>> transposed;
    // ensure all nodes present
    for(const auto &p: graph) transposed[p.first];
    for(const auto &p: graph){
        const string &u = p.first;
        for(const auto &v: p.second){
            transposed[v].push_back(u);
        }
    }
    return transposed;
}

vector<pair<string,string>> inverse_edges(const vector<string>& nodes,
                                          const vector<pair<string,string>>& edges){
    vector<pair<string,string>> inv;
    auto exists = [&](const string &a, const string &b){
        for(const auto &e: edges){
            if((e.first==a && e.second==b) ||
               (e.first==b && e.second==a))
                return true;
        }
        return false;
    };
    for(size_t i=0;i<nodes.size();++i){
        for(size_t j=i+1;j<nodes.size();++j){
            if(!exists(nodes[i], nodes[j]))
                inv.emplace_back(nodes[i], nodes[j]);
        }
    }
    return inv;
}

map<string, set<string>> graph_data;
vector< set<string> > maximal_cliques;

void bron_kerbosch(set<string> R, set<string> P, set<string> X, int depth=0){
    string indent(depth*2, ' ');
    cout << indent << "Step Call: R=" << setToStr(R)
         << ", P=" << setToStr(P) << ", X=" << setToStr(X) << "\n";

    if(P.empty() && X.empty()){
        cout << indent << "-> Found Maximal Clique: " << setToStr(R) << "\n";
        maximal_cliques.push_back(R);
        return;
    }

    vector<string> Pvec(P.begin(), P.end());
    sort(Pvec.begin(), Pvec.end());

    for(const auto &v: Pvec){
        set<string> neigh = graph_data[v];

        set<string> R2 = R; R2.insert(v);

        set<string> P2;
        for(const auto &u: P)
            if(neigh.count(u)) P2.insert(u);

        set<string> X2;
        for(const auto &u: X)
            if(neigh.count(u)) X2.insert(u);

        bron_kerbosch(R2, P2, X2, depth+1);

        P.erase(v);
        X.insert(v);
    }
}

int main(){
    cout << "--- PROBLEM 1 OUTPUT ---\n";

    map<string, vector<string>> my_directed_graph = {
        {"A", {"B"}},
        {"B", {"C"}},
        {"C", {"A"}}
    };

    cout << "Original Directed: {";
    bool f=true;
    for(auto &p: my_directed_graph){
        if(!f) cout << ", ";
        cout << "\"" << p.first << "\": [";
        for(size_t i=0;i<p.second.size();++i){
            if(i) cout << ", ";
            cout << "\"" << p.second[i] << "\"";
        }
        cout << "]";
        f=false;
    }
    cout << "}\n";

    auto trans = get_transpose(my_directed_graph);
    cout << "Transposed: {";
    f=true;
    for(auto &p: trans){
        if(!f) cout << ", ";
        cout << "\"" << p.first << "\": [";
        for(size_t i=0;i<p.second.size();++i){
            if(i) cout << ", ";
            cout << "\"" << p.second[i] << "\"";
        }
        cout << "]";
        f=false;
    }
    cout << "}\n\n";

    vector<string> nodes = {"A","B","C","D"};
    vector<pair<string,string>> undirected_edges = {
        {"A","B"}, {"B","C"}, {"C","D"}
    };

    cout << "Original Edges: [";
    for(size_t i=0;i<undirected_edges.size();++i){
        if(i) cout << ", ";
        cout << "(" << undirected_edges[i].first << ", "
             << undirected_edges[i].second << ")";
    }
    cout << "]\n";

    auto inv = inverse_edges(nodes, undirected_edges);

    cout << "Inverse Edges: [";
    for(size_t i=0;i<inv.size();++i){
        if(i) cout << ", ";
        cout << "(" << inv[i].first << ", " << inv[i].second << ")";
    }
    cout << "]\n\n";

    cout << "--- PROBLEM 2: BRON-KERBOSCH TRACE ---\n\n";

    graph_data = {
        {"A", {"B","C"}},
        {"B", {"A","C"}},
        {"C", {"A","B","D"}},
        {"D", {"C"}}
    };

    set<string> R, P, X;
    P.insert("A"); P.insert("B"); P.insert("C"); P.insert("D");

    cout << "Starting Algorithm...\n";
    bron_kerbosch(R, P, X);

    cout << "\n--- RESULTS ---\n";
    cout << "All Maximal Cliques Found:\n";
    for(auto &c: maximal_cliques){
        cout << setToStr(c) << "\n";
    }

    size_t best = 0;
    set<string> best_c;
    for(auto &c: maximal_cliques){
        if(c.size() > best){
            best = c.size();
            best_c = c;
        }
    }

    cout << "Maximum Clique is: " << setToStr(best_c)
         << " with size " << best << "\n";

    return 0;
}

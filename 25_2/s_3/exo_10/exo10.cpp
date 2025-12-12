#include <iostream>
#include <iomanip>
#include <cmath>

using namespace std;

double bayes_prob(double prevalence, double sens, double spec) {
    double tp = sens * prevalence;
    double fp = (1.0 - spec) * (1.0 - prevalence);
    return tp / (tp + fp);
}

double entropy(double p) {
    if (p <= 0.0 || p >= 1.0) return 0.0;
    return -(p * log2(p) + (1.0 - p) * log2(1.0 - p));
}

int main() {

    cout << "Problem Set #10 - computed answers (C++)\r\n\r\n";

    cout << "Problem 1 classifications:\r\n";
    cout << "1) {find max, linear search, shortest path in unweighted graph, matrix multiplication} -> P\r\n";
    cout << "2) {sorting, Dijkstra (non-negative), BFS, DFS, merge sort, quicksort} -> P\r\n";
    cout << "3) {sudoku (decision)} -> NP-complete\r\n";
    cout << "4) {3-coloring, scheduling with conflicts} -> NP-complete\r\n";
    cout << "5) {TSP (decision), Hamiltonian Cycle, Clique} -> NP-complete (optimization NP-hard)\r\n";
    cout << "6) {cryptography, factoring large integers} -> hard, factoring not known NP-complete\r\n";
    cout << "7) {Halting Problem, Busy Beaver} -> Undecidable\r\n\r\n";

    double prevalence = 0.001;
    double sens = 0.99;
    double spec = 0.99;

    double post = bayes_prob(prevalence, sens, spec);

    cout << fixed << setprecision(6);
    cout << "Problem 2 (Bayes):\r\n";
    cout << "Prevalence = " << prevalence 
         << ", sensitivity = " << sens 
         << ", specificity = " << spec << "\r\n";
    cout << "P(disease | test+) = " << post 
         << " (" << post * 100.0 << "%)\r\n\r\n";

    double pA=0.5, pB=0.99, pC=0.01;

    cout << "Problem 3 (Shannon entropy):\r\n";
    cout << "Coin A p=0.50 -> H = " << entropy(pA) << " bits\r\n";
    cout << "Coin B p=0.99 -> H = " << entropy(pB) << " bits\r\n";
    cout << "Coin C p=0.01 -> H = " << entropy(pC) << " bits\r\n";

    return 0;
}

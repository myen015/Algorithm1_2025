#include <bits/stdc++.h>
using namespace std;

bool nand_gate(bool a, bool b) {
    return !(a && b);
}

bool not_via_nand(bool x) {
    return nand_gate(x, x);
}

bool and_via_nand(bool x, bool y) {
    bool t = nand_gate(x, y);
    return nand_gate(t, t);
}

bool or_via_nand(bool x, bool y) {
    bool a = nand_gate(x, x);
    bool b = nand_gate(y, y);
    return nand_gate(a, b);
}

string bits_to_string(const vector<int>& v) {
    string s;
    for (int b : v) s.push_back(b ? '1' : '0');
    return s;
}

void problem1_counting(int n, int m) {
    cout << "Problem 1 — counting finite functions\n";
    cout << "Domain size = 2^" << n << " inputs.\n";
    cout << "Number of functions to {0,1}            = 2^(2^" << n << ")\n";
    cout << "Number of functions to {-1,0,1}         = 3^(2^" << n << ")\n";
    cout << "Number of functions to {0,1}^" << m << " = 2^(" << m << " * 2^" << n << ")\n";
    cout << "(Exact numeric values grow extremely fast; numeric computation only for small n below.)\n\n";

    if (n <= 5 && m <= 5) {
        unsigned long long domain = 1ULL << n; 
        auto pow_small = [&](unsigned long long base, unsigned long long exp){
            vector<int> digits(1,1);
            for (unsigned long long i=0;i<exp;i++){
                int carry=0;
                for (size_t j=0;j<digits.size();j++){
                    long long prod = 1LL*digits[j]*base + carry;
                    digits[j] = prod % 10;
                    carry = prod / 10;
                }
                while (carry) {
                    digits.push_back(carry%10);
                    carry/=10;
                }
            }
            string s;
            for (auto it = digits.rbegin(); it != digits.rend(); ++it) s.push_back(char('0'+*it));
            return s;
        };

        unsigned long long k1 = 2;
        unsigned long long k2 = 3;
        unsigned long long k3 = 1ULL << m;
        cout << "Numeric (small n,m) results:\n";
        cout << "2^(2^" << n << ") = " << pow_small(k1, domain) << "\n";
        cout << "3^(2^" << n << ") = " << pow_small(k2, domain) << "\n";
        cout << k3 << "^(2^" << n << ") = " << pow_small(k3, domain) << "\n";
    } else {
        cout << "n or m too large for exact numeric printing here (values extremely large).\n";
    }
    cout << "\n";
}

void problem2_nand_constructions() {
    cout << "Problem 2 — NAND constructions and truth tables\n";
    cout << "NAND truth table (A B | A NAND B):\n";
    cout << "A B | NAND | NOT(A) | AND_via_NAND | OR_via_NAND\n";
    for (int a=0;a<=1;a++){
        for (int b=0;b<=1;b++){
            bool nandv = nand_gate(a,b);
            bool notv = not_via_nand(a);
            bool andv = and_via_nand(a,b);
            bool orv  = or_via_nand(a,b);
            cout << a << " " << b << " |   " << nandv << "   |    " << notv << "    |      " << andv << "       |     " << orv << "\n";
        }
    }
    cout << "\n";
    cout << "Verification: NOT(x)=x NAND x, AND(x,y)=(x NAND y) NAND (x NAND y), OR(x,y)=(x NAND x) NAND (y NAND y)\n\n";
    cout << "Theorem remark: since NOT/AND/OR are implementable with ≤3 NANDs each, any n-gate circuit can be simulated with at most 3n NAND gates.\n\n";
}

void problem3_dnf_and_complexity(int n, const vector<int>& truth_table) {
    cout << "Problem 3 — Universality and circuit-size estimate\n";
    int domain = 1<<n;
    if ((int)truth_table.size() != domain) {
        cout << "Error: truth table size mismatch.\n";
        return;
    }
    int ones = 0;
    for (int v : truth_table) if (v) ones++;
    cout << "Given n=" << n << ", truth table has " << ones << " minterm(s) with value 1 out of " << domain << ".\n";
    cout << "Each minterm δ_x can be implemented as an AND of n literals (a literal may be a variable or its negation), so building one minterm needs O(n) gates.\n";
    cout << "Combining all needed minterms with OR produces F; worst-case number of minterms is 2^n, so the naive DNF circuit size is O(n * 2^n).\n\n";

    if (domain <= 16) {
        cout << "DNF (sum of minterms) representation (minterms shown as binary patterns):\n";
        bool first = true;
        for (int x=0;x<domain;x++){
            if (truth_table[x]) {
                if (!first) cout << " OR ";
                cout << "(";
                for (int bit=0; bit<n; ++bit){
                    int idx = n-1-bit;
                    bool bitval = (x >> idx) & 1;
                    if (bit) cout << " AND ";
                    if (bitval) cout << "v" << (idx);
                    else cout << "¬v" << (idx);
                }
                cout << ")";
                first = false;
            }
        }
        cout << "\n\n";
    } else {
        cout << "DNF not printed (domain too large to display minterms).\n\n";
    }

    if (ones == 0) {
        cout << "If no minterms are 1, constant 0 function requires 0 gates.\n";
    } else {
        long long gates_for_minterms = 1LL * ones * max(0, n - 1);
        long long or_gates = max(0, ones - 1); 
        cout << "Rough gate estimate (binary gates): minterms ≈ " << gates_for_minterms
             << ", OR-combine ≈ " << or_gates << ", total ≈ " << (gates_for_minterms + or_gates) << ".\n";
        cout << "This is consistent with O(n * 2^n) worst-case complexity.\n\n";
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "=== Fundamental Algorithm Techniques - Problem Set #9 demo ===\n\n";

    int n1 = 3; 
    int m1 = 2;
    problem1_counting(n1, m1);

    problem2_nand_constructions();

    int n3 = 3;
    vector<int> tt(1<<n3, 0);
    tt[3] = 1; tt[5] = 1; tt[6] = 1;
    problem3_dnf_and_complexity(n3, tt);

    cout << "Notes:\n";
    cout << "- To use this code for custom inputs, edit n1,m1 or provide a custom truth table for Problem 3.\n";
    cout << "- Exact numeric printing in Problem 1 is feasible only for small n,m because values grow double-exponentially.\n";

    return 0;
}

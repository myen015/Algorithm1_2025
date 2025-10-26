#include <bits/stdc++.h>
using namespace std;

struct BigInt {
    static const uint32_t BASE = 1000000000;
    vector<uint32_t> d;
    BigInt(unsigned long long v = 0) { 
        while (v) { d.push_back(uint32_t(v % BASE)); v /= BASE; }
        if (d.empty()) d.push_back(0);
    }
    BigInt(const string &s) {
        int len = s.size();
        for (int i = len; i > 0; i -= 9) {
            int l = max(0, i - 9);
            int r = i - l;
            d.push_back((uint32_t)stoul(s.substr(l, r)));
        }
        trim();
    }
    void trim() {
        while (d.size() > 1 && d.back() == 0) d.pop_back();
    }
    string toString() const {
        stringstream ss;
        int n = d.size();
        ss << d.empty() ? 0 : d.back();
        if (!d.empty()) {
            ss.str(); 
        }
        if (d.empty()) return "0";
        ss.str("");
        ss.clear();
        ss << d.back();
        for (int i = (int)d.size() - 2; i >= 0; --i) {
            ss << setw(9) << setfill('0') << d[i];
        }
        return ss.str();
    }
    static BigInt add(const BigInt &a, const BigInt &b) {
        BigInt res;
        res.d.assign(max(a.d.size(), b.d.size()) + 1, 0);
        uint64_t carry = 0;
        size_t i = 0;
        for (; i < a.d.size() || i < b.d.size(); ++i) {
            uint64_t av = i < a.d.size() ? a.d[i] : 0;
            uint64_t bv = i < b.d.size() ? b.d[i] : 0;
            uint64_t sum = av + bv + carry;
            res.d[i] = uint32_t(sum % BASE);
            carry = sum / BASE;
        }
        if (carry) res.d[i++] = uint32_t(carry);
        res.d.resize(i);
        res.trim();
        return res;
    }
    static BigInt mul(const BigInt &a, const BigInt &b) {
        BigInt res;
        res.d.assign(a.d.size() + b.d.size(), 0);
        for (size_t i = 0; i < a.d.size(); ++i) {
            uint64_t carry = 0;
            uint64_t ai = a.d[i];
            for (size_t j = 0; j < b.d.size() || carry; ++j) {
                uint64_t bj = j < b.d.size() ? b.d[j] : 0;
                uint64_t cur = res.d[i + j] + ai * bj + carry;
                res.d[i + j] = uint32_t(cur % BASE);
                carry = cur / BASE;
            }
        }
        res.trim();
        return res;
    }
};

struct Mat {
    BigInt a,b,c,d;
    Mat(): a(1), b(0), c(0), d(1) {}
    Mat(const BigInt &a_, const BigInt &b_, const BigInt &c_, const BigInt &d_): a(a_), b(b_), c(c_), d(d_) {}
};

Mat mul(const Mat &x, const Mat &y) {
    return Mat(
        BigInt::add(BigInt::mul(x.a, y.a), BigInt::mul(x.b, y.c)),
        BigInt::add(BigInt::mul(x.a, y.b), BigInt::mul(x.b, y.d)),
        BigInt::add(BigInt::mul(x.c, y.a), BigInt::mul(x.d, y.c)),
        BigInt::add(BigInt::mul(x.c, y.b), BigInt::mul(x.d, y.d))
    );
}

Mat mat_pow(Mat base, unsigned long long exp) {
    Mat res;
    while (exp) {
        if (exp & 1) res = mul(res, base);
        base = mul(base, base);
        exp >>= 1;
    }
    return res;
}

BigInt fib(unsigned long long n) {
    if (n == 0) return BigInt(0);
    Mat M(BigInt(1), BigInt(1), BigInt(1), BigInt(0));
    Mat P = mat_pow(M, n);
    return P.c;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    unsigned long long n;
    cout<< "Enter a non-negative integer n to compute the nth Fibonacci number: ";
    if (!(cin >> n)) return 0;
    BigInt fn = fib(n);
    cout << fn.toString() << '\n';
    return 0;
}

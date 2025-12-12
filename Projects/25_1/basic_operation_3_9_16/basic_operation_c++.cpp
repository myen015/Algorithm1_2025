#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <string>

using namespace std;
using Digits = vector<int>;

// Convert int to big integer (LSB first, base 10)
Digits to_bigint(long long n) {
    if (n == 0) return {0};
    Digits digits;
    while (n > 0) {
        digits.push_back(n % 10);
        n /= 10;
    }
    return digits;
}

// Convert big integer back to int
long long from_bigint(const Digits& digits) {
    long long n = 0;
    for (int i = digits.size() - 1; i >= 0; i--) {
        n = n * 10 + digits[i];
    }
    return n;
}

// Addition
Digits add(const Digits& a, const Digits& b) {
    Digits result;
    int carry = 0;
    size_t i = 0, j = 0;
    while (i < a.size() || j < b.size() || carry) {
        int val = carry;
        if (i < a.size()) val += a[i++];
        if (j < b.size()) val += b[j++];
        result.push_back(val % 10);
        carry = val / 10;
    }
    return result;
}

// Subtraction (assumes a >= b)
Digits subtract(Digits a, const Digits& b) {
    int borrow = 0;
    for (size_t i = 0; i < a.size(); i++) {
        int val = a[i] - borrow;
        if (i < b.size()) val -= b[i];
        if (val < 0) {
            val += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }
        a[i] = val;
    }
    while (a.size() > 1 && a.back() == 0) {
        a.pop_back();
    }
    return a;
}

// Simple multiplication
Digits multiply_simple(const Digits& a, const Digits& b) {
    Digits result(a.size() + b.size(), 0);
    for (size_t i = 0; i < a.size(); i++) {
        for (size_t j = 0; j < b.size(); j++) {
            result[i + j] += a[i] * b[j];
        }
    }
    int carry = 0;
    for (size_t i = 0; i < result.size(); i++) {
        int val = result[i] + carry;
        result[i] = val % 10;
        carry = val / 10;
    }
    while (result.size() > 1 && result.back() == 0) {
        result.pop_back();
    }
    return result;
}

// Shift left (multiply by 10^k)
Digits shift_left(const Digits& digits, int k) {
    Digits result(k);
    result.insert(result.end(), digits.begin(), digits.end());
    return result;
}

// Normalize digits (handle carries)
Digits normalize(Digits digits) {
    int carry = 0;
    for (size_t i = 0; i < digits.size(); i++) {
        int val = digits[i] + carry;
        digits[i] = val % 10;
        carry = val / 10;
    }
    while (carry) {
        digits.push_back(carry % 10);
        carry /= 10;
    }
    while (digits.size() > 1 && digits.back() == 0) {
        digits.pop_back();
    }
    return digits;
}

// Karatsuba Multiplication
Digits karatsuba(Digits a, Digits b) {
    if (a.size() < 2 || b.size() < 2) {
        return multiply_simple(a, b);
    }
    int n = max(a.size(), b.size());
    a.resize(n, 0);
    b.resize(n, 0);
    int m = n / 2;

    Digits al(a.begin(), a.begin() + m);
    Digits ah(a.begin() + m, a.end());
    Digits bl(b.begin(), b.begin() + m);
    Digits bh(b.begin() + m, b.end());

    Digits zl = karatsuba(al, bl);
    Digits zr = karatsuba(ah, bh);
    Digits zm = karatsuba(add(al, ah), add(bl, bh));
    zm = subtract(zm, add(zl, zr));

    zm = shift_left(zm, m);
    zl = shift_left(zl, 0);
    Digits zr_shifted = shift_left(zr, 2 * m);

    return normalize(add(add(zl, zm), zr_shifted));
}

// Division (long division)
pair<Digits, Digits> divide(Digits a, const Digits& b) {
    if (from_bigint(b) == 0) throw runtime_error("Division by zero");

    Digits quotient;
    Digits remainder;

    for (int i = a.size() - 1; i >= 0; i--) {
        remainder = shift_left(remainder, 1);
        remainder.push_back(a[i]);
        remainder = normalize(remainder);

        int q_digit = 0;
        while (from_bigint(remainder) >= from_bigint(b)) {
            remainder = subtract(remainder, b);
            q_digit++;
        }
        quotient.push_back(q_digit);
    }

    reverse(quotient.begin(), quotient.end());
    while (quotient.size() > 1 && quotient[0] == 0) {
        quotient.erase(quotient.begin());
    }
    if (quotient.empty()) quotient = {0};

    return {quotient, remainder};
}

// Benchmark function
void benchmark_operations(int size = 100) {
    long long a_int = 1;
    for (int i = 0; i < size; i++) a_int = a_int * 10 + 9;  // 999...9
    long long b_int = a_int / 3;

    Digits a = to_bigint(a_int);
    Digits b = to_bigint(b_int);

    cout << "\n=== C++ Benchmark for " << size << "-digit numbers (100 runs each) ===" << endl;
    cout << "Operation | Time (ms)" << endl;
    cout << "----------|----------" << endl;

    // Addition
    auto start = chrono::high_resolution_clock::now();
    for (int i = 0; i < 100; i++) {
        volatile auto result = add(a, b);
    }
    auto end = chrono::high_resolution_clock::now();
    auto add_time = chrono::duration<double, milli>(end - start).count();
    cout << "Add       | " << add_time << endl;

    // Subtraction
    start = chrono::high_resolution_clock::now();
    for (int i = 0; i < 100; i++) {
        volatile auto result = subtract(a, b);
    }
    end = chrono::high_resolution_clock::now();
    auto sub_time = chrono::duration<double, milli>(end - start).count();
    cout << "Sub       | " << sub_time << endl;

    // Multiplication (Karatsuba)
    start = chrono::high_resolution_clock::now();
    for (int i = 0; i < 100; i++) {
        volatile auto result = karatsuba(a, b);
    }
    end = chrono::high_resolution_clock::now();
    auto mul_time = chrono::duration<double, milli>(end - start).count();
    cout << "Mul       | " << mul_time << endl;

    // Division
    start = chrono::high_resolution_clock::now();
    for (int i = 0; i < 100; i++) {
        volatile auto result = divide(a, b);
    }
    end = chrono::high_resolution_clock::now();
    auto div_time = chrono::duration<double, milli>(end - start).count();
    cout << "Div       | " << div_time << endl;
}

int main() {
    // Test small values
    cout << "=== C++ Big Integer Tests ===" << endl;
    cout << "123 + 456 = " << from_bigint(add(to_bigint(123), to_bigint(456))) << endl;
    cout << "123 * 456 = " << from_bigint(karatsuba(to_bigint(123), to_bigint(456))) << endl;

    auto [q, r] = divide(to_bigint(123), to_bigint(3));
    cout << "123 // 3 = " << from_bigint(q) << " remainder " << from_bigint(r) << endl;

    // Benchmark
    benchmark_operations(100);

    return 0;
}

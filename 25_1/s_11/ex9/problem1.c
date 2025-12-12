#include <stdio.h>
#include <math.h>

double count_functions(int base, int n)
{

    double domain_size = pow(2.0, n);

    return pow((double)base, domain_size);
}

int main()
{
    int n = 3;
    int m = 2;

    printf("--- Problem 1: Number of Finite Functions (n=%d) ---\n\n", n);

    double count_case1 = count_functions(2, n);
    printf("1. Output {0, 1} (Base=2):\n");
    printf("   Formula: 2^(2^n)\n");
    printf("   Result for n=%d: 2^(2^3) = 2^8 = %.0f functions\n\n", n, count_case1);

    double count_case2 = count_functions(3, n);
    printf("2. Output {-1, 0, 1} (Base=3):\n");
    printf("   Formula: 3^(2^n)\n");
    printf("   Result for n=%d: 3^(2^3) = 3^8 = %.0f functions\n\n", n, count_case2);

    int base_case3 = (int)pow(2.0, m);
    double count_case3 = count_functions(base_case3, n);
    printf("3. Output {0, 1}^m (m=%d, Base=2^m=%d):\n", m, base_case3);
    printf("   Formula: (2^m)^(2^n) = 2^(m * 2^n)\n");
    printf("   Result for n=%d, m=%d: 2^(2 * 8) = 2^16 = %.0f functions\n", n, m, count_case3);

    return 0;
}
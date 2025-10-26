#include <stdio.h>

void multiplyMatrix(long long a[2][2], long long b[2][2])
{
    long long x = a[0][0] * b[0][0] + a[0][1] * b[1][0];
    long long y = a[0][0] * b[0][1] + a[0][1] * b[1][1];
    long long z = a[1][0] * b[0][0] + a[1][1] * b[1][0];
    long long w = a[1][0] * b[0][1] + a[1][1] * b[1][1];

    a[0][0] = x;
    a[0][1] = y;
    a[1][0] = z;
    a[1][1] = w;
}

void powerMatrix(long long F[2][2], int n)
{
    if (n == 0 || n == 1)
        return;

    long long M[2][2] = {{1, 1}, {1, 0}};

    powerMatrix(F, n / 2);
    multiplyMatrix(F, F);

    if (n % 2 != 0)
        multiplyMatrix(F, M);
}

long long fibonacci(int n)
{
    if (n == 0)
        return 0;

    long long F[2][2] = {{1, 1}, {1, 0}};
    powerMatrix(F, n - 1);
    return F[0][0];
}

int main()
{
    int n;
    printf("Enter n: ");
    scanf("%d", &n);

    printf("Fibonacci(%d) = %lld\n", n, fibonacci(n));
    return 0;
}

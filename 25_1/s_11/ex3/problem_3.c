#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define N 2000 // vector length
#define W 5    // number of ones
#define TRIALS 10000

void random_vector(int v[], int n, int w)
{
    for (int i = 0; i < n; i++)
        v[i] = 0;
    for (int i = 0; i < w; i++)
    {
        int pos;
        do
        {
            pos = rand() % n;
        } while (v[pos] == 1);
        v[pos] = 1;
    }
}

int dot(int x[], int y[], int n)
{
    int s = 0;
    for (int i = 0; i < n; i++)
        s += x[i] * y[i];
    return s;
}

int main()
{
    srand(time(NULL));
    int x[N], y[N];
    double sum = 0, sum2 = 0;

    for (int t = 0; t < TRIALS; t++)
    {
        random_vector(x, N, W);
        random_vector(y, N, W);
        int overlap = dot(x, y, N);
        double sim = (double)overlap / (W * W);
        sum += sim;
        sum2 += sim * sim;
    }

    double mean = sum / TRIALS;
    double var = sum2 / TRIALS - mean * mean;

    printf("Mean similarity = %.6f\n", mean);
    printf("Variance = %.6f\n", var);
    return 0;
}

#include <stdio.h>
#include <stdbool.h>
#include <math.h>

#define N 3

const bool TRUTH_TABLE_F[] = {
    false, true, false, true, false, true, true, true};

bool minterm_delta_x(int target_x_index, int current_input_index, int n)
{
    for (int i = 0; i < n; i++)
    {

        bool target_bit = (target_x_index >> i) & 1;
        bool current_bit = (current_input_index >> i) & 1;

        if (target_bit != current_bit)
        {
            return false;
        }
    }
    return true;
}

bool evaluate_f_via_dnf(int current_input_index, int n)
{
    bool result = false;
    int num_inputs = 1 << n;

    for (int target_x_index = 0; target_x_index < num_inputs; target_x_index++)
    {

        if (TRUTH_TABLE_F[target_x_index] == true)
        {

            bool delta_x_output = minterm_delta_x(target_x_index, current_input_index, n);

            result = result || delta_x_output;
        }
    }
    return result;
}

int main()
{
    printf("Problem 3: Circuit Universality (DNF Construction)\n");
    printf("Demonstrating F(A, B, C) via DNF (n=%d)\n\n", N);

    printf("Input (A B C) | Expected F | DNF Computed F | Match?\n");

    int num_inputs = 1 << N;
    for (int i = 0; i < num_inputs; i++)
    {

        printf("  (%d %d %d)   |",
               (i >> 2) & 1,
               (i >> 1) & 1,
               i & 1);

        bool expected = TRUTH_TABLE_F[i];
        bool computed = evaluate_f_via_dnf(i, N);

        printf("     %d      |        %d       |   %s\n",
               expected,
               computed,
               (expected == computed ? "YES" : "NO"));
    }

    printf("\nConclusion: Any function F is computable via the DNF structure, \n");
    printf("which requires O(n) gates for each of the 2^n minterms, total O(n * 2^n).\n");

    return 0;
}
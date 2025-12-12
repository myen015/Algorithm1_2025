

#include <stdio.h>
#include <stdbool.h>

bool NAND(bool A, bool B)
{

    return !(A && B);
}

bool NOT_from_NAND(bool A)
{
    return NAND(A, A);
}

bool AND_from_NAND(bool A, bool B)
{
    bool nand_result = NAND(A, B);

    return NOT_from_NAND(nand_result);
}

bool OR_from_NAND(bool A, bool B)
{
    bool not_A = NOT_from_NAND(A);
    bool not_B = NOT_from_NAND(B);

    return NAND(not_A, not_B);
}

void print_truth_table(const char *operation, bool (*func)(bool, bool))
{
    printf("\n%s Truth Table (Built with NAND)\n", operation);

    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            bool A = i;
            bool B = j;
            printf("%d | %d | %d\n", A, B, func(A, B));
        }
    }
}

int main()
{
    printf("Problem 2: NAND Universality Demonstration\n");

    printf("\nNOT Truth Table (Built with 1 NAND)\n");

    printf("0 | %d\n", NOT_from_NAND(0));
    printf("1 | %d\n", NOT_from_NAND(1));

    print_truth_table("AND", AND_from_NAND);

    print_truth_table("OR", OR_from_NAND);

    return 0;
}
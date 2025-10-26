#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "array_utils.h"

#define MAX_SIZE 10000
#define MIN_SIZE 100

int *generateRandomArray(int *size)
{
    srand(time(NULL));
    *size = rand() % (MAX_SIZE - MIN_SIZE + 1) + MIN_SIZE;
    int *arr = (int *)malloc(*size * sizeof(int));
    if (!arr)
    {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    for (int i = 0; i < *size; i++)
    {
        arr[i] = rand() % 100000;
    }
    return arr;
}

void displayArray(int *arr, int size)
{
    for (int i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

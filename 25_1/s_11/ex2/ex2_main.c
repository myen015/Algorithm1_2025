// Nursultan Zhakypzhan
// Course: Fundamental Algorithmic Techniques
// Assignment: ex2
// Date: 2025-10-12
// Description: This program tests and compares various sorting algorithms on a randomly generated array.

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include "array_utils.h"
#include "ex2.h"

void testSorts()
{
    int size;
    int *arr = generateRandomArray(&size);
    int *copy = (int *)malloc(size * sizeof(int));

    FILE *file = fopen("README.md", "a");
    if (!file)
    {
        printf("Error: cannot open README.md\n");
        return;
    }

    fprintf(file, "============================\n");
    fprintf(file, "Array size: %d\n", size);
    printf("Array size: %d\n", size);

    clock_t start, end;
    double duration;

    // --- Bubble Sort ---
    memcpy(copy, arr, size * sizeof(int));
    start = clock();
    bubbleSort(copy, size);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Bubble Sort: %.6f sec\n", duration);
    fprintf(file, "Bubble Sort: %.6f sec\n", duration);

    // --- Quick Sort (standard) ---
    memcpy(copy, arr, size * sizeof(int));
    start = clock();
    quickSort(copy, 0, size - 1);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Quick Sort (standard): %.6f sec\n", duration);
    fprintf(file, "Quick Sort (standard): %.6f sec\n", duration);

    // --- Quick Sort (random pivot) ---
    memcpy(copy, arr, size * sizeof(int));
    start = clock();
    quickSortRandomPivot(copy, 0, size - 1);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Quick Sort (random pivot): %.6f sec\n", duration);
    fprintf(file, "Quick Sort (random pivot): %.6f sec\n", duration);

    // --- Quick Sort (average pivot) ---
    memcpy(copy, arr, size * sizeof(int));
    start = clock();
    quickSortAveragePivot(copy, 0, size - 1);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Quick Sort (average pivot): %.6f sec\n", duration);
    fprintf(file, "Quick Sort (average pivot): %.6f sec\n", duration);

    // --- Merge Sort ---
    memcpy(copy, arr, size * sizeof(int));
    start = clock();
    mergeSort(copy, 0, size - 1);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Merge Sort: %.6f sec\n", duration);
    fprintf(file, "Merge Sort: %.6f sec\n", duration);

    // --- Heap Sort ---
    memcpy(copy, arr, size * sizeof(int));
    start = clock();
    heapSort(copy, size);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Heap Sort: %.6f sec\n", duration);
    fprintf(file, "Heap Sort: %.6f sec\n", duration);

    fprintf(file, "\n");
    fclose(file);

    free(arr);
    free(copy);
}

int main()
{
    testSorts();
    printf("\nResults written to README.md\n");
    return 0;
}

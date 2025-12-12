#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "ex2.h"

static void swap(int *a, int *b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

// ---------- Bubble Sort ----------
void bubbleSort(int arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - i - 1; j++)
            if (arr[j] > arr[j + 1])
                swap(&arr[j], &arr[j + 1]);
}

// ---------- Quick Sort (standard pivot = last element) ----------
static int partition(int arr[], int low, int high)
{
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++)
    {
        if (arr[j] < pivot)
        {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

void quickSort(int arr[], int low, int high)
{
    if (low < high)
    {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// ---------- Quick Sort (RANDOM pivot) ----------
static int partitionRandom(int arr[], int low, int high)
{
    int randomIndex = low + rand() % (high - low + 1);
    swap(&arr[randomIndex], &arr[high]); // move random pivot to end
    return partition(arr, low, high);
}

void quickSortRandomPivot(int arr[], int low, int high)
{
    if (low < high)
    {
        int pi = partitionRandom(arr, low, high);
        quickSortRandomPivot(arr, low, pi - 1);
        quickSortRandomPivot(arr, pi + 1, high);
    }
}

// ---------- Quick Sort (AVERAGE pivot of low, mid, high) ----------
static int partitionAveragePivot(int arr[], int low, int high)
{
    int mid = low + (high - low) / 2;
    int avg = (arr[low] + arr[mid] + arr[high]) / 3;

    // Find index of element closest to avg
    int pivotIndex = low;
    int diff = abs(arr[low] - avg);
    if (abs(arr[mid] - avg) < diff)
    {
        pivotIndex = mid;
        diff = abs(arr[mid] - avg);
    }
    if (abs(arr[high] - avg) < diff)
        pivotIndex = high;

    swap(&arr[pivotIndex], &arr[high]); // move chosen pivot to end
    return partition(arr, low, high);
}

void quickSortAveragePivot(int arr[], int low, int high)
{
    if (low < high)
    {
        int pi = partitionAveragePivot(arr, low, high);
        quickSortAveragePivot(arr, low, pi - 1);
        quickSortAveragePivot(arr, pi + 1, high);
    }
}

// ---------- Merge Sort ----------
static void merge(int arr[], int l, int m, int r)
{
    int n1 = m - l + 1, n2 = r - m;
    int *L = (int *)malloc(n1 * sizeof(int));
    int *R = (int *)malloc(n2 * sizeof(int));
    for (int i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2)
        arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
    while (i < n1)
        arr[k++] = L[i++];
    while (j < n2)
        arr[k++] = R[j++];

    free(L);
    free(R);
}

void mergeSort(int arr[], int l, int r)
{
    if (l < r)
    {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

// ---------- Heap Sort ----------
static void heapify(int arr[], int n, int i)
{
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;

    if (l < n && arr[l] > arr[largest])
        largest = l;
    if (r < n && arr[r] > arr[largest])
        largest = r;

    if (largest != i)
    {
        swap(&arr[i], &arr[largest]);
        heapify(arr, n, largest);
    }
}

void heapSort(int arr[], int n)
{
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);
    for (int i = n - 1; i > 0; i--)
    {
        swap(&arr[0], &arr[i]);
        heapify(arr, i, 0);
    }
}

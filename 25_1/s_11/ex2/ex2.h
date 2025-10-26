#ifndef SORTING_ALGORITHMS_H
#define SORTING_ALGORITHMS_H

void bubbleSort(int arr[], int n);
void quickSort(int arr[], int low, int high);
void quickSortRandomPivot(int arr[], int low, int high);
void quickSortAveragePivot(int arr[], int low, int high);
void mergeSort(int arr[], int l, int r);
void heapSort(int arr[], int n);

#endif

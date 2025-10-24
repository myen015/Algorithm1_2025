This repository has implementations of some type of sorting algorithms: Bad_sort, Quick sort, Heap sort, and Merge sort. 

Bad Sort: A simple sorting algorithm that repeatedly steps through the list, compares adjacent items, and swaps them if they are in the wrong order.

Quick Sort: A divide-and-conquer algorithm that selects a pivot element and partitions the array around the pivot, then recursively sorts the partitions.

Heap Sort: A comparison-based sorting algorithm that builds a max heap from the list and extracts the maximum element to construct the sorted array.

Merge Sort: A divide-and-conquer algorithm that divides the list into halves, recursively sorts them, and then merges the sorted halves back together.


Code inputs:
First input: An integer n which is size of array.

Second input: Array of integers

Third input: Variable k which represents which type of sorting you want to use:

1: Bad Sort

2: Quick Sort

3: Heap Sort

4: Merge Sort

FOr instance:

Input:

5
3 1 4 1 5
2


Output (Quick Sort):

1 1 3 4 5


Functions:
bad_sort(arr): Implements the bad sort algorithm.

rand_partition(arr, l, r): Partitions the array around a pivot for quick sort.

quick_sort(arr, l, r): Recursively sorts the array using the quick sort algorithm.

merge(v, l, m, r, tmp): Merges two sorted subarrays for merge sort.

merge_sort(v, l, r, tmp): Recursively sorts the array using the merge sort algorithm.

heapify(v, n, i): Ensures the max heap property for heap sort.

heap_sort(v): Sorts the array using heap sort.

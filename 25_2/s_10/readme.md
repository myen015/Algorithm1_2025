# Sorting Algorithms

Coded 4 different ways to sort numbers:

1. **Merge Sort** - splits array in half until pieces are tiny, then puts them back together sorted
2. **Quick Sort** - picks a number in the middle, puts smaller stuff left and bigger stuff right
3. **Heap Sort** - makes a special tree structure called a heap, then takes out the biggest number over and over
4. **Selection Sort** - finds the smallest number and puts it first, then finds next smallest, etc.

## The Code

Program creates 8 random numbers and sorts them 4 different ways.


## Speed

- Merge, Quick, Heap: O(n log n) - pretty fast
- Selection: O(n²) - slower

Selection sort is easiest to understand but slowest for big lists.

## How to Run
```
python sorting_algorithms.py
```

## My Thoughts

Merge sort was easier than I thought. Heap sort took me a while to understand the parent/child thing with the indices (2*i+1 and 2*i+2).

The heapify function was confusing at first but makes sense now.

All of them work and give the same answer which is good!
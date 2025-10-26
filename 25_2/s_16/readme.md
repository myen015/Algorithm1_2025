# Sorting Algorithms

I made 4 sorting algorithms:
- Merge Sort
- Quick Sort  
- Insertion Sort
- Heap Sort

## How to run it
```bash
python sorting_algorithms.py
```

## The Algorithms

### Merge Sort
Splits array in half, sorts each half, then merges them back.  
Time: O(n log n) - always

### Quick Sort  
Pick a middle element, put smaller stuff on left, bigger stuff on right, repeat.  
Time: O(n log n) usually, sometimes O(n²)

### Insertion Sort
Go through array, put each element in the right spot.  
Time: O(n²) - slow but easy to understand

### Heap Sort
Make a heap, take out the biggest element repeatedly.  
Time: O(n log n) - this one was hard to understand

## Testing

I tested with this array: `[64, 34, 25, 12, 22, 11, 90]`

All algorithms work and give: `[11, 12, 22, 25, 34, 64, 90]`

## My thoughts

- Merge sort was easier than I expected
- Quick sort is pretty clever with the pivot thing
- Insertion sort is really simple
- Heap sort... I had to read the notes like 3 times to get it

The hardest part was the heapify function in heap sort. I drew it on paper to understand the parent/child thing.
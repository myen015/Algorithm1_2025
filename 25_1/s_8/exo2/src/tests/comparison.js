const { badSort } = require("../sorts/bad_sort.js");
const { quickSort } = require("../sorts/quick_sort.js");
const { mergeSort } = require("../sorts/merge_sort.js");
const { heapSort } = require("../sorts/heap_sort.js");

function comparison(size = 100) {
  const generateRandomArray = (n) =>
    Array.from({ length: n }, () => Math.floor(Math.random() * 1000));

  const arr1 = generateRandomArray(size);
  const start1 = performance.now();
  mergeSort(arr1, 0, arr1.length - 1);
  const end1 = performance.now();
  console.log(`Merge Sort: ${(end1 - start1).toFixed(4)} ms`);

  const arr2 = generateRandomArray(size);
  const start2 = performance.now();
  quickSort(arr2, 0, arr2.length - 1);
  const end2 = performance.now();
  console.log(`Quick Sort: ${(end2 - start2).toFixed(4)} ms`);

  const arr3 = generateRandomArray(size);
  const start3 = performance.now();
  heapSort(arr3);
  const end3 = performance.now();
  console.log(`Heap Sort: ${(end3 - start3).toFixed(4)} ms`);

  const arr4 = generateRandomArray(size);
  const start4 = performance.now();
  badSort(arr4, 0, arr4.length - 1);
  const end4 = performance.now();
  console.log(`Bad Sort: ${(end4 - start4).toFixed(4)} ms`);
}

comparison();

// results: Merge sort is somehow the best for 100 elements.

// Bubble sort is the worst and almost 5 times slower than others.
// Quick sort is almost the same as heap sort.

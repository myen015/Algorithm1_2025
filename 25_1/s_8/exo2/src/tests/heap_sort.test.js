const { heapSort } = require("../sorts/heap_sort.js");

describe("heapSort - basic sorting", () => {
  it("should sort the array", () => {
    const arr = [3, 2, 1];
    heapSort(arr);
    expect(arr).toEqual([1, 2, 3]);
  });
});

describe("heapSort - same elements", () => {
  it("should sort the array with all the same elements", () => {
    const arr = [1, 1, 1];
    heapSort(arr);
    expect(arr).toEqual([1, 1, 1]);
  });
});

describe("heapSort - large numbers", () => {
  it("should sort the array with large numbers", () => {
    const arr = [1000, 100000000, 10000];
    heapSort(arr);
    expect(arr).toEqual([1000, 10000, 100000000]);
  });
});

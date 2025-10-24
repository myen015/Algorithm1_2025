const { quickSort } = require("../sorts/quick_sort.js");

describe("quickSort - basic sorting", () => {
  it("should sort the array", () => {
    const arr = [3, 2, 1];
    quickSort(arr, 0, arr.length - 1);
    expect(arr).toEqual([1, 2, 3]);
  });
});

describe("quickSort - same elements", () => {
  it("should sort the array with all the same elements", () => {
    const arr = [1, 1, 1];
    quickSort(arr, 0, arr.length - 1);
    expect(arr).toEqual([1, 1, 1]);
  });
});

describe("quickSort - large numbers", () => {
  it("should sort the array with large numbers", () => {
    const arr = [1000, 100000000, 10000];
    quickSort(arr, 0, arr.length - 1);
    expect(arr).toEqual([1000, 10000, 100000000]);
  });
});

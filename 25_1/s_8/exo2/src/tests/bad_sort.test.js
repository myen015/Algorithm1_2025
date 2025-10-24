const badSort = require("../sorts/bad_sort.js");

describe("badSort - basic sorting", () => {
  it("should sort the array", () => {
    const arr = [3, 2, 1];
    badSort(arr);
    expect(arr).toEqual([1, 2, 3]);
  });
});

describe("badSort - same elements", () => {
  it("should sort the array with all the same elements", () => {
    const arr = [1, 1, 1];
    badSort(arr);
    expect(arr).toEqual([1, 1, 1]);
  });
});

describe("badSort - large numbers", () => {
  it("should sort the array with large numbers", () => {
    const arr = [1000, 100000000, 10000];
    badSort(arr);
    expect(arr).toEqual([1000, 10000, 100000000]);
  });
});

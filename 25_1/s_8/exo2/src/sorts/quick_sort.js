function quickSort(arr, low, high) {
  if (low < high) {
    const pivot = partition_random(arr, low, high);
    quickSort(arr, low, pivot - 1);
    quickSort(arr, pivot + 1, high);
  }
  return arr;
}

function partition(arr, low, high) {
  const pivot = arr[high];
  let i = low - 1;
  for (let j = low; j < high; j++) {
    if (arr[j] <= pivot) {
      i++;
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
  }
  [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
  return i + 1;
}

function partition_random(arr, low, high) {
  const random = Math.floor(Math.random() * (high - low + 1)) + low;
  [arr[random], arr[high]] = [arr[high], arr[random]];
  return partition(arr, low, high);
}

module.exports = { quickSort };

// With help of https://www.geeksforgeeks.org/dsa/quicksort-using-random-pivoting/

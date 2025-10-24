// O(n²) Sorting Algorithm - Bubble Sort
function bubbleSort(arr) {
    const n = arr.length;
    const result = [...arr]; // Create copy to avoid mutating original
    
    for (let i = 0; i < n - 1; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            if (result[j] > result[j + 1]) {
                // Swap elements
                [result[j], result[j + 1]] = [result[j + 1], result[j]];
            }
        }
    }
    return result;
}

// Quick Sort with Random Pivot
function quickSortRandom(arr) {
    if (arr.length <= 1) return [...arr];
    
    const result = [...arr];
    quickSortRandomHelper(result, 0, result.length - 1);
    return result;
}

function quickSortRandomHelper(arr, low, high) {
    if (low < high) {
        // Random pivot selection
        const randomIndex = Math.floor(Math.random() * (high - low + 1)) + low;
        [arr[randomIndex], arr[high]] = [arr[high], arr[randomIndex]];
        
        const pivotIndex = partitionRandom(arr, low, high);
        quickSortRandomHelper(arr, low, pivotIndex - 1);
        quickSortRandomHelper(arr, pivotIndex + 1, high);
    }
}

function partitionRandom(arr, low, high) {
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

// Quick Sort with Average Pivot (Median-of-Three)
function quickSortAverage(arr) {
    if (arr.length <= 1) return [...arr];
    
    const result = [...arr];
    quickSortAverageHelper(result, 0, result.length - 1);
    return result;
}

function quickSortAverageHelper(arr, low, high) {
    if (low < high) {
        // Median-of-three pivot selection
        const mid = Math.floor((low + high) / 2);
        medianOfThree(arr, low, mid, high);
        
        const pivotIndex = partitionAverage(arr, low, high);
        quickSortAverageHelper(arr, low, pivotIndex - 1);
        quickSortAverageHelper(arr, pivotIndex + 1, high);
    }
}

function medianOfThree(arr, low, mid, high) {
    if (arr[mid] < arr[low]) [arr[low], arr[mid]] = [arr[mid], arr[low]];
    if (arr[high] < arr[low]) [arr[low], arr[high]] = [arr[high], arr[low]];
    if (arr[high] < arr[mid]) [arr[mid], arr[high]] = [arr[high], arr[mid]];
    
    // Place median at the end as pivot
    [arr[mid], arr[high]] = [arr[high], arr[mid]];
}

function partitionAverage(arr, low, high) {
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

// Merge Sort
function mergeSort(arr) {
    if (arr.length <= 1) return [...arr];
    
    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid));
    const right = mergeSort(arr.slice(mid));
    
    return merge(left, right);
}

function merge(left, right) {
    const result = [];
    let leftIndex = 0;
    let rightIndex = 0;
    
    while (leftIndex < left.length && rightIndex < right.length) {
        if (left[leftIndex] <= right[rightIndex]) {
            result.push(left[leftIndex]);
            leftIndex++;
        } else {
            result.push(right[rightIndex]);
            rightIndex++;
        }
    }
    
    // Add remaining elements
    while (leftIndex < left.length) {
        result.push(left[leftIndex]);
        leftIndex++;
    }
    
    while (rightIndex < right.length) {
        result.push(right[rightIndex]);
        rightIndex++;
    }
    
    return result;
}

// Heap Sort
function heapSort(arr) {
    const result = [...arr];
    const n = result.length;
    
    // Build max heap
    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
        heapify(result, n, i);
    }
    
    // Extract elements from heap one by one
    for (let i = n - 1; i > 0; i--) {
        [result[0], result[i]] = [result[i], result[0]];
        heapify(result, i, 0);
    }
    
    return result;
}

function heapify(arr, n, i) {
    let largest = i;
    const left = 2 * i + 1;
    const right = 2 * i + 2;
    
    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }
    
    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }
    
    if (largest !== i) {
        [arr[i], arr[largest]] = [arr[largest], arr[i]];
        heapify(arr, n, largest);
    }
}

//Testing Functions
function generateRandomArray(size, max = 1000) {
    return Array.from({ length: size }, () => Math.floor(Math.random() * max));
}

function isSorted(arr) {
    for (let i = 1; i < arr.length; i++) {
        if (arr[i] < arr[i - 1]) return false;
    }
    return true;
}

function testSortingAlgorithm(sortFunction, name, testArray) {
    console.log(`\nTesting ${name}:`);
    console.log(`Original: [${testArray.join(', ')}]`);
    
    const startTime = performance.now();
    const sorted = sortFunction(testArray);
    const endTime = performance.now();
    
    console.log(`Sorted:   [${sorted.join(', ')}]`);
    console.log(`Correct:  ${isSorted(sorted)}`);
    console.log(`Time:     ${(endTime - startTime).toFixed(4)} ms`);
    
    return isSorted(sorted);
}

function runComprehensiveTests() {
    console.log("=== Sorting Algorithms Test Suite ===\n");
    
    const algorithms = [
        { func: bubbleSort, name: "Bubble Sort (O(n²))" },
        { func: quickSortRandom, name: "Quick Sort (Random Pivot)" },
        { func: quickSortAverage, name: "Quick Sort (Median-of-Three)" },
        { func: mergeSort, name: "Merge Sort (O(n log n))" },
        { func: heapSort, name: "Heap Sort (O(n log n))" }
    ];
    
    // Test with different array sizes and types
    const testCases = [
        { name: "Small Random", array: generateRandomArray(10, 50) },
        { name: "Medium Random", array: generateRandomArray(20, 100) },
        { name: "Already Sorted", array: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] },
        { name: "Reverse Sorted", array: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1] },
        { name: "Duplicates", array: [5, 2, 8, 2, 9, 1, 5, 5, 2, 8] },
        { name: "Single Element", array: [42] },
        { name: "Empty Array", array: [] }
    ];
    
    let totalTests = 0;
    let passedTests = 0;
    
    testCases.forEach(testCase => {
        console.log(`\n${"=".repeat(50)}`);
        console.log(`TEST CASE: ${testCase.name}`);
        console.log(`${"=".repeat(50)}`);
        
        algorithms.forEach(algorithm => {
            const passed = testSortingAlgorithm(algorithm.func, algorithm.name, testCase.array);
            totalTests++;
            if (passed) passedTests++;
        });
    });
    
    console.log(`\n${"=".repeat(50)}`);
    console.log(`SUMMARY: ${passedTests}/${totalTests} tests passed`);
    console.log(`${"=".repeat(50)}`);
}

// Performance comparison for larger datasets
function performanceComparison() {
    console.log("\n=== Performance Comparison (Larger Datasets) ===\n");
    
    const sizes = [100, 500, 1000];
    const algorithms = [
        { func: bubbleSort, name: "Bubble Sort" },
        { func: quickSortRandom, name: "Quick Sort (Random)" },
        { func: quickSortAverage, name: "Quick Sort (Median-3)" },
        { func: mergeSort, name: "Merge Sort" },
        { func: heapSort, name: "Heap Sort" }
    ];
    
    sizes.forEach(size => {
        console.log(`\nArray Size: ${size} elements`);
        console.log("-".repeat(40));
        
        const testArray = generateRandomArray(size);
        
        algorithms.forEach(algorithm => {
            const startTime = performance.now();
            const sorted = algorithm.func(testArray);
            const endTime = performance.now();
            
            const time = (endTime - startTime).toFixed(4);
            const correct = isSorted(sorted) ? "✓" : "✗";
            
            console.log(`${algorithm.name.padEnd(25)} ${time.padStart(8)} ms ${correct}`);
        });
    });
}

runComprehensiveTests();
performanceComparison();

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        bubbleSort,
        quickSortRandom,
        quickSortAverage,
        mergeSort,
        heapSort,
        testSortingAlgorithm,
        generateRandomArray,
        isSorted
    };
}
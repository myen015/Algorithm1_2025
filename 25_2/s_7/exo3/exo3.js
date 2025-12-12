// PROBLEM 1: FIBONACCI 
function multiplyMatrix(A, B) {
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]
    ];
}

function matrixPower(matrix, n) {
    if (n === 1) return matrix;
    
    if (n % 2 === 0) {
        const half = matrixPower(matrix, n / 2);
        return multiplyMatrix(half, half);
    } else {
        return multiplyMatrix(matrix, matrixPower(matrix, n - 1));
    }
}

function fibonacciMatrixMethod(n) {
    if (n === 0) return 0;
    if (n === 1) return 1;
    
    const baseMatrix = [[1, 1], [1, 0]];
    const resultMatrix = matrixPower(baseMatrix, n);
    
    return resultMatrix[0][1];
}

function fibonacciSymmetricMatrix(n) {
    if (n === 0) return 0;
    if (n === 1) return 1;
    
    const symmetricMatrix = [[2, 1], [1, 1]];
    const power = Math.floor(n / 2);
    const resultMatrix = matrixPower(symmetricMatrix, power);
    
    // Multiply by [1, 0] vector
    return resultMatrix[0][0];
}


// Test Fibonacci
console.log("\n=== PROBLEM 1: FIBONACCI ===");
console.log("\nTesting Fibonacci computation:");
for (let i = 0; i <= 15; i++) {
    console.log(`F(${i}) = ${fibonacciMatrixMethod(i)}`);
}


// PROBLEM 2: 0/1 KNAPSACK ALGORITHM
function knapsack01(weights, values, capacity) {
    const n = weights.length;
    const dp = Array(n + 1).fill(null).map(() => Array(capacity + 1).fill(0));
    
    for (let i = 1; i <= n; i++) {
        for (let w = 0; w <= capacity; w++) {
            if (weights[i - 1] <= w) {
                dp[i][w] = Math.max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                );
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }
    
    return { maxValue: dp[n][capacity], dp: dp };
}

function knapsackSpaceOptimized(weights, values, capacity) {
    const n = weights.length;
    const dp = Array(capacity + 1).fill(0);
    
    for (let i = 0; i < n; i++) {
        for (let w = capacity; w >= weights[i]; w--) {
            dp[w] = Math.max(dp[w], values[i] + dp[w - weights[i]]);
        }
    }
    
    return dp[capacity];
}


console.log("\n=== PROBLEM 2: 0/1 KNAPSACK ALGORITHM ===");
const weights = [2, 3, 4, 5];
const values = [3, 4, 5, 6];
const capacity = 8;

console.log("\nCourse Example:");
console.log("Weights:", weights);
console.log("Values:", values);
console.log("Capacity:", capacity);

const result = knapsack01(weights, values, capacity);
console.log("\nMaximum value:", result.maxValue);

const resultOptimized = knapsackSpaceOptimized(weights, values, capacity);
console.log("Maximum value (space-optimized):", resultOptimized);



// PROBLEM 3: NEURO COMPUTING
function generateRandomBinaryVectors(count, length) {
    const vectors = [];
    for (let i = 0; i < count; i++) {
        const vector = Array(length).fill(0).map(() => Math.random() > 0.5 ? 1 : 0);
        vectors.push(vector);
    }
    return vectors;
}

function cosineSimilarity(x, y) {
    const dotProduct = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
    const normX = Math.sqrt(x.reduce((sum, xi) => sum + xi * xi, 0));
    const normY = Math.sqrt(y.reduce((sum, yi) => sum + yi * yi, 0));
    
    if (normX === 0 || normY === 0) return 0;
    return dotProduct / (normX * normY);
}

function jaccardSimilarity(x, y) {
    let intersection = 0;
    let union = 0;
    
    for (let i = 0; i < x.length; i++) {
        if (x[i] === 1 && y[i] === 1) intersection++;
        if (x[i] === 1 || y[i] === 1) union++;
    }
    
    return union === 0 ? 0 : intersection / union;
}

function computeSimilarities(vectors, similarityFunc) {
    const similarities = [];
    
    for (let i = 0; i < vectors.length; i++) {
        for (let j = i + 1; j < vectors.length; j++) {
            similarities.push(similarityFunc(vectors[i], vectors[j]));
        }
    }
    
    return similarities;
}

function analyzeSimilarities(similarities, name) {
    const mean = similarities.reduce((a, b) => a + b, 0) / similarities.length;
    const variance = similarities.reduce((sum, x) => sum + (x - mean) ** 2, 0) / similarities.length;
    const stdDev = Math.sqrt(variance);
    
    console.log(`\n${name} Statistics:`);
    console.log(`  Mean: ${mean.toFixed(4)}`);
    console.log(`  Std Dev: ${stdDev.toFixed(4)}`);
    console.log(`  Min: ${Math.min(...similarities).toFixed(4)}`);
    console.log(`  Max: ${Math.max(...similarities).toFixed(4)}`);
    
    return { mean, stdDev, min: Math.min(...similarities), max: Math.max(...similarities) };
}

function countSparseBinaryVectors(N, w) {
    function factorial(n) {
        if (n <= 1) return 1;
        let result = 1;
        for (let i = 2; i <= n; i++) result *= i;
        return result;
    }
    
    function binomialCoefficient(n, k) {
        if (k > n) return 0;
        if (k === 0 || k === n) return 1;
        
        let result = 1;
        for (let i = 0; i < k; i++) {
            result *= (n - i);
            result /= (i + 1);
        }
        return result;
    }
    
    return binomialCoefficient(N, w);
}

function neuroComputingExperiment() {
    console.log("\n=== PROBLEM 3: NEURO COMPUTING ===");
    
    console.log("\n1. Generating 100 random binary vectors of length N=100");
    const vectors = generateRandomBinaryVectors(100, 100);
    console.log(`   Generated ${vectors.length} vectors`);
    console.log(`   Sample vector: [${vectors[0].slice(0, 10).join(', ')}...]`);
    
    console.log("\n2. Computing similarity functions:");
    const cosineSims = computeSimilarities(vectors, cosineSimilarity);
    const jaccardSims = computeSimilarities(vectors, jaccardSimilarity);
    
    analyzeSimilarities(cosineSims, "Cosine Similarity");
    analyzeSimilarities(jaccardSims, "Jaccard Similarity");
    
    
    console.log("\n3. Repeating for larger N values:");
    for (const N of [500, 1000, 2000]) {
        const largeVectors = generateRandomBinaryVectors(50, N);
        const largeSims = computeSimilarities(largeVectors, cosineSimilarity);
        const stats = analyzeSimilarities(largeSims, `  N=${N}`);
        console.log(`     Range: ${(stats.max - stats.min).toFixed(4)}`);
    }
    
    console.log("\n4. Sparse binary vectors (N=2000, w=5 ones):");
    const possibleVectors = countSparseBinaryVectors(2000, 5);
    console.log(`   Number of possible vectors: ${possibleVectors.toExponential(2)}`);
    console.log(`   This is C(2000,5) = 2000!/(5!*1995!)`);
    
    console.log("\n5. Capacity of sparse binary vectors:");
    console.log("   Capacity = log₂(number of possible vectors)");
    console.log(`   Capacity ≈ ${Math.log2(possibleVectors).toFixed(2)} bits`);

}

neuroComputingExperiment();


function generateBinaryVector(n) {
  return Array.from({ length: n }, () => (Math.random() < 0.5 ? 0 : 1));
}

function dotProduct(x, y) {
  return x.reduce((sum, val, i) => sum + val * y[i], 0);
}

function l1Norm(x) {
  return x.reduce((sum, val) => sum + val, 0);
}

function similarity(x, y) {
  const dot = dotProduct(x, y);
  const normX = l1Norm(x);
  const normY = l1Norm(y);
  return normX === 0 || normY === 0 ? 0 : dot / (normX * normY);
}

function jaccardSimilarity(x, y) {
  const intersection = x.reduce((sum, val, i) => sum + Math.min(val, y[i]), 0);
  const union = x.reduce((sum, val, i) => sum + Math.max(val, y[i]), 0);
  return union === 0 ? 0 : intersection / union;
}

function computeSimilarities(n, count = 100) {
  const simArray = [];
  const jaccArray = [];

  const vectors = Array.from({ length: count }, () => generateBinaryVector(n));

  for (let i = 0; i < count; i++) {
    for (let j = i + 1; j < count; j++) {
      simArray.push(similarity(vectors[i], vectors[j]));
      jaccArray.push(jaccardSimilarity(vectors[i], vectors[j]));
    }
  }

  return { sim: simArray, jacc: jaccArray };
}

function countSparseVectors(n, w) {
  let result = 1;
  for (let i = 0; i < w; i++) {
    result *= n - i;
    result /= i + 1;
  }
  return Math.floor(result);
}

function getMean(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function getStdDev(arr) {
  const mean = getMean(arr);
  const variance =
    arr.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / arr.length;
  return Math.sqrt(variance);
}

const n = 10;
const { sim, jacc } = computeSimilarities(n, 100);

console.log("=== N = " + n + " ===");
console.log("Similarity mean:", getMean(sim).toFixed(4));
console.log("Similarity stddev:", getStdDev(sim).toFixed(4));
console.log("Jaccard mean:", getMean(jacc).toFixed(4));
console.log("Jaccard stddev:", getStdDev(jacc).toFixed(4));

console.log("\n=== N = 50 ===");
const { sim: sim50, jacc: jacc50 } = computeSimilarities(50, 100);
console.log("Similarity mean:", getMean(sim50).toFixed(4));
console.log("Similarity stddev:", getStdDev(sim50).toFixed(4));

console.log("\n=== Sparse vectors: N=2000, w=5 ===");
const possibleCount = countSparseVectors(2000, 5);
console.log("Possible vectors:", possibleCount);

console.log("\n=== Capacity (Hamming distance) ===");
const testVec1 = generateBinaryVector(2000);
const testVec2 = generateBinaryVector(2000);
const hammingDist = testVec1.reduce(
  (sum, val, i) => sum + (val !== testVec2[i] ? 1 : 0),
  0
);
console.log("Hamming distance example:", hammingDist);
console.log("Normalized capacity:", (hammingDist / 2000).toFixed(4));

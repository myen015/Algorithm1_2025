// ============================================
// PROBLEM 1: P, NP, NP-complete, NP-hard (4/10 pts)
// ============================================

// Quick refresher on complexity classes:
// P = problems solvable in polynomial time (easy shit)
// NP = problems where you can verify a solution quickly (even if finding it is hard)
// NP-complete = hardest problems in NP (if you solve one, you solve them all)
// NP-hard = at least as hard as NP-complete (might not even be in NP)

const complexityClasses = {
  // Line 1: find max, linear search, shortest path in unweighted graph, matrix multiplication
  // All these are solvable in polynomial time, so they're in P
  line1: {
    problems: [
      "find max",
      "linear search",
      "shortest path (unweighted)",
      "matrix multiplication",
    ],
    class: "P",
    explanation:
      "All these can be solved in polynomial time. Find max is O(n), linear search is O(n), shortest path unweighted is O(V+E) with BFS, matrix mult is O(n^3). Easy stuff.",
  },

  // Line 2: sorting, Dijkstra, BFS, DFS, merge sort, quicksort
  // Again all polynomial time algorithms
  line2: {
    problems: [
      "sorting",
      "Dijkstra (non-negative)",
      "BFS",
      "DFS",
      "merge sort",
      "quicksort",
    ],
    class: "P",
    explanation:
      "These are also polynomial. Sorting is O(n log n), Dijkstra is O((V+E) log V), BFS/DFS are O(V+E). All doable in polynomial time.",
  },

  // Line 3: sudoku
  // Sudoku is NP-complete - you can verify a solution quickly but finding it is hard
  line3: {
    problems: ["sudoku"],
    class: "NP-complete",
    explanation:
      "Sudoku is NP-complete. Given a filled sudoku, you can check if its valid quickly (polynomial). But finding a solution? That shit is hard. Its actually equivalent to graph coloring.",
  },

  // Line 4: 3-coloring, scheduling with conflicts
  // Both are classic NP-complete problems
  line4: {
    problems: ["3-coloring of graph", "scheduling with conflicts"],
    class: "NP-complete",
    explanation:
      "3-coloring means coloring graph nodes with 3 colors so no adjacent nodes have same color. Scheduling with conflicts is similar - assign tasks avoiding conflicts. Both are NP-complete. Easy to verify a solution, hard to find one.",
  },

  // Line 5: TSP, Hamiltonian Cycle, Clique
  // The holy trinity of NP-complete problems
  line5: {
    problems: ["TSP", "Hamiltonian Cycle", "Clique"],
    class: "NP-complete",
    explanation:
      "These are the famous NP-complete problems. TSP = find shortest tour visiting all cities. Hamiltonian Cycle = find cycle visiting each vertex once. Clique = find complete subgraph of size k. All NP-complete classics.",
  },

  // Line 6: Cryptography, factoring large integers
  // This is tricky - factoring is in NP but not known to be NP-complete (probably NP-intermediate)
  line6: {
    problems: ["cryptography", "factoring large integers"],
    class: "NP (possibly NP-intermediate)",
    explanation:
      "Factoring is definitely in NP - you can verify factors quickly. But its not proven to be NP-complete. Most people think its NP-intermediate (harder than P, easier than NP-complete). Thats why RSA works!",
  },

  // Line 7: Halting Problem, busy beaver
  // These are undecidable - not even in NP-hard, theyre impossible to solve in general
  line7: {
    problems: ["Halting Problem", "busy beaver"],
    class: "Undecidable (not even in NP)",
    explanation:
      "These are undecidable problems. No algorithm can solve them for all inputs, not even in infinite time. Halting Problem = determine if program stops or runs forever. Busy Beaver = find longest-running program of size n. These are beyond NP-hard.",
  },
};

// Print the classification
for (let line in complexityClasses) {
  console.log(`\n${line}:`);
  console.log(`Problems: ${complexityClasses[line].problems.join(", ")}`);
  console.log(`Class: ${complexityClasses[line].class}`);
  console.log(`Explanation: ${complexityClasses[line].explanation}`);
}

// ============================================
// PROBLEM 2: Bayes Theorem (3/10 pts)
// ============================================

// The setup: Disease affects 0.1% of people, test is 99% accurate
// Patient tests positive. Whats the probability they actually have the disease?
// Answer is 9%! Seems crazy right? Lets see why.

function bayesTheorem() {
  // Given data
  const diseaseRate = 0.001; // 0.1% of people have disease
  const testAccuracy = 0.99; // 99% accurate (both sensitivity and specificity)

  // Lets say we test 10,000 people
  const population = 10000;

  // How many actually have the disease?
  const actualSick = population * diseaseRate; // 10,000 * 0.001 = 10 people

  // How many are healthy?
  const actualHealthy = population - actualSick; // 9,990 people

  // Of the 10 sick people, how many test positive? (99% accuracy = 99% sensitivity)
  const truePosives = actualSick * testAccuracy; // 10 * 0.99 = 9.9 ≈ 10 people

  // Of the 9,990 healthy people, how many FALSE positives? (99% specificity means 1% false positive rate)
  const falsePositives = actualHealthy * (1 - testAccuracy); // 9,990 * 0.01 = 99.9 ≈ 100 people

  // Total people who test positive
  const totalPositives = truePosives + falsePositives; // 10 + 100 = 110 people

  // Of those who test positive, how many actually have disease?
  const probability = truePosives / totalPositives; // 10 / 110 ≈ 0.09 = 9%

  console.log("\n\n=== BAYES THEOREM EXAMPLE ===");
  console.log(`Population: ${population} people`);
  console.log(`Disease rate: ${diseaseRate * 100}%`);
  console.log(`Test accuracy: ${testAccuracy * 100}%`);
  console.log("");
  console.log(`Actually sick: ${actualSick} people`);
  console.log(`Actually healthy: ${actualHealthy} people`);
  console.log("");
  console.log(`True positives (sick AND test positive): ${truePosives}`);
  console.log(`False positives (healthy BUT test positive): ${falsePositives}`);
  console.log(`Total who test positive: ${totalPositives}`);
  console.log("");
  console.log(
    `Probability patient has disease given positive test: ${(
      probability * 100
    ).toFixed(1)}%`
  );
  console.log("");
  console.log("WHY SO LOW?");
  console.log(
    "Because the disease is so rare (0.1%), even with 99% accurate test,"
  );
  console.log(
    "you get way more false positives from the huge healthy population"
  );
  console.log("than true positives from the tiny sick population.");
  console.log("100 false positives vs 10 true positives = only 9% chance!");

  return probability;
}

bayesTheorem();

// ============================================
// PROBLEM 3: Shannon Entropy (3/10 pts)
// ============================================

// Shannon Entropy measures how much "surprise" or "information" is in a random variable
// Formula: H(X) = -Σ p_i * log2(p_i)
// Basically it tells you how many bits you need on average to describe the outcome

function shannonEntropy(probHeads) {
  const probTails = 1 - probHeads;

  // Handle edge cases where log(0) would be undefined
  let entropy = 0;
  if (probHeads > 0 && probHeads < 1) {
    entropy = -(
      probHeads * Math.log2(probHeads) +
      probTails * Math.log2(probTails)
    );
  }

  return entropy;
}

console.log("\n\n=== SHANNON ENTROPY ===");

// Coin A: 50% heads (fair coin)
const coinA_entropy = shannonEntropy(0.5);
console.log("\nCoin A (50% heads):");
console.log(`Entropy: ${coinA_entropy.toFixed(4)} bits`);
console.log(
  "This is a fair coin. Maximum uncertainty. You need 1 full bit to describe the outcome."
);
console.log(
  "Makes sense - heads or tails, thats exactly 2 possibilities = 1 bit."
);

// Coin B: 99% heads (heavily biased)
const coinB_entropy = shannonEntropy(0.99);
console.log("\nCoin B (99% heads):");
console.log(`Entropy: ${coinB_entropy.toFixed(4)} bits`);
console.log("This coin almost always shows heads. Very little surprise.");
console.log(
  "You barely need any bits to describe it - its predictable as fuck."
);
console.log("Only 0.08 bits because 99% of the time you know what youll get.");

// Coin C: 1% heads (opposite bias)
const coinC_entropy = shannonEntropy(0.01);
console.log("\nCoin C (1% heads):");
console.log(`Entropy: ${coinC_entropy.toFixed(4)} bits`);
console.log("This coin almost never shows heads. Also very predictable.");
console.log(
  "Same low entropy as coin B - lack of uncertainty means few bits needed."
);

console.log("\n=== WHY DOES THIS MAKE SENSE? ===");
console.log("Fair coin (50/50): Maximum uncertainty = 1 bit needed");
console.log(
  "  - You genuinely dont know what youll get, need full bit to encode"
);
console.log("");
console.log("Biased coin (99/1): Almost no uncertainty = 0.08 bits needed");
console.log(
  "  - You almost always know what youll get, barely need to encode anything"
);
console.log(
  '  - If I told you "the coin landed normally" youd know it was heads 99% of time'
);
console.log(
  "  - Only when rare event happens do you need to actually communicate info"
);
console.log("");
console.log(
  "The more predictable something is, the less information it contains,"
);
console.log("and the fewer bits you need to describe it on average.");

// Lets visualize entropy across different probabilities
console.log("\n=== ENTROPY FOR DIFFERENT PROBABILITIES ===");
for (let p = 0; p <= 1; p += 0.1) {
  const h = shannonEntropy(p);
  console.log(`P(heads) = ${p.toFixed(1)}: H = ${h.toFixed(4)} bits`);
}
console.log(
  "\nNotice how entropy peaks at 0.5 (fair coin) and drops towards 0 at extremes!"
);

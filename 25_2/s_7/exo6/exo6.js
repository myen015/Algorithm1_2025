// 1. General class for the tree object
class TreeNode {
    constructor(weight, n) {
        this.weight = weight;
        this.n = n;
        this.children = [];
    }

    addChild(child) {
        this.children.push(child);
    }
}

// 2. Generate a tree of depth N with initial parent weight calculated to ensure sum = 1
// For a tree of depth D, each level contributes the same sum as the root
// Total sum = D * root_weight, so root_weight = 1/D
function generateTree(depth, n, rootWeight = null) {
    if (depth === 0) {
        return null;
    }

    const currentWeight = rootWeight !== null ? rootWeight : 1 / depth;
    const node = new TreeNode(currentWeight, n);

    for (let i = 0; i < n; i++) {
        const childWeight = currentWeight / n;
        const child = generateTree(depth - 1, n, childWeight);
        if (child) {
            node.addChild(child);
        }
    }

    return node;
}

// 3. Depth-first recursive function summing weights
function depthFirstSum(node) {
    if (!node) {
        return 0;
    }

    let sum = node.weight;

    for (const child of node.children) {
        sum += depthFirstSum(child);
    }

    return sum;
}

// 4. Breadth-first sum
function breadthFirstSum(root) {
    if (!root) {
        return 0;
    }

    let sum = 0;
    const queue = [root];

    while (queue.length > 0) {
        const node = queue.shift();
        sum += node.weight;

        for (const child of node.children) {
            queue.push(child);
        }
    }

    return sum;
}

// 5. Depth-first with sign flipping
function depthFirstSumFlip(node, flipSign = false) {
    if (!node) {
        return 0;
    }

    if (flipSign) {
        node.weight = -node.weight;
    }

    let sum = node.weight;

    for (const child of node.children) {
        sum += depthFirstSumFlip(child, flipSign);
    }

    return sum;
}

// 5. Breadth-first with sign flipping
function breadthFirstSumFlip(root, flipSign = false) {
    if (!root) {
        return 0;
    }

    let sum = 0;
    const queue = [root];

    while (queue.length > 0) {
        const node = queue.shift();

        if (flipSign) {
            node.weight = -node.weight;
        }
        
        sum += node.weight;

        for (const child of node.children) {
            queue.push(child);
        }
    }

    return sum;
}

// 6. Breadth-first: Non-recursive version (already implemented above)
// This is the standard and recommended implementation

// 6. Breadth-first: Recursive version (NOT RECOMMENDED)
function breadthFirstSumRecursive(nodes) {
    if (!nodes || nodes.length === 0) {
        return 0;
    }

    let sum = 0;
    const nextLevel = [];

    for (const node of nodes) {
        sum += node.weight;
        for (const child of node.children) {
            nextLevel.push(child);
        }
    }

    return sum + breadthFirstSumRecursive(nextLevel);
}

function breadthFirstSumRecursiveWrapper(root) {
    if (!root) {
        return 0;
    }
    return breadthFirstSumRecursive([root]);
}

function runTests() {
    console.log("=".repeat(60));
    console.log("FACEBOOK INTERVIEW PROBLEM - WEIGHTED TREES");
    console.log("=".repeat(60));

    const testValues = [2, 3, 4, 5];

    testValues.forEach(n => {
        console.log(`\n${"=".repeat(60)}`);
        console.log(`Testing with n = ${n}`);
        console.log("=".repeat(60));

        const tree = generateTree(3, n);

        const dfsSum = depthFirstSum(tree);
        console.log(`\nDepth-First Sum: ${dfsSum.toFixed(10)}`);
        console.log(`Expected: 1.0000000000`);
        console.log(`Match: ${Math.abs(dfsSum - 1.0) < 1e-10 ? "✓ PASS" : "✗ FAIL"}`);

        const bfsSum = breadthFirstSum(tree);
        console.log(`\nBreadth-First Sum: ${bfsSum.toFixed(10)}`);
        console.log(`Expected: 1.0000000000`);
        console.log(`Match: ${Math.abs(bfsSum - 1.0) < 1e-10 ? "✓ PASS" : "✗ FAIL"}`);

        const bfsRecSum = breadthFirstSumRecursiveWrapper(tree);
        console.log(`\nBreadth-First Sum (Recursive): ${bfsRecSum.toFixed(10)}`);
        console.log(`Match: ${Math.abs(bfsRecSum - 1.0) < 1e-10 ? "✓ PASS" : "✗ FAIL"}`);
    });

    console.log(`\n${"=".repeat(60)}`);
    console.log("TESTING SIGN FLIPPING");
    console.log("=".repeat(60));

    const n = 3;
    const tree = generateTree(3, n);

    const firstSum = depthFirstSumFlip(tree, false);
    console.log(`\nFirst DFS (no flip): ${firstSum.toFixed(10)}`);
    console.log(`Expected: 1.0000000000`);
    console.log(`Match: ${Math.abs(firstSum - 1.0) < 1e-10 ? "✓ PASS" : "✗ FAIL"}`);

    const secondSum = depthFirstSumFlip(tree, true);
    console.log(`\nSecond DFS (with flip): ${secondSum.toFixed(10)}`);
    console.log(`Expected: -1.0000000000`);
    console.log(`Match: ${Math.abs(secondSum - (-1.0)) < 1e-10 ? "✓ PASS" : "✗ FAIL"}`);

    const tree2 = generateTree(3, n);
    const firstBfsSum = breadthFirstSumFlip(tree2, false);
    console.log(`\nFirst BFS (no flip): ${firstBfsSum.toFixed(10)}`);
    console.log(`Match: ${Math.abs(firstBfsSum - 1.0) < 1e-10 ? "✓ PASS" : "✗ FAIL"}`);

    const secondBfsSum = breadthFirstSumFlip(tree2, true);
    console.log(`\nSecond BFS (with flip): ${secondBfsSum.toFixed(10)}`);
    console.log(`Match: ${Math.abs(secondBfsSum - (-1.0)) < 1e-10 ? "✓ PASS" : "✗ FAIL"}`);
}

// 7. Discussion: Why DFS can be recursive but BFS is not recommended
console.log("\n" + "=".repeat(60));
console.log("DISCUSSION: DFS vs BFS Recursion");
console.log("=".repeat(60));

console.log(`
WHY DEPTH-FIRST SEARCH IS NATURALLY RECURSIVE:
-----------------------------------------------
1. CALL STACK MATCHES TREE STRUCTURE
   - DFS explores one path completely before backtracking
   - The function call stack naturally stores the path being explored
   - Each recursive call goes deeper into one branch
   - When a leaf is reached, the function returns and backtracks

2. MEMORY EFFICIENCY
   - Stack depth = tree depth (not node count)
   - For balanced tree: O(log n) stack space
   - Only stores current path, not all nodes

3. NATURAL PROBLEM DECOMPOSITION
   - "Process node, then process each child" maps directly to recursion
   - Base case (leaf node) is obvious
   - Recursive case naturally combines results from children

WHY BREADTH-FIRST SEARCH IS NOT RECOMMENDED FOR RECURSION:
-----------------------------------------------------------
1. AGAINST NATURAL ORDER
   - BFS processes nodes level by level
   - Recursion naturally goes deep, not wide
   - Need to collect ALL nodes at current level before recursing

2. MEMORY INEFFICIENCY
   - Must store entire level in each recursive call
   - Worst case: bottom level has n^depth nodes
   - Stack depth = tree depth, but each frame stores O(n^d) nodes
   - Total: O(depth * n^depth) vs O(n^depth) for iterative

3. AWKWARD IMPLEMENTATION
   - Need to pass array of nodes (not single node)
   - Loses clarity of "process one node at a time"
   - Queue-based iteration is more natural and readable

4. PRACTICAL ISSUES
   - Risk of stack overflow on deep trees
   - Poor cache locality (jumping between stack frames)
   - Harder to debug and maintain

EXAMPLE COMPLEXITY:
For a binary tree of depth 10:
- DFS Recursive: ~10 stack frames (one per level)
- BFS Recursive: ~10 stack frames, but last frame holds 2^10 = 1,024 nodes!
- BFS Iterative: Single frame, processes nodes one at a time

CONCLUSION:
- Use recursive DFS: Natural, efficient, readable
- Use iterative BFS: Natural for queue operations, memory efficient
`);

// Run all tests
runTests();

console.log("\n" + "=".repeat(60));
console.log("All tests completed!");
console.log("=".repeat(60));
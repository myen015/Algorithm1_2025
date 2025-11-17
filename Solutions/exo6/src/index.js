// 1. General class for the tree node
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

// 2. Generate a tree of depth N with initial parent weight 1/n
function generateTree(n, depth, parentWeight = null) {
  if (parentWeight === null) {
    parentWeight = 1 / depth;
  }
  const root = new TreeNode(parentWeight, n);

  if (depth > 1) {
    const childWeight = parentWeight / n;
    for (let i = 0; i < n; i++) {
      const child = generateTree(n, depth - 1, childWeight);
      root.addChild(child);
    }
  }

  return root;
}

// 3. Depth-first recursive function to sum weights (should return 1)
function depthFirstSum(node) {
  if (!node) return 0;

  let sum = node.weight;

  for (const child of node.children) {
    sum += depthFirstSum(child);
  }

  return sum;
}

// 4. Breadth-first iterative function to sum weights (should return 1)
function breadthFirstSum(root) {
  if (!root) return 0;

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

function getTreeDepth(node) {
  if (!node || node.children.length === 0) return 1;
  return 1 + Math.max(...node.children.map((child) => getTreeDepth(child)));
}

// 5. Alternating sign traversals - flip sign each time we reach a node
// Should get 1 after first search (DFS) and -1 after second search (BFS)
function depthFirstAlternatingSum(node, sign = 1) {
  if (!node) return 0;

  let sum = node.weight * sign;

  for (const child of node.children) {
    sum += depthFirstAlternatingSum(child, -sign);
  }

  return sum;
}

function breadthFirstAlternatingSum(root) {
  if (!root) return 0;

  let sum = 0;
  const queue = [{ node: root, sign: -1 }];

  while (queue.length > 0) {
    const { node, sign } = queue.shift();
    sum += node.weight * sign;

    for (const child of node.children) {
      queue.push({ node: child, sign: -sign });
    }
  }

  return sum;
}

// Wrapper functions that normalize alternating sum to get 1 and -1
function depthFirstAlternatingSumNormalized(root) {
  const depth = getTreeDepth(root);
  const rawSum = depthFirstAlternatingSum(root);
  return rawSum * depth;
}

function breadthFirstAlternatingSumNormalized(root) {
  const depth = getTreeDepth(root);
  const rawSum = breadthFirstAlternatingSum(root);
  return rawSum * depth;
}

// 6. Breadth-first: Recursive version
function breadthFirstSumRecursive(queue = []) {
  if (queue.length === 0) return 0;

  const node = queue.shift();
  let sum = node.weight;

  for (const child of node.children) {
    queue.push(child);
  }

  return sum + breadthFirstSumRecursive(queue);
}

function breadthFirstSumRecursiveWrapper(root) {
  if (!root) return 0;
  return breadthFirstSumRecursive([root]);
}

function main() {
  console.log("=== Testing with n=2, depth=3 ===");
  const tree1 = generateTree(2, 3);
  console.log("DFS Sum:", depthFirstSum(tree1)); // Should be ~1
  console.log("BFS Sum:", breadthFirstSum(tree1)); // Should be ~1
  console.log("BFS Recursive Sum:", breadthFirstSumRecursiveWrapper(tree1)); // Should be ~1
  console.log("DFS Alternating:", depthFirstAlternatingSumNormalized(tree1)); // Should be 1
  console.log("BFS Alternating:", breadthFirstAlternatingSumNormalized(tree1)); // Should be -1

  console.log("\n=== Testing with n=3, depth=3 ===");
  const tree2 = generateTree(3, 3);
  console.log("DFS Sum:", depthFirstSum(tree2)); // Should be ~1
  console.log("BFS Sum:", breadthFirstSum(tree2)); // Should be ~1
  console.log("BFS Recursive Sum:", breadthFirstSumRecursiveWrapper(tree2)); // Should be ~1
  console.log("DFS Alternating:", depthFirstAlternatingSumNormalized(tree2)); // Should be 1
  console.log("BFS Alternating:", breadthFirstAlternatingSumNormalized(tree2)); // Should be -1

  console.log("\n=== Testing with n=5, depth=2 ===");
  const tree3 = generateTree(5, 2);
  console.log("DFS Sum:", depthFirstSum(tree3)); // Should be ~1
  console.log("BFS Sum:", breadthFirstSum(tree3)); // Should be ~1
  console.log("DFS Alternating:", depthFirstAlternatingSumNormalized(tree3)); // Should be 1
  console.log("BFS Alternating:", breadthFirstAlternatingSumNormalized(tree3)); // Should be -1
}

main();

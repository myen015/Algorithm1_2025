const graph1 = {
  col_pointers: [0, 2, 5, 8, 11, 12],
  row_indices: [1, 2, 0, 2, 3, 0, 1, 3, 1, 2, 4, 3],
  values: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  directed: false,
};

const graph2 = {
  col_pointers: [0, 0, 2, 4, 5, 7],
  row_indices: [0, 3, 0, 1, 2, 1, 3],
  values: [1, 1, 1, 1, 1, 1, 1],
  directed: true,
};

const vertices = ["A", "B", "C", "D", "E"];
const n = vertices.length;

function decodeCSC(col_pointers, row_indices, values, n) {
  const adjMatrix = Array(n)
    .fill(0)
    .map(() => Array(n).fill(0));

  for (let col = 0; col < n; col++) {
    const start = col_pointers[col];
    const end = col_pointers[col + 1];

    for (let idx = start; idx < end; idx++) {
      const row = row_indices[idx];
      const value = values[idx];
      adjMatrix[row][col] = value;
    }
  }

  return adjMatrix;
}

function printAdjMatrix(adjMatrix, vertices, graphName) {
  console.log(`\n=== ${graphName} - Adjacency Matrix ===`);
  console.log("    " + vertices.join("  "));

  for (let i = 0; i < vertices.length; i++) {
    let row = vertices[i] + "  ";
    for (let j = 0; j < vertices.length; j++) {
      row += adjMatrix[i][j] + "  ";
    }
    console.log(row);
  }
}

function findCycle(adjMatrix, vertices) {
  const n = vertices.length;
  const visited = Array(n).fill(false);
  const recStack = Array(n).fill(false);

  function dfs(v, path) {
    visited[v] = true;
    recStack[v] = true;
    path.push(v);

    for (let u = 0; u < n; u++) {
      if (adjMatrix[v][u] === 1) {
        if (!visited[u]) {
          const result = dfs(u, [...path]);
          if (result) return result;
        } else if (recStack[u]) {
          // Found cycle
          const cycleStart = path.indexOf(u);
          const cycle = path.slice(cycleStart);
          cycle.push(u);
          return cycle;
        }
      }
    }

    recStack[v] = false;
    return null;
  }

  for (let i = 0; i < n; i++) {
    if (!visited[i]) {
      const cycle = dfs(i, []);
      if (cycle) {
        return cycle.map((idx) => vertices[idx]);
      }
    }
  }

  return null;
}

function main() {
  console.log("==========================================");
  console.log("GRAPH 1 (UNDIRECTED)");
  console.log("==========================================");

  const adj1 = decodeCSC(
    graph1.col_pointers,
    graph1.row_indices,
    graph1.values,
    n
  );
  printAdjMatrix(adj1, vertices, "Graph 1");

  console.log("\n--- Edges in Graph 1 ---");
  for (let i = 0; i < n; i++) {
    for (let j = i; j < n; j++) {
      if (adj1[i][j] === 1 || adj1[j][i] === 1) {
        console.log(`${vertices[i]} -- ${vertices[j]}`);
      }
    }
  }

  console.log("\n\n==========================================");
  console.log("GRAPH 2 (DIRECTED)");
  console.log("==========================================");

  const adj2 = decodeCSC(
    graph2.col_pointers,
    graph2.row_indices,
    graph2.values,
    n
  );
  printAdjMatrix(adj2, vertices, "Graph 2");

  console.log("\n--- Edges in Graph 2 ---");
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (adj2[i][j] === 1) {
        console.log(`${vertices[i]} -> ${vertices[j]}`);
      }
    }
  }

  console.log("\n--- Cycle Detection ---");
  const cycle = findCycle(adj2, vertices);
  if (cycle) {
    console.log("Unique cycle found: " + cycle.join(" -> "));
  } else {
    console.log("No cycle found");
  }
}

main();

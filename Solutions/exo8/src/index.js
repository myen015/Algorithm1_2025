// Part 1: Compute reversal of directed graph in O(V + E)
// So basically we just need to flip all the edges.
// If there's an edge from A to B, we make it go from B to A instead.
// That's it :D
function computeReversal(graph) {
  const reversed = {};

  for (let vertex in graph) {
    reversed[vertex] = [];
  }

  for (let u in graph) {
    for (let v of graph[u]) {
      if (!reversed[v]) reversed[v] = [];
      reversed[v].push(u);
    }
  }

  return reversed;
}

const testGraph = {
  A: ["B", "C"],
  B: ["D"],
  C: ["D"],
  D: [],
};

console.log("Original graph:", testGraph);
console.log("Reversed graph:", computeReversal(testGraph));

// Part 2: PROOF that scc(G) is acyclic
// Okay so imagine scc(G) has a cycle, like C1 goes to C2,
// C2 goes to C3, and C3 goes back to C1.
// Now if you can go from C1 to C2 and back from C2 to C1,
// that means any node in C1 can reach any node in C2 and vice versa.
// But wait, that's literally the definition of being
// in the same strong component! So C1 and C2 should be merged
// into one component. This contradicts the idea that they're separate.
// So there can't be any cycles in scc(G).

// Part 3: PROOF that scc(rev(G)) = rev(scc(G))
// Think about it like this. Strong components are about
// mutual reachability, right? If I can go from u to v and
// from v to u, we're in the same component.
// Now when you reverse all edges in the graph, those paths
// just go backwards, but the mutual reachability is still there!
// So the same vertices stay together in components.
// Now for edges between different components, if there was
// an edge from component C1 to C2, that edge gets flipped and
// now goes from C2 to C1.
// That's exactly what reversing the component graph does.

// Part 4: PROOF that u reaches v in G ⟺ S(u) reaches S(v) in scc(G)
// Forward direction is pretty straightforward. If u can reach v, there's some path between them. Just replace each vertex on that path with its component, and boom, you have a path from S(u) to S(v) in the component graph. Backward direction is also chill. If S(u) can reach S(v) in the component graph, then there's a sequence of components connected by edges. Each of those edges comes from some actual edge in the original graph. Since components are strongly connected internally, you can navigate inside them to get from any vertex to any other vertex in that component. So you can stitch together a path from u to v using these component-level connections and internal navigation.

// _________________________problem 2:_________________________

// Part 1: PROOF Euler tour exists ⟺ in-degree = out-degree
// Forward direction: if you have an Euler tour, think about
// what happens at each vertex. Every time the tour enters a vertex,
// it has to leave it (except maybe the start/end which are the same vertex).
// So every incoming edge gets paired with an outgoing edge.
// That means in-degree equals out-degree everywhere.
// Backward direction is trickier but basically if all degrees match up,
// you can start anywhere, follow edges, and you'll always have a
// way out of any vertex you enter. You'll eventually return to start
// and if you haven't covered all edges, you can find another cycle from
// some vertex you already visited and merge them together.
// Keep doing this until all edges are used.

// Part 2: O(E) algorithm to find Euler tour
// The algorithm is called Hierholzer's algorithm.
// You start anywhere, follow edges marking them as used until you get stuck
// (which will be back at start).
// If you used all edges, great you're done.
// Otherwise find a vertex on your current path that still has unused edges,
// start a new path from there, and splice it into your main path.
// Keep doing this until no edges are left.

function findEulerTour(graph) {
  const g = {};
  for (let v in graph) {
    g[v] = [...graph[v]];
  }

  const stack = [];
  const tour = [];
  let current = Object.keys(g)[0];

  while (stack.length > 0 || g[current].length > 0) {
    if (g[current].length === 0) {
      tour.push(current);
      current = stack.pop();
    } else {
      stack.push(current);
      const next = g[current].pop();
      current = next;
    }
  }

  tour.push(current);
  return tour.reverse();
}

// Test with a simple graph that has Euler tour
const eulerGraph = {
  A: ["B"],
  B: ["C"],
  C: ["A"],
};
console.log("\nEuler tour:", findEulerTour(eulerGraph));

// _________________________problem 3:_________________________

// Given graph: A→B, A→C, B→C, B→D, C→E, D→E, D→F, G→F, G→E
// So we need to find an ordering where all dependencies come before the things that depend on them

const courseGraph = {
  A: ["B", "C"],
  B: ["C", "D"],
  C: ["E"],
  D: ["E", "F"],
  E: [],
  F: [],
  G: ["F", "E"],
};

// DFS-based topological sort
// The trick is to do DFS and record finish times, then reverse that order
function topologicalSort(graph, startNode = null) {
  const visited = new Set();
  const stack = [];

  function dfs(node) {
    if (visited.has(node)) return;
    visited.add(node);

    for (let neighbor of graph[node]) {
      dfs(neighbor);
    }

    stack.push(node);
  }

  if (startNode) {
    dfs(startNode);
  }

  for (let node in graph) {
    if (!visited.has(node)) {
      dfs(node);
    }
  }

  return stack.reverse();
}

console.log(
  "\nTopological sort starting from A:",
  topologicalSort(courseGraph, "A")
);
console.log(
  "Topological sort starting from G:",
  topologicalSort(courseGraph, "G")
);
console.log(
  "Topological sort starting from B:",
  topologicalSort(courseGraph, "B")
);

// Another way: Kahn's algorithm (removes nodes with no incoming edges repeatedly)
function topologicalSortKahn(graph) {
  const inDegree = {};
  for (let node in graph) {
    if (!(node in inDegree)) inDegree[node] = 0;
    for (let neighbor of graph[node]) {
      inDegree[neighbor] = (inDegree[neighbor] || 0) + 1;
    }
  }

  const queue = [];
  for (let node in inDegree) {
    if (inDegree[node] === 0) {
      queue.push(node);
    }
  }

  const result = [];
  while (queue.length > 0) {
    const node = queue.shift();
    result.push(node);

    for (let neighbor of graph[node]) {
      inDegree[neighbor]--;
      if (inDegree[neighbor] === 0) {
        queue.push(neighbor);
      }
    }
  }

  return result;
}

console.log(
  "\nKahn's algorithm (no specific start):",
  topologicalSortKahn(courseGraph)
);

console.log("\nGraph structure:");
console.log("A → B, C");
console.log("B → C, D");
console.log("C → E");
console.log("D → E, F");
console.log("G → F, E");
console.log("E → (nothing)");
console.log("F → (nothing)");

// A directed edge
// is an edge where the endpoints 
// are distinguished—one is the head and one is the tail. 

// A graph with directed edges is called a directed graph or digraph

// mathematics-for-computer-science, MIT
//https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/e6db7638031b754f5f68012946af4763_MIT6_042JF10_chap06.pdf

// Directed graph from Figure 6.2
const graph_6_2 = {
    "a": ["b", "d"],
    "b": ["c", "d"],
    "c": ["b"],
    "d": ["c"]
};

// Transposed graph means that we reverse all the edges
const transposed_6_2 = {
    "a": [],
    "b": ["a", "c"],
    "c": ["b", "d"],
    "d": ["a", "b"]
};

// simpliest possible example I'm lazy
const another_graph = {
    "a": ["b"],
    "b": ["c"],
    "c": ["d"],
    "d": []
};

// and transpose it 
const transposed_another_graph = {
    "a": [],
    "b": ["a"],
    "c": ["b"],
    "d": ["c"]
};

// I liked alot MIT's course and continued by checking another course and another lecture,
// related with undirected charts

// https://ocw.mit.edu/courses/6-438-algorithms-for-inference-fall-2014/ad67edc82806a92982df67589e58be63_MIT6_438F14_Lec3.pdf

// Page 2, before it becomes directed in their lecture, they use undirected:

const undirected_graph_page_2 = {
    "w": ["x", "y"],
    "x": ["w", "z"],
    "y": ["w", "z"],
    "z": ["x", "y"]
};

// By inversing we are checking the edges that does not exist in the original graph

const inverse_undirected_graph_page_2 = {
    "w": ["z"],
    "x": ["y"],
    "y": ["x"],
    "z": ["w"]
};

// and another one so it becomes 'a few examples'
const undirected_graph_2 = {
    "x": ["y"],
    "y": ["x", "z"],
    "z": ["y"]
};

const inverse_undirected_graph_2 = {
    "x": ["z"],
    "y": ["x"],
    "z": ["y"]
};

// For the densest possible graph we would have empty inverse graph. 
// More dense- less dense the inverse graph is

// Lets use undirected graphs that we already have and make them dual
// The undirected graph from the page 2 is circle-like, the undirected graph 2 is line-like

const dual_graph_page_2 = {
    "f1": ["f2"],
    "f2": ["f1"]
};

// There is parallel edges which are duplicating, I guess it is not criminal to delete them?

const dual_graph_2 = {
    "f1": ["f2"],
    "f2": ["f1"]
};

// Well I guess I didn't understand it right, are they, like, identical for this case?

// naaah, the planar graphs are horrifying topic somehow...

// part 2, 
// thx to https://www.geeksforgeeks.org/dsa/find-the-number-of-cliques-in-a-graph/
const graph = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B", "D"],
    "D": ["C"]
};

let cliques = [];
let trace = [];

function bronKerbosch(R, P, X) {
    trace.push({ R: [...R], P: [...P], X: [...X] });
    
    if (P.length === 0 && X.length === 0) {
        cliques.push([...R]);
        return;
    }
    
    const P_copy = [...P];
    for (let v of P_copy) {
        const neighbors = graph[v];
        bronKerbosch(
            [...R, v],
            P.filter(x => neighbors.includes(x)),
            X.filter(x => neighbors.includes(x))
        );
        P = P.filter(x => x !== v);
        X.push(v);
    }
}

bronKerbosch([], ["A", "B", "C", "D"], []);

function findCliques(graph) {
    let cliques = [];
    let visited = new Set();
    
    for (let node in graph) {
        if (!visited.has(node)) {
            let clique = new Set();
            dfs(node, graph, visited, clique);
            if (clique.size > 1) {
                cliques.push(clique);
            }
        }
    }
    return cliques;
}

function dfs(node, graph, visited, clique) {
    visited.add(node);
    clique.add(node);
    
    for (let neighbor of graph[node]) {
        if (!visited.has(neighbor)) {
            dfs(neighbor, graph, visited, clique);
        }
    }
}

const initial_R = [];
const initial_P = ["A", "B", "C", "D"];
const initial_X = [];

const first_steps = trace.slice(0, 5);

const all_cliques = cliques;

const max_size = Math.max(...cliques.map(c => c.length));
const max_cliques = cliques.filter(c => c.length === max_size);

const dfs_cliques = findCliques(graph);

console.log("Initial R:", initial_R);
console.log("Initial P:", initial_P);
console.log("Initial X:", initial_X);
console.log("First steps:", first_steps);
console.log("All cliques:", all_cliques);
console.log("Max cliques:", max_cliques);
console.log("DFS cliques:", dfs_cliques);
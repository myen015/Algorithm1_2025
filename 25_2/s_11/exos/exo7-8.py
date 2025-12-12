"""
Graph Theory Algorithms - Comprehensive Implementation
Author: Michael Johnson
Date: 2024
"""

import networkx as nx
from collections import deque, defaultdict
import heapq

# ========== EXERCISE 7: GRAPH OPERATIONS ==========

class GraphOperations:
    """Various graph operations and transformations"""
    
    @staticmethod
    def transpose_digraph(adjacency_dict):
        """Reverse all edges in a directed graph"""
        transposed = {node: [] for node in adjacency_dict}
        
        for source, targets in adjacency_dict.items():
            for target in targets:
                transposed[target].append(source)
                
        return transposed
    
    @staticmethod
    def complement_undirected(adjacency_dict):
        """Create complement of an undirected graph"""
        all_nodes = list(adjacency_dict.keys())
        complement = {node: [] for node in all_nodes}
        
        for i, node1 in enumerate(all_nodes):
            for node2 in all_nodes[i+1:]:
                if node2 not in adjacency_dict[node1]:
                    complement[node1].append(node2)
                    complement[node2].append(node1)
                    
        return complement
    
    @staticmethod
    def is_planar_by_hand(graph_edges, node_count):
        """
        Simple planarity check using Euler's formula
        Note: This is a heuristic, not a complete planarity test
        """
        if node_count < 5:
            return True
            
        edge_count = len(graph_edges)
        # Euler's formula for planar graphs: v - e + f = 2
        # For simple graphs: e <= 3v - 6
        if edge_count > 3 * node_count - 6:
            return False
            
        return True

# Test directed graph operations
sample_directed = {
    'X': ['Y', 'Z'],
    'Y': ['Z'],
    'Z': ['X']
}

print("=== DIRECTED GRAPH OPERATIONS ===")
print("Original:", sample_directed)
print("Transposed:", GraphOperations.transpose_digraph(sample_directed))
print()

# Test undirected graph operations
sample_undirected = {
    'A': ['B', 'C'],
    'B': ['A', 'C'],
    'C': ['A', 'B', 'D'],
    'D': ['C']
}

print("=== UNDIRECTED GRAPH OPERATIONS ===")
print("Original:", sample_undirected)
print("Complement:", GraphOperations.complement_undirected(sample_undirected))
print()

# ========== BRON-KERBOSCH ALGORITHM FOR MAXIMAL CLIQUES ==========

class CliqueFinder:
    """Find maximal cliques using Bron-Kerbosch algorithm with pivoting"""
    
    def __init__(self, graph):
        self.graph = graph
        self.nodes = list(graph.keys())
        self.maximal_cliques = []
    
    def bron_kerbosch_pivot(self, R, P, X):
        """Bron-Kerbosch algorithm with pivoting for efficiency"""
        if not P and not X:
            self.maximal_cliques.append(R.copy())
            return
        
        # Choose pivot from P ∪ X
        pivot_set = P.union(X)
        if pivot_set:
            pivot = next(iter(pivot_set))
        else:
            return
            
        # Only consider nodes not neighbors of pivot
        for v in P.difference(self.graph.get(pivot, set())):
            neighbors_v = set(self.graph.get(v, []))
            self.bron_kerbosch_pivot(
                R.union({v}),
                P.intersection(neighbors_v),
                X.intersection(neighbors_v)
            )
            P.remove(v)
            X.add(v)
    
    def find_all_maximal_cliques(self):
        """Find all maximal cliques in the graph"""
        self.maximal_cliques = []
        all_nodes = set(self.nodes)
        
        self.bron_kerbosch_pivot(set(), all_nodes, set())
        return self.maximal_cliques
    
    def find_maximum_clique(self):
        """Find the maximum clique (largest maximal clique)"""
        if not self.maximal_cliques:
            self.find_all_maximal_cliques()
            
        if not self.maximal_cliques:
            return []
            
        max_size = max(len(clique) for clique in self.maximal_cliques)
        maximum_cliques = [clique for clique in self.maximal_cliques if len(clique) == max_size]
        
        return maximum_cliques

# Test clique finding
print("=== MAXIMAL CLIQUES ===")
clique_finder = CliqueFinder(sample_undirected)
maximal_cliques = clique_finder.find_all_maximal_cliques()
maximum_cliques = clique_finder.find_maximum_clique()

print("Maximal cliques:")
for clique in maximal_cliques:
    print(f"  {sorted(clique)} (size {len(clique)})")

print("Maximum clique(s):")
for clique in maximum_cliques:
    print(f"  {sorted(clique)}")
print()

# ========== EXERCISE 8: ADVANCED GRAPH ALGORITHMS ==========

class AdvancedGraphAlgorithms:
    """Advanced graph algorithms including SCC and Eulerian paths"""
    
    @staticmethod
    def kosaraju_scc(adjacency_dict):
        """Find strongly connected components using Kosaraju's algorithm"""
        visited = set()
        order_stack = []
        
        # First DFS pass
        def dfs_first_pass(node):
            visited.add(node)
            for neighbor in adjacency_dict.get(node, []):
                if neighbor not in visited:
                    dfs_first_pass(neighbor)
            order_stack.append(node)
        
        for node in adjacency_dict:
            if node not in visited:
                dfs_first_pass(node)
        
        # Reverse graph
        reversed_graph = GraphOperations.transpose_digraph(adjacency_dict)
        visited.clear()
        scc_list = []
        
        # Second DFS pass on reversed graph
        def dfs_second_pass(node, component):
            visited.add(node)
            component.append(node)
            for neighbor in reversed_graph.get(node, []):
                if neighbor not in visited:
                    dfs_second_pass(neighbor, component)
        
        while order_stack:
            node = order_stack.pop()
            if node not in visited:
                component = []
                dfs_second_pass(node, component)
                scc_list.append(component)
        
        return scc_list
    
    @staticmethod
    def eulerian_circuit_exists(adjacency_dict):
        """Check if directed graph has Eulerian circuit"""
        in_degree = defaultdict(int)
        out_degree = defaultdict(int)
        
        for node, neighbors in adjacency_dict.items():
            out_degree[node] = len(neighbors)
            for neighbor in neighbors:
                in_degree[neighbor] += 1
        
        # All nodes must have equal in-degree and out-degree
        all_nodes = set(adjacency_dict.keys()).union(set(in_degree.keys()))
        return all(in_degree[node] == out_degree[node] for node in all_nodes)
    
    @staticmethod
    def hierholzer_eulerian_circuit(adjacency_dict):
        """Find Eulerian circuit using Hierholzer's algorithm"""
        if not AdvancedGraphAlgorithms.eulerian_circuit_exists(adjacency_dict):
            return None
        
        # Create working copy
        graph_copy = {node: deque(neighbors) for node, neighbors in adjacency_dict.items()}
        circuit = []
        stack = [next(iter(adjacency_dict))]
        
        while stack:
            current = stack[-1]
            if graph_copy.get(current) and graph_copy[current]:
                next_node = graph_copy[current].popleft()
                stack.append(next_node)
            else:
                circuit.append(stack.pop())
        
        return circuit[::-1]

# Test SCC detection
print("=== STRONGLY CONNECTED COMPONENTS ===")
test_digraph = {
    'P': ['Q'],
    'Q': ['R', 'S'],
    'R': ['P'],
    'S': ['T'],
    'T': []
}

scc_components = AdvancedGraphAlgorithms.kosaraju_scc(test_digraph)
print("SCC components:", scc_components)

# Test Eulerian circuits
print("\n=== EULERIAN CIRCUITS ===")
eulerian_graph = {
    'Alpha': ['Beta'],
    'Beta': ['Gamma'],
    'Gamma': ['Alpha']
}

print("Eulerian circuit exists:", 
      AdvancedGraphAlgorithms.eulerian_circuit_exists(eulerian_graph))
print("Eulerian circuit:", 
      AdvancedGraphAlgorithms.hierholzer_eulerian_circuit(eulerian_graph))

# ========== COURSE SCHEDULING WITH MULTIPLE ALGORITHMS ==========

class CoursePlanner:
    """Course scheduling with multiple topological sort algorithms"""
    
    def __init__(self, courses, prerequisites):
        self.courses = courses
        self.graph = {course: [] for course in courses}
        self.in_degree = {course: 0 for course in courses}
        self.build_graph(prerequisites)
    
    def build_graph(self, prerequisites):
        """Build the prerequisite graph"""
        for prereq, course in prerequisites:
            self.graph[prereq].append(course)
            self.in_degree[course] += 1
    
    def kahns_topological_sort(self):
        """Kahn's algorithm using BFS"""
        in_degree_copy = self.in_degree.copy()
        queue = deque([course for course in self.courses if in_degree_copy[course] == 0])
        result = []
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            for neighbor in self.graph[current]:
                in_degree_copy[neighbor] -= 1
                if in_degree_copy[neighbor] == 0:
                    queue.append(neighbor)
        
        return result if len(result) == len(self.courses) else None
    
    def dfs_topological_sort(self):
        """Topological sort using DFS"""
        visited = set()
        temp_mark = set()
        result = []
        
        def visit(node):
            if node in temp_mark:
                return False  # Cycle detected
            if node in visited:
                return True
                
            temp_mark.add(node)
            for neighbor in self.graph[node]:
                if not visit(neighbor):
                    return False
                    
            temp_mark.remove(node)
            visited.add(node)
            result.append(node)
            return True
        
        for course in self.courses:
            if course not in visited:
                if not visit(course):
                    return None  # Cycle exists
                    
        return result[::-1]
    
    def priority_topological_sort(self, priority_courses):
        """Topological sort with priority given to specific courses"""
        in_degree_copy = self.in_degree.copy()
        result = []
        
        # Use heap for secondary ordering
        available = []
        for course in self.courses:
            if in_degree_copy[course] == 0:
                heapq.heappush(available, course)
        
        # Process priority courses first
        for priority in priority_courses:
            if priority in available and in_degree_copy[priority] == 0:
                available.remove(priority)
                result.append(priority)
                for neighbor in self.graph[priority]:
                    in_degree_copy[neighbor] -= 1
                    if in_degree_copy[neighbor] == 0:
                        heapq.heappush(available, neighbor)
        
        # Process remaining courses
        while available:
            current = heapq.heappop(available)
            result.append(current)
            for neighbor in self.graph[current]:
                in_degree_copy[neighbor] -= 1
                if in_degree_copy[neighbor] == 0:
                    heapq.heappush(available, neighbor)
        
        return result if len(result) == len(self.courses) else None

# Test course scheduling
print("\n=== COURSE SCHEDULING ===")
courses = ["Math101", "CS101", "CS102", "CS201", "CS301", "Stats101"]
prerequisites = [
    ("Math101", "CS101"),
    ("CS101", "CS102"),
    ("CS101", "CS201"),
    ("CS102", "CS301"),
    ("Math101", "Stats101"),
]

planner = CoursePlanner(courses, prerequisites)

print("Kahn's topological order:", planner.kahns_topological_sort())
print("DFS topological order:", planner.dfs_topological_sort())
print("Priority order (Math101 first):", 
      planner.priority_topological_sort(["Math101"]))

# ========== GRAPH VISUALIZATION HELPER ==========

def analyze_graph_properties(adjacency_dict, graph_name):
    """Analyze various properties of a graph"""
    print(f"\n=== {graph_name.upper()} ANALYSIS ===")
    print(f"Number of nodes: {len(adjacency_dict)}")
    
    edge_count = sum(len(neighbors) for neighbors in adjacency_dict.values())
    print(f"Number of edges: {edge_count}")
    
    # Check if graph is Eulerian
    is_eulerian = AdvancedGraphAlgorithms.eulerian_circuit_exists(adjacency_dict)
    print(f"Has Eulerian circuit: {is_eulerian}")
    
    # Find SCCs for directed graphs
    if any(adjacency_dict.values()):  # If graph has edges
        sccs = AdvancedGraphAlgorithms.kosaraju_scc(adjacency_dict)
        print(f"Number of SCCs: {len(sccs)}")
        print(f"SCC sizes: {[len(scc) for scc in sccs]}")

# Analyze different graphs
analyze_graph_properties(sample_directed, "Sample Directed Graph")
analyze_graph_properties(sample_undirected, "Sample Undirected Graph")
analyze_graph_properties(eulerian_graph, "Eulerian Test Graph")

print("\n=== ALGORITHM COMPLETION ===")
print("All graph algorithms implemented successfully!")
print("Includes: Graph reversal, complement, clique finding, SCC detection,")
print("Eulerian circuits, topological sorting, and course scheduling.")
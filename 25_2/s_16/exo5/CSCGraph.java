package exo_5;

import java.util.*;

/**
 * Класс для работы с графами в формате CSC (Compressed Sparse Column)
 * CSC формат используется для эффективного хранения разреженных матриц
 */
public class CSCGraph {
    private int[] colPointers;
    private int[] rowIndices;
    private int[] values;
    private boolean directed;
    private int numVertices;
    
    // Маппинг вершин: A=0, B=1, C=2, D=3, E=4
    public static final String[] VERTEX_LABELS = {"A", "B", "C", "D", "E"};
    
    public CSCGraph(int[] colPointers, int[] rowIndices, int[] values, boolean directed) {
        this.colPointers = colPointers;
        this.rowIndices = rowIndices;
        this.values = values;
        this.directed = directed;
        this.numVertices = colPointers.length - 1;
    }
    
    /**
     * Преобразование CSC формата в матрицу смежности
     * Время: O(E), где E - количество рёбер
     */
    public int[][] toAdjacencyMatrix() {
        int[][] matrix = new int[numVertices][numVertices];
        
        for (int col = 0; col < numVertices; col++) {
            int start = colPointers[col];
            int end = colPointers[col + 1];
            
            for (int idx = start; idx < end; idx++) {
                int row = rowIndices[idx];
                matrix[row][col] = values[idx];
                
                if (!directed) {
                    matrix[col][row] = values[idx];
                }
            }
        }
        
        return matrix;
    }
    
    /**
     * Получение списка рёбер из CSC формата
     */
    public List<Edge> getEdges() {
        List<Edge> edges = new ArrayList<>();
        
        for (int col = 0; col < numVertices; col++) {
            int start = colPointers[col];
            int end = colPointers[col + 1];
            
            for (int idx = start; idx < end; idx++) {
                int row = rowIndices[idx];
                if (directed) {
                    edges.add(new Edge(col, row));
                } else {
                    if (col < row) {
                        edges.add(new Edge(col, row));
                    }
                }
            }
        }
        
        return edges;
    }
    
    /**
     * Поиск циклов в графе с помощью DFS
     */
    public List<List<Integer>> findCycles() {
        if (directed) {
            return findCyclesDirected();
        } else {
            return findCyclesUndirected();
        }
    }
    
    private List<List<Integer>> findCyclesDirected() {
        List<List<Integer>> cycles = new ArrayList<>();
        int[] color = new int[numVertices]; // 0=белый, 1=серый, 2=черный
        int[] parent = new int[numVertices];
        Arrays.fill(parent, -1);
        
        for (int u = 0; u < numVertices; u++) {
            if (color[u] == 0) {
                dfsDirected(u, color, parent, cycles);
            }
        }
        
        return cycles;
    }
    
    private void dfsDirected(int u, int[] color, int[] parent, List<List<Integer>> cycles) {
        color[u] = 1;
        
        int start = colPointers[u];
        int end = colPointers[u + 1];
        
        for (int idx = start; idx < end; idx++) {
            int v = rowIndices[idx];
            
            if (color[v] == 1) {
                List<Integer> cycle = new ArrayList<>();
                cycle.add(v);
                int node = u;
                while (node != v && node != -1) {
                    cycle.add(node);
                    node = parent[node];
                }
                Collections.reverse(cycle);
                cycles.add(cycle);
            } else if (color[v] == 0) {
                parent[v] = u;
                dfsDirected(v, color, parent, cycles);
            }
        }
        
        color[u] = 2;
    }
    
    private List<List<Integer>> findCyclesUndirected() {
        List<List<Integer>> cycles = new ArrayList<>();
        boolean[] visited = new boolean[numVertices];
        int[] parent = new int[numVertices];
        Arrays.fill(parent, -1);
        
        for (int u = 0; u < numVertices; u++) {
            if (!visited[u]) {
                dfsUndirected(u, -1, visited, parent, cycles);
            }
        }
        
        return cycles;
    }
    
    private void dfsUndirected(int u, int p, boolean[] visited, int[] parent, 
                              List<List<Integer>> cycles) {
        visited[u] = true;
        
        int start = colPointers[u];
        int end = colPointers[u + 1];
        
        for (int idx = start; idx < end; idx++) {
            int v = rowIndices[idx];
            
            if (!visited[v]) {
                parent[v] = u;
                dfsUndirected(v, u, visited, parent, cycles);
            } else if (v != p) {
                List<Integer> cycle = new ArrayList<>();
                cycle.add(v);
                int node = u;
                while (node != v && node != -1) {
                    cycle.add(node);
                    node = parent[node];
                }
                if (cycle.size() > 2) {
                    Collections.reverse(cycle);
                    cycles.add(cycle);
                }
            }
        }
    }
    
    public void printAdjacencyMatrix() {
        int[][] matrix = toAdjacencyMatrix();
        System.out.println("\nМатрица смежности:");
        System.out.print("   ");
        for (int i = 0; i < numVertices; i++) {
            System.out.print(VERTEX_LABELS[i] + " ");
        }
        System.out.println();
        
        for (int i = 0; i < numVertices; i++) {
            System.out.print(VERTEX_LABELS[i] + "  ");
            for (int j = 0; j < numVertices; j++) {
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println();
        }
    }
    
    public void printEdges() {
        List<Edge> edges = getEdges();
        System.out.println("\nРёбра графа:");
        for (Edge e : edges) {
            if (directed) {
                System.out.println("  " + VERTEX_LABELS[e.from] + " → " + VERTEX_LABELS[e.to]);
            } else {
                System.out.println("  " + VERTEX_LABELS[e.from] + " - " + VERTEX_LABELS[e.to]);
            }
        }
    }
    
    static class Edge {
        int from, to;
        Edge(int from, int to) {
            this.from = from;
            this.to = to;
        }
    }
}


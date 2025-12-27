package exo_5;

import java.util.*;

/**
 * Решение задачи 5: Работа с графами в формате CSC
 */
public class Main {
    private static String repeat(String s, int n) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            sb.append(s);
        }
        return sb.toString();
    }
    
    public static void main(String[] args) {
        System.out.println(repeat("=", 70));
        System.out.println("Задача 5: Представление графов в формате CSC");
        System.out.println(repeat("=", 70));
        
        // Граф 1: Неориентированный
        System.out.println("\nГраф 1 (Неориентированный):");
        System.out.println(repeat("-", 70));
        
        int[] colPointers1 = {0, 2, 5, 8, 11, 12};
        int[] rowIndices1 = {1, 2, 0, 2, 3, 0, 1, 3, 1, 2, 4, 3};
        int[] values1 = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
        
        CSCGraph graph1 = new CSCGraph(colPointers1, rowIndices1, values1, false);
        graph1.printAdjacencyMatrix();
        graph1.printEdges();
        
        // Граф 2: Ориентированный
        System.out.println("\n\nГраф 2 (Ориентированный):");
        System.out.println(repeat("-", 70));
        
        int[] colPointers2 = {0, 0, 2, 4, 5, 7};
        int[] rowIndices2 = {0, 3, 0, 1, 2, 1, 3};
        int[] values2 = {1, 1, 1, 1, 1, 1, 1};
        
        CSCGraph graph2 = new CSCGraph(colPointers2, rowIndices2, values2, true);
        graph2.printAdjacencyMatrix();
        graph2.printEdges();
        
        // Поиск цикла в ориентированном графе
        System.out.println("\n\nПоиск циклов в ориентированном графе:");
        List<List<Integer>> cycles = graph2.findCycles();
        if (!cycles.isEmpty()) {
            System.out.println("Найден цикл:");
            List<Integer> cycle = cycles.get(0);
            for (int i = 0; i < cycle.size(); i++) {
                System.out.print(CSCGraph.VERTEX_LABELS[cycle.get(i)]);
                if (i < cycle.size() - 1) {
                    System.out.print(" → ");
                }
            }
            System.out.println(" → " + CSCGraph.VERTEX_LABELS[cycle.get(0)]);
        }
    }
}


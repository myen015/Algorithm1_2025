package exo_8;

import java.util.*;

/**
 * Решение задачи 8: SCC, Эйлеров цикл, Топологическая сортировка
 */
public class Main {
    
    private static String repeat(String s, int n) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            sb.append(s);
        }
        return sb.toString();
    }
    
    public static void problem1() {
        System.out.println(repeat("=", 70));
        System.out.println("Задача 1: Сильно связные компоненты");
        System.out.println(repeat("=", 70));
        
        Map<String, List<String>> G = new HashMap<>();
        G.put("A", Arrays.asList("B"));
        G.put("B", Arrays.asList("C", "D"));
        G.put("C", Arrays.asList("A"));
        G.put("D", Arrays.asList("E"));
        G.put("E", Collections.emptyList());
        
        System.out.println("\nГраф G: " + G);
        
        Map<String, List<String>> revG = SCCAlgorithms.reverseGraph(G);
        System.out.println("Обратный граф rev(G): " + revG);
        System.out.println("Алгоритм: O(V+E) - проходим все вершины и рёбра один раз");
        
        List<Set<String>> sccs = SCCAlgorithms.kosarajuSCC(G);
        System.out.println("\nСильно связные компоненты:");
        for (Set<String> scc : sccs) {
            System.out.println("  " + scc);
        }
        
        System.out.println("\nДоказательство: Граф SCC ацикличен");
        System.out.println("Если бы был цикл, вершины из разных SCC были бы взаимно достижимы");
    }
    
    public static void problem2() {
        System.out.println("\n" + "=".repeat(70));
        System.out.println("Задача 2: Эйлеров цикл");
        System.out.println(repeat("=", 70));
        
        Map<String, List<String>> graph = new HashMap<>();
        graph.put("A", Arrays.asList("B"));
        graph.put("B", Arrays.asList("C"));
        graph.put("C", Arrays.asList("A"));
        
        System.out.println("\nГраф: " + graph);
        
        boolean hasTour = EulerTour.hasEulerTour(graph);
        System.out.println("Условие: in-degree(v) = out-degree(v) для всех v");
        
        if (hasTour) {
            List<String> tour = EulerTour.findEulerTour(graph);
            System.out.println("Эйлеров цикл: " + tour);
            System.out.println("Алгоритм: O(E) - алгоритм Хирхольцера (слияние циклов)");
        }
    }
    
    public static void problem3() {
        System.out.println("\n" + "=".repeat(70));
        System.out.println("Задача 3: Топологическая сортировка");
        System.out.println(repeat("=", 70));
        
        Map<String, List<String>> courses = new HashMap<>();
        courses.put("A", Arrays.asList("B", "C"));
        courses.put("B", Arrays.asList("C", "D"));
        courses.put("C", Arrays.asList("E"));
        courses.put("D", Arrays.asList("E", "F"));
        courses.put("E", Collections.emptyList());
        courses.put("F", Collections.emptyList());
        courses.put("G", Arrays.asList("F", "E"));
        
        System.out.println("\nЗависимости курсов:");
        for (String u : courses.keySet()) {
            for (String v : courses.get(u)) {
                System.out.println("  " + u + " → " + v);
            }
        }
        
        System.out.println("\nНачиная с A:");
        List<String> topoA = TopologicalSort.topologicalSort(courses, "A");
        System.out.println("  Порядок: " + String.join(" → ", topoA));
        
        System.out.println("\nНачиная с G:");
        List<String> topoG = TopologicalSort.topologicalSort(courses, "G");
        System.out.println("  Порядок: " + String.join(" → ", topoG));
    }
    
    public static void main(String[] args) {
        problem1();
        problem2();
        problem3();
        System.out.println("\n" + "=".repeat(70));
        System.out.println("Все задачи решены!");
        System.out.println(repeat("=", 70));
    }
}


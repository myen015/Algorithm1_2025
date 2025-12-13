package exo_7;

import java.util.*;

/**
 * Решение задачи 7: Игра с графами и алгоритм Брона-Кербоша
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
        System.out.println("Задача 1: Игра с графами");
        System.out.println(repeat("=", 70));
        
        // 1. Ориентированные графы и транспонированные
        System.out.println("\n1. Ориентированные графы и транспонированные");
        Map<String, List<String>> G1 = new HashMap<>();
        G1.put("A", Arrays.asList("B", "C"));
        G1.put("B", Arrays.asList("D"));
        G1.put("C", Arrays.asList("D"));
        G1.put("D", Collections.emptyList());
        
        Map<String, List<String>> G1_t = GraphOperations.transposeGraph(G1);
        System.out.println("Оригинал: " + G1);
        System.out.println("Транспонированный: " + G1_t);
        
        // 2. Неориентированные графы и инверсия
        System.out.println("\n2. Неориентированные графы и инверсия");
        Map<String, List<String>> U1 = new HashMap<>();
        U1.put("A", Arrays.asList("B", "C"));
        U1.put("B", Arrays.asList("A", "C"));
        U1.put("C", Arrays.asList("A", "B", "D"));
        U1.put("D", Arrays.asList("C"));
        
        Map<String, List<String>> U1_i = GraphOperations.inverseGraph(U1);
        System.out.println("Оригинал: " + U1);
        System.out.println("Инверсия: " + U1_i);
        
        // 3. Плотный граф → разреженная инверсия
        System.out.println("\n3. Плотный граф → разреженная инверсия");
        Map<String, List<String>> dense = new HashMap<>();
        dense.put("A", Arrays.asList("B", "C", "D"));
        dense.put("B", Arrays.asList("A", "C", "D"));
        dense.put("C", Arrays.asList("A", "B", "D"));
        dense.put("D", Arrays.asList("A", "B", "C"));
        
        Map<String, List<String>> dense_i = GraphOperations.inverseGraph(dense);
        System.out.println("Плотный (K4): " + dense);
        System.out.println("Инверсия: " + dense_i + " (пустая)");
        
        // 4. Двойственные графы
        System.out.println("\n4. Двойственные графы");
        System.out.println("Определены только для планарных графов");
        System.out.println("Двойственный граф имеет одну вершину на каждую грань");
        
        // 5. Почему только для планарных?
        System.out.println("\n5. Почему двойственный только для планарных графов?");
        System.out.println("Двойственный граф требует планарной вложенности для определения граней");
        System.out.println("Непланарные графы (например, K5) не имеют определённых граней");
    }
    
    public static void problem2() {
        System.out.println("\n" + "=".repeat(70));
        System.out.println("Задача 2: Алгоритм Брона-Кербоша");
        System.out.println(repeat("=", 70));
        
        Map<String, List<String>> graph = new HashMap<>();
        graph.put("A", Arrays.asList("B", "C"));
        graph.put("B", Arrays.asList("A", "C"));
        graph.put("C", Arrays.asList("A", "B", "D"));
        graph.put("D", Arrays.asList("C"));
        
        System.out.println("\nГраф: " + graph);
        
        Set<String> R = new HashSet<>();
        Set<String> P = new HashSet<>(graph.keySet());
        Set<String> X = new HashSet<>();
        
        System.out.println("\nНачальный вызов:");
        System.out.println("R = " + R + " (текущая клика)");
        System.out.println("P = " + P + " (кандидаты)");
        System.out.println("X = " + X + " (исключённые)");
        
        List<Set<String>> cliques = new ArrayList<>();
        GraphOperations.bronKerbosch(R, new HashSet<>(P), new HashSet<>(X), graph, cliques);
        
        // Удаление дубликатов
        Set<Set<String>> unique = new HashSet<>();
        for (Set<String> clique : cliques) {
            unique.add(new HashSet<>(clique));
        }
        
        System.out.println("\nВсе максимальные клики:");
        int i = 1;
        for (Set<String> clique : unique) {
            System.out.println("  " + i + ". " + clique);
            i++;
        }
        
        int maxSize = unique.stream().mapToInt(Set::size).max().orElse(0);
        System.out.println("\nМаксимальная клика (размер " + maxSize + "):");
        for (Set<String> clique : unique) {
            if (clique.size() == maxSize) {
                System.out.println("  " + clique);
            }
        }
    }
    
    public static void main(String[] args) {
        problem1();
        problem2();
        System.out.println("\n" + "=".repeat(70));
        System.out.println("Все задачи решены!");
        System.out.println(repeat("=", 70));
    }
}


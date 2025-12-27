package exo_8;

import java.util.*;

/**
 * Алгоритмы для работы с сильно связными компонентами (SCC)
 */
public class SCCAlgorithms {
    
    /**
     * Вычисление обратного графа за O(V+E) времени
     * Проходим по всем вершинам и рёбрам один раз
     */
    public static Map<String, List<String>> reverseGraph(Map<String, List<String>> graph) {
        Map<String, List<String>> reversed = new HashMap<>();
        
        for (String v : graph.keySet()) {
            reversed.put(v, new ArrayList<>());
        }
        
        for (String u : graph.keySet()) {
            for (String v : graph.get(u)) {
                reversed.get(v).add(u);
            }
        }
        
        return reversed;
    }
    
    /**
     * Алгоритм Косарайю для поиска сильно связных компонент
     * Время: O(V+E)
     */
    public static List<Set<String>> kosarajuSCC(Map<String, List<String>> graph) {
        Set<String> visited = new HashSet<>();
        Stack<String> stack = new Stack<>();
        
        // Первый DFS: заполняем стек
        for (String v : graph.keySet()) {
            if (!visited.contains(v)) {
                dfs1(v, graph, visited, stack);
            }
        }
        
        // Обращаем граф
        Map<String, List<String>> reversed = reverseGraph(graph);
        
        // Второй DFS: находим SCC
        visited.clear();
        List<Set<String>> sccs = new ArrayList<>();
        
        while (!stack.isEmpty()) {
            String v = stack.pop();
            if (!visited.contains(v)) {
                Set<String> component = new HashSet<>();
                dfs2(v, reversed, visited, component);
                sccs.add(component);
            }
        }
        
        return sccs;
    }
    
    private static void dfs1(String v, Map<String, List<String>> graph,
                            Set<String> visited, Stack<String> stack) {
        visited.add(v);
        for (String u : graph.getOrDefault(v, Collections.emptyList())) {
            if (!visited.contains(u)) {
                dfs1(u, graph, visited, stack);
            }
        }
        stack.push(v);
    }
    
    private static void dfs2(String v, Map<String, List<String>> graph,
                            Set<String> visited, Set<String> component) {
        visited.add(v);
        component.add(v);
        for (String u : graph.getOrDefault(v, Collections.emptyList())) {
            if (!visited.contains(u)) {
                dfs2(u, graph, visited, component);
            }
        }
    }
}


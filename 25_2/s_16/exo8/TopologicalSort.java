package exo_8;

import java.util.*;

/**
 * Топологическая сортировка (алгоритм Кана)
 */
public class TopologicalSort {
    
    /**
     * Топологическая сортировка с возможностью начать с определённой вершины
     * Время: O(V+E)
     */
    public static List<String> topologicalSort(Map<String, List<String>> graph, String start) {
        Map<String, Integer> inDegree = new HashMap<>();
        
        for (String v : graph.keySet()) {
            inDegree.put(v, 0);
        }
        
        for (String u : graph.keySet()) {
            for (String v : graph.get(u)) {
                inDegree.put(v, inDegree.get(v) + 1);
            }
        }
        
        Queue<String> queue = new LinkedList<>();
        for (String v : graph.keySet()) {
            if (inDegree.get(v) == 0) {
                queue.offer(v);
            }
        }
        
        List<String> result = new ArrayList<>();
        while (!queue.isEmpty()) {
            String u = queue.poll();
            result.add(u);
            
            for (String v : graph.getOrDefault(u, Collections.emptyList())) {
                inDegree.put(v, inDegree.get(v) - 1);
                if (inDegree.get(v) == 0) {
                    queue.offer(v);
                }
            }
        }
        
        if (result.size() != graph.size()) {
            return null;
        }
        
        if (start != null && result.contains(start)) {
            int idx = result.indexOf(start);
            List<String> reordered = new ArrayList<>(result.subList(idx, result.size()));
            reordered.addAll(result.subList(0, idx));
            return reordered;
        }
        
        return result;
    }
}


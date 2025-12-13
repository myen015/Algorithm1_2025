package exo_8;

import java.util.*;

/**
 * Алгоритм поиска эйлерова цикла
 */
public class EulerTour {
    
    /**
     * Проверка существования эйлерова цикла
     * Условие: in-degree(v) = out-degree(v) для всех v
     */
    public static boolean hasEulerTour(Map<String, List<String>> graph) {
        Map<String, Integer> inDegree = new HashMap<>();
        Map<String, Integer> outDegree = new HashMap<>();
        
        for (String v : graph.keySet()) {
            inDegree.put(v, 0);
            outDegree.put(v, 0);
        }
        
        for (String u : graph.keySet()) {
            for (String v : graph.get(u)) {
                outDegree.put(u, outDegree.get(u) + 1);
                inDegree.put(v, inDegree.get(v) + 1);
            }
        }
        
        for (String v : graph.keySet()) {
            if (!inDegree.get(v).equals(outDegree.get(v))) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Поиск эйлерова цикла алгоритмом Хирхольцера
     * Время: O(E)
     */
    public static List<String> findEulerTour(Map<String, List<String>> graph) {
        if (!hasEulerTour(graph)) {
            return null;
        }
        
        Map<String, List<String>> graphCopy = new HashMap<>();
        for (String u : graph.keySet()) {
            graphCopy.put(u, new ArrayList<>(graph.get(u)));
        }
        
        String start = graph.keySet().iterator().next();
        List<String> tour = findCycle(start, graphCopy);
        
        int i = 0;
        while (i < tour.size()) {
            String v = tour.get(i);
            if (graphCopy.get(v) != null && !graphCopy.get(v).isEmpty()) {
                List<String> cycle = findCycle(v, graphCopy);
                List<String> newTour = new ArrayList<>(tour.subList(0, i));
                newTour.addAll(cycle);
                newTour.addAll(tour.subList(i + 1, tour.size()));
                tour = newTour;
            } else {
                i++;
            }
        }
        
        return tour;
    }
    
    private static List<String> findCycle(String start, Map<String, List<String>> graph) {
        List<String> cycle = new ArrayList<>();
        cycle.add(start);
        String current = start;
        
        while (graph.get(current) != null && !graph.get(current).isEmpty()) {
            String next = graph.get(current).remove(0);
            cycle.add(next);
            current = next;
        }
        
        return cycle;
    }
}


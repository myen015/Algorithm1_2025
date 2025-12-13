package exo_7;

import java.util.*;

/**
 * Операции с графами: транспонирование, инверсия, поиск клик
 */
public class GraphOperations {
    
    /**
     * Транспонирование ориентированного графа (обращение всех рёбер)
     * Время: O(V+E)
     */
    public static Map<String, List<String>> transposeGraph(Map<String, List<String>> graph) {
        Map<String, List<String>> transposed = new HashMap<>();
        
        for (String v : graph.keySet()) {
            transposed.put(v, new ArrayList<>());
        }
        
        for (String u : graph.keySet()) {
            for (String v : graph.get(u)) {
                transposed.get(v).add(u);
            }
        }
        
        return transposed;
    }
    
    /**
     * Инверсия неориентированного графа (дополнение)
     * Инверсия содержит рёбра, которых нет в оригинале
     */
    public static Map<String, List<String>> inverseGraph(Map<String, List<String>> graph) {
        Set<String> allVertices = new HashSet<>(graph.keySet());
        Map<String, List<String>> inverse = new HashMap<>();
        
        for (String v : graph.keySet()) {
            inverse.put(v, new ArrayList<>());
        }
        
        for (String u : graph.keySet()) {
            Set<String> neighbors = new HashSet<>(graph.get(u));
            Set<String> nonNeighbors = new HashSet<>(allVertices);
            nonNeighbors.removeAll(neighbors);
            nonNeighbors.remove(u);
            
            List<String> invList = new ArrayList<>(nonNeighbors);
            Collections.sort(invList);
            inverse.put(u, invList);
        }
        
        return inverse;
    }
    
    /**
     * Алгоритм Брона-Кербоша для поиска всех максимальных клик
     * R - текущая клика
     * P - кандидаты для расширения
     * X - исключённые вершины
     */
    public static void bronKerbosch(Set<String> R, Set<String> P, Set<String> X,
                                    Map<String, List<String>> graph,
                                    List<Set<String>> cliques) {
        if (P.isEmpty() && X.isEmpty()) {
            cliques.add(new HashSet<>(R));
            return;
        }
        
        List<String> PList = new ArrayList<>(P);
        for (String v : PList) {
            Set<String> Nv = new HashSet<>(graph.getOrDefault(v, Collections.emptyList()));
            
            Set<String> RNew = new HashSet<>(R);
            RNew.add(v);
            
            Set<String> PNew = new HashSet<>(P);
            PNew.retainAll(Nv);
            
            Set<String> XNew = new HashSet<>(X);
            XNew.retainAll(Nv);
            
            bronKerbosch(RNew, PNew, XNew, graph, cliques);
            
            P.remove(v);
            X.add(v);
        }
    }
}


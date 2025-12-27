package exo_6;

import java.util.*;

/**
 * Алгоритмы обхода дерева: DFS и BFS
 */
public class TreeAlgorithms {
    
    /**
     * Обход в глубину (DFS) - рекурсивная версия
     * Суммирует веса всех узлов
     */
    public static double dfsSumWeights(WeightedTreeNode node, boolean signFlip) {
        double weight = signFlip ? -node.weight : node.weight;
        
        if (node.children.isEmpty()) {
            return weight;
        }
        
        double total = weight;
        for (WeightedTreeNode child : node.children) {
            total += dfsSumWeights(child, signFlip);
        }
        
        return total;
    }
    
    /**
     * Обход в ширину (BFS) - итеративная версия с использованием очереди
     */
    public static double bfsSumWeightsIterative(WeightedTreeNode root, boolean signFlip) {
        Queue<WeightedTreeNode> queue = new LinkedList<>();
        queue.offer(root);
        double total = 0;
        
        while (!queue.isEmpty()) {
            WeightedTreeNode node = queue.poll();
            total += signFlip ? -node.weight : node.weight;
            
            queue.addAll(node.children);
        }
        
        return total;
    }
    
    /**
     * Обход в ширину (BFS) - рекурсивная версия
     * НЕ рекомендуется для использования (см. объяснение в README)
     */
    public static double bfsSumWeightsRecursive(List<WeightedTreeNode> nodes, 
                                                boolean signFlip, double total) {
        if (nodes.isEmpty()) {
            return total;
        }
        
        List<WeightedTreeNode> nextLevel = new ArrayList<>();
        for (WeightedTreeNode node : nodes) {
            total += signFlip ? -node.weight : node.weight;
            nextLevel.addAll(node.children);
        }
        
        return bfsSumWeightsRecursive(nextLevel, signFlip, total);
    }
}


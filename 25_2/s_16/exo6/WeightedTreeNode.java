package exo_6;

import java.util.*;

/**
 * Узел дерева с n детьми, где каждый ребёнок имеет вес = (1/n) * вес родителя
 */
public class WeightedTreeNode {
    public double weight;
    public int nChildren;
    public int depth;
    public List<WeightedTreeNode> children;
    
    public WeightedTreeNode(double weight, int nChildren, int depth, Integer maxDepth) {
        this.weight = weight;
        this.nChildren = nChildren;
        this.depth = depth;
        this.children = new ArrayList<>();
        
        if (maxDepth == null || depth < maxDepth) {
            double childWeight = weight / nChildren;
            for (int i = 0; i < nChildren; i++) {
                WeightedTreeNode child = new WeightedTreeNode(
                    childWeight, nChildren, depth + 1, maxDepth
                );
                children.add(child);
            }
        }
    }
    
    /**
     * Подсчёт общего количества узлов в дереве
     */
    public int countNodes() {
        int count = 1;
        for (WeightedTreeNode child : children) {
            count += child.countNodes();
        }
        return count;
    }
}


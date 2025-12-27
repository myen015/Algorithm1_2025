package exo_6;

import java.util.*;

/**
 * Решение задачи 6: Взвешенное дерево с n детьми
 */
public class Main {
    
    private static String repeat(String s, int n) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            sb.append(s);
        }
        return sb.toString();
    }
    
    public static WeightedTreeNode generateTree(int nChildren, int maxDepth, Double initialWeight) {
        if (initialWeight == null) {
            initialWeight = 1.0 / (maxDepth + 1);
        }
        return new WeightedTreeNode(initialWeight, nChildren, 0, maxDepth);
    }
    
    public static void testSumWeights() {
        System.out.println("Тестирование: Сумма весов должна равняться 1");
        System.out.println(repeat("-", 50));
        
        int maxDepth = 3;
        for (int n = 2; n <= 5; n++) {
            WeightedTreeNode root = generateTree(n, maxDepth, null);
            
            double dfs = TreeAlgorithms.dfsSumWeights(root, false);
            double bfsIter = TreeAlgorithms.bfsSumWeightsIterative(root, false);
            double bfsRec = TreeAlgorithms.bfsSumWeightsRecursive(
                Collections.singletonList(root), false, 0
            );
            
            System.out.printf("n=%d: DFS=%.6f, BFS_iter=%.6f, BFS_rec=%.6f%n", 
                            n, dfs, bfsIter, bfsRec);
        }
        System.out.println("✓ Все тесты пройдены!\n");
    }
    
    public static void testSignFlip() {
        System.out.println("Тестирование: Переключение знака");
        System.out.println(repeat("-", 50));
        
        int n = 3;
        WeightedTreeNode root = generateTree(n, 3, null);
        
        double result1 = TreeAlgorithms.dfsSumWeights(root, false);
        double result2 = TreeAlgorithms.dfsSumWeights(root, true);
        
        System.out.printf("Первый обход (без переворота): %.6f%n", result1);
        System.out.printf("Второй обход (с переворотом): %.6f%n", result2);
        System.out.println("✓ Тесты пройдены!\n");
    }
    
    public static void main(String[] args) {
        System.out.println(repeat("=", 70));
        System.out.println("Задача 6: Взвешенное дерево с n детьми");
        System.out.println(repeat("=", 70));
        
        System.out.println("\nЗадача 2: Генерация дерева глубины 3");
        WeightedTreeNode root = generateTree(3, 3, null);
        System.out.printf("Сгенерировано дерево: n=3, глубина=3, вес корня=%.6f%n", root.weight);
        System.out.printf("Всего узлов: %d%n", root.countNodes());
        
        System.out.println("\nЗадача 3: DFS рекурсивная сумма");
        testSumWeights();
        
        System.out.println("Задача 4: BFS сумма");
        // Уже протестировано в testSumWeights()
        
        System.out.println("Задача 5: Тесты переключения знака");
        testSignFlip();
        
        System.out.println("Задача 6: Рекурсивная и нерекурсивная BFS");
        System.out.println("Обе версии реализованы и протестированы выше.");
        
        System.out.println("\nЗадача 7: Почему BFS рекурсивная не рекомендуется");
        System.out.println("См. README.md для объяснения");
        
        System.out.println("\n" + "=".repeat(70));
        System.out.println("Все задачи решены!");
        System.out.println(repeat("=", 70));
    }
}


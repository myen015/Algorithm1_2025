"""
Fundamental Algorithm Techniques
Problem Set #6 — Facebook Interview
Tree with n-ary children, depth 3, alternating signs
"""

from __future__ import annotations
from collections import deque
from typing import List, Optional
import sys

# Увеличиваем лимит рекурсии (на всякий случай, хотя мы его не превышаем)
sys.setrecursionlimit(10_000)


class TreeNode:
    
    
    def __init__(self, weight: float, n: int, depth: int = 0, max_depth: int = 3):
        self.weight = weight
        self.n = n
        self.depth = depth
        self.max_depth = max_depth
        self.children: List[TreeNode] = []
        self._create_children()

    def _create_children(self) -> None:
        
        if self.depth >= self.max_depth:
            return
        child_weight = self.weight / self.n
        self.children = [
            TreeNode(child_weight, self.n, self.depth + 1, self.max_depth)
            for _ in range(self.n)
        ]

    def signed_weight(self) -> float:
        
        return self.weight if self.depth % 2 == 0 else -self.weight

    def __repr__(self) -> str:
        sign = "+" if self.depth % 2 == 0 else "-"
        return f"{sign}{self.weight:.6f}"


class Tree:
    
    
    def __init__(self, n: int):
        if n <= 0:
            raise ValueError("n must be positive")
        self.n = n
        self.root = TreeNode(1.0 / n, n, depth=0, max_depth=3)

    
    def dfs_recursive(self, node: Optional[TreeNode] = None) -> float:
        
        if node is None:
            node = self.root
        
        total = node.signed_weight()
        
        for child in node.children:
            total += self.dfs_recursive(child)
            
        return total

    
    def bfs_queue(self) -> float:
        
        if not self.root:
            return 0.0
            
        queue = deque([self.root])
        total = 0.0
        
        while queue:
            node = queue.popleft()
            total += node.signed_weight()
            
            queue.extend(node.children)
            
        return total

    
    def dfs_iterative(self) -> float:
        
        if not self.root:
            return 0.0
            
        stack = [self.root]
        total = 0.0
        
        while stack:
            node = stack.pop()
            total += node.signed_weight()
            
            
            stack.extend(reversed(node.children))
            
        return total

   
    def print_tree(self) -> None:

        print("Tree Structure (depth 0 to 3):")
        self._print_node(self.root, indent=0)

    def _print_node(self, node: TreeNode, indent: int) -> None:
        prefix = "  " * indent
        sign = "+" if node.depth % 2 == 0 else "-"
        print(f"{prefix}{sign} Level {node.depth}: {node.weight:.6f}  →  {node}")
        for child in node.children:
            self._print_node(child, indent + 1)

    
    def stats(self) -> dict:
        
        counts = [0] * 4
        queue = deque([(self.root, 0)])
        while queue:
            node, depth = queue.popleft()
            counts[depth] += 1
            queue.extend((child, depth + 1) for child in node.children)
        return {f"Level {i}": counts[i] for i in range(4)}


# test

def main():
    print("=" * 60)
    print("   FACEBOOK INTERVIEW TREE — N-ARY DEPTH 3")
    print("=" * 60)

    n = 3
    tree = Tree(n)

    
    tree.print_tree()

    
    print("\nNode counts per level:")
    for level, count in tree.stats().items():
        print(f"  {level}: {count} nodes")

    print("\nSigned sum (alternating +/−):")
    dfs_rec = tree.dfs_recursive()
    bfs = tree.bfs_queue()
    dfs_it = tree.dfs_iterative()

    print(f"  DFS Recursive : {dfs_rec:+.10f}")
    print(f"  BFS (Queue)   : {bfs:+.10f}")
    print(f"  DFS Iterative : {dfs_it:+.10f}")

    assert abs(dfs_rec - bfs) < 1e-12, "DFS ≠ BFS!"
    assert abs(dfs_rec - dfs_it) < 1e-12, "Recursive ≠ Iterative!"

    print("\nAll methods agree — PASSED!")

    print("\nMathematical verification:")
    print(f"  Level 0: +1/{n} = +{1/n:.6f}")
    print(f"  Level 1: -{n}/{n*n} = -{n/(n*n):.6f} × {n} = -{1/n:.6f}")
    print(f"  Level 2: +{n*n}/{n*n*n} = +{1/n:.6f}")
    print(f"  Level 3: -{n*n*n}/{n*n*n*n} = -{1/n:.6f}")
    print(f"  Total: +{1/n} − {1/n} + {1/n} − {1/n} = 0.0")

    
    print("\nWhy DFS ≠ BFS in traversal order?")
    print("DFS: goes deep into one branch before siblings")
    print("BFS: visits all nodes at depth d before depth d+1")
    print("But for SUM with alternating signs — order doesn't matter!")



if __name__ == "__main__":
    main()
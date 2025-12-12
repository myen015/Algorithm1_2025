easy = ['find max', 'linear search', 'shortest path', 'matrix multiplicaton', 
        'sorting', 'dijkstra', 'bfs', 'dfs', 'merge sort', 'quicksort']

hard = ['sudoku', '3 coloring', 'scheduling', 'traveling salesman', 
        'hamiltonian cycle', 'clique']

very_hard = ['traveling salesman', 'hamiltonian cycle', 'clique', 
             'cryptography', 'factoring integers']

imposible = ['halting problem', 'busy beaver']

print("klasifikaciya zadach")
print("="*40)

print("\n1. legkie zadachi (class p):")
for task in easy:
    print(f"   - {task}")

print("\n2. trudnie zadachi (np-complete):")
for task in hard:
    print(f"   - {task}")

print("\n3. ochen trudnie (np-hard):")
for task in very_hard:
    print(f"   - {task}")

print("\n4. nevozmozhnie zadachi:")
for task in imposible:
    print(f"   - {task}")

print("\n" + "="*40)
print("vivod:")
print("p - mozhno reshit bistro")
print("np - mozhno proverit bistro")
print("np-complete - samie slozhnie v np")
print("np-hard - eshe slozhnee")
print("undecidable - voobshe nelzya reshit")

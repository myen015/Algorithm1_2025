def dfs(node, graph, visited, stack):
    visited[node] = True
    
    if node in graph:
        for neighbor in graph[node]:
            if neighbor not in visited or not visited[neighbor]:
                dfs(neighbor, graph, visited, stack)
    
    stack.append(node)


def topological_sort(graph, start_node):
    visited = {}
    stack = []
    
    for node in graph:
        visited[node] = False
    
    dfs(start_node, graph, visited, stack)
    
    for node in graph:
        if not visited[node]:
            dfs(node, graph, visited, stack)
    
    stack.reverse()
    return stack


def start():
    graph = {
        'A': ['B', 'C'],
        'B': ['C', 'D'],
        'C': ['E'],
        'D': ['E', 'F'],
        'E': [],
        'F': [],
        'G': ['F', 'E']
    }
    
    print("graph:")
    for node in graph:
        print(f"{node} -> {graph[node]}")
    
    print("\n" + "="*50)
    print("topological sort start from A")
    order = topological_sort(graph, 'A')
    print(" -> ".join(order))
    
    print("\n" + "="*50)
    print("topological sort start from G")
    order = topological_sort(graph, 'G')
    print(" -> ".join(order))
    
    print("\n" + "="*50)
    print("topological sort start from B")
    order = topological_sort(graph, 'B')
    print(" -> ".join(order))


start()

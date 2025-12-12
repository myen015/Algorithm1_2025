def reverse_graph(graph):
    result = {}
    
    for node in graph:
        result[node] = []
    
    for node in graph:
        for neighbor in graph[node]:
            result[neighbor].append(node)
    
    return result


def start():
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': []
    }
    
    print("Original graph:")
    for node in graph:
        print(f"{node} -> {graph[node]}")
    
    reversed_graph = reverse_graph(graph)
    
    print("\nReversed graph:")
    for node in reversed_graph:
        print(f"{node} -> {reversed_graph[node]}")


start()

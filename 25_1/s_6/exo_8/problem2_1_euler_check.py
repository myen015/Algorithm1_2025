def count_degrees(graph):
    in_degree = {}
    out_degree = {}
    
    for node in graph:
        out_degree[node] = len(graph[node])
        in_degree[node] = 0
    
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    return in_degree, out_degree


def has_euler_tour(graph):
    in_deg, out_deg = count_degrees(graph)
    
    for node in graph:
        if in_deg[node] != out_deg[node]:
            return False
    return True


def start():
    graph1 = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A']
    }
    
    graph2 = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['A']
    }
    
    print("graph 1")
    for node in graph1:
        print(f"{node} -> {graph1[node]}")
    
    in_deg, out_deg = count_degrees(graph1)
    print("\ndegrees:")
    for node in graph1:
        print(f"{node}: in={in_deg[node]}, out={out_deg[node]}")
    
    if has_euler_tour(graph1):
        print("has euler")
    else:
        print("no Euler")
    
    print("\n" + "="*40)
    print("\ngraph 2")
    for node in graph2:
        print(f"{node} -> {graph2[node]}")
    
    in_deg, out_deg = count_degrees(graph2)
    print("\ndegrees:")
    for node in graph2:
        print(f"{node}: in={in_deg[node]}, out={out_deg[node]}")
    
    if has_euler_tour(graph2):
        print("has euler")
    else:
        print("no euler")


start()

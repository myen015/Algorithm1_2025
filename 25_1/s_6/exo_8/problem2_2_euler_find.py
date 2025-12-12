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


def find_cycle(start, graph, used):
    cycle = []
    stack = [start]
    current = start
    
    while True:
        found = False
        if current in graph:
            for i in range(len(graph[current])):
                neighbor = graph[current][i]
                edge = (current, neighbor, i)
                if edge not in used:
                    used.add(edge)
                    cycle.append(current)
                    current = neighbor
                    found = True
                    break
        
        if not found:
            if current == start and len(cycle) > 0:
                cycle.append(current)
                return cycle
            return []
    
    return cycle


def find_euler_tour(graph):
    if not has_euler_tour(graph):
        return None
    
    start = list(graph.keys())[0]
    used = set()
    tour = []
    stack = [start]
    current = start
    
    while stack:
        if current in graph:
            found = False
            for i in range(len(graph[current])):
                neighbor = graph[current][i]
                edge = (current, neighbor, i)
                if edge not in used:
                    used.add(edge)
                    stack.append(current)
                    current = neighbor
                    found = True
                    break
            if not found:
                tour.append(current)
                current = stack.pop()
        else:
            tour.append(current)
            current = stack.pop()
    
    tour.reverse()
    return tour


def start():
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['D'],
        'D': ['A']
    }
    
    print("graph:")
    for node in graph:
        print(f"{node} -> {graph[node]}")
    
    in_deg, out_deg = count_degrees(graph)
    print("\ndegrees:")
    for node in graph:
        print(f"{node}: in={in_deg[node]}, out={out_deg[node]}")
    
    tour = find_euler_tour(graph)
    
    if tour:
        print("\neuler tour found")
        for i in range(len(tour)):
            if i < len(tour) - 1:
                print(f"{tour[i]} -> ", end="")
            else:
                print(tour[i])
    else:
        print("\nno euler tour exists")


start()

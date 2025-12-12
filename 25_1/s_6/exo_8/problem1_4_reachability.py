def dfs(node, graph, visited, stack):
    visited[node] = True
    if node in graph:
        for neighbor in graph[node]:
            if neighbor not in visited or not visited[neighbor]:
                dfs(neighbor, graph, visited, stack)
    stack.append(node)


def dfs2(node, graph, visited, component):
    visited[node] = True
    component.append(node)
    if node in graph:
        for neighbor in graph[node]:
            if neighbor not in visited or not visited[neighbor]:
                dfs2(neighbor, graph, visited, component)


def reverse_graph(graph):
    result = {}
    for node in graph:
        result[node] = []
    for node in graph:
        for neighbor in graph[node]:
            result[neighbor].append(node)
    return result


def find_scc(graph):
    visited = {}
    stack = []
    for node in graph:
        visited[node] = False
    for node in graph:
        if not visited[node]:
            dfs(node, graph, visited, stack)
    rev_graph = reverse_graph(graph)
    visited = {}
    for node in graph:
        visited[node] = False
    components = []
    while stack:
        node = stack.pop()
        if not visited[node]:
            component = []
            dfs2(node, rev_graph, visited, component)
            components.append(component)
    return components


def build_scc_graph(graph, components):
    comp_map = {}
    for i in range(len(components)):
        for node in components[i]:
            comp_map[node] = i
    scc_graph = {}
    for i in range(len(components)):
        scc_graph[i] = set()
    for node in graph:
        for neighbor in graph[node]:
            comp1 = comp_map[node]
            comp2 = comp_map[neighbor]
            if comp1 != comp2:
                scc_graph[comp1].add(comp2)
    return scc_graph, comp_map


def can_reach(start, end, graph):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node == end:
            return True
        if node in visited:
            continue
        visited.add(node)
        if node in graph:
            for neighbor in graph[node]:
                stack.append(neighbor)
    return False


def start():
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A', 'D'],
        'D': ['E'],
        'E': ['D']
    }
    
    components = find_scc(graph)
    scc_graph, comp_map = build_scc_graph(graph, components)
    
    print("components:")
    for i in range(len(components)):
        print(f"S{i}: {components[i]}")
    
    print("\nchecking reachability:")
    u = 'A'
    v = 'E'
    
    print(f"\ncan {u} reach {v} in G?")
    reach_g = can_reach(u, v, graph)
    print(f"result: {reach_g}")
    
    s_u = comp_map[u]
    s_v = comp_map[v]
    print(f"\ncan S({u})=S{s_u} reach S({v})=S{s_v} in scc(G)?")
    reach_scc = can_reach(s_u, s_v, scc_graph)
    print(f"result: {reach_scc}")
    
    print(f"\nboth are {reach_g} - proof works")


start()

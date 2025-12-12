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
    return scc_graph


def start():
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A', 'D'],
        'D': ['E'],
        'E': ['D']
    }
    
    print("original graph G:")
    for node in graph:
        print(f"{node} -> {graph[node]}")
    
    components_g = find_scc(graph)
    scc_g = build_scc_graph(graph, components_g)
    
    print("\nscc(G):")
    for node in scc_g:
        print(f"{node} -> {list(scc_g[node])}")
    
    rev_graph = reverse_graph(graph)
    print("\nreversed graph rev(G):")
    for node in rev_graph:
        print(f"{node} -> {rev_graph[node]}")
    
    components_rev = find_scc(rev_graph)
    scc_rev = build_scc_graph(rev_graph, components_rev)
    
    print("\nscc(rev(G)):")
    for node in scc_rev:
        print(f"{node} -> {list(scc_rev[node])}")
    
    rev_scc = {}
    for node in scc_g:
        rev_scc[node] = set()
    for node in scc_g:
        for neighbor in scc_g[node]:
            rev_scc[neighbor].add(node)
    
    print("\nrev(scc(G)):")
    for node in rev_scc:
        print(f"{node} -> {list(rev_scc[node])}")
    
    print("\nthey are the same")


start()

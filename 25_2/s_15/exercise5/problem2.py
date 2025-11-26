def csc_to_adj(col_pointers, row_indices, n, directed=True):
    adj = [[0 for _ in range(n)] for _ in range(n)]
    for j in range(n):
        start = col_pointers[j]
        end = col_pointers[j + 1]
        for k in range(start, end):
            i = row_indices[k]
            adj[i][j] = 1
            if not directed:
                adj[j][i] = 1
    return adj

def print_matrix(mat, labels=None):
    n = len(mat)
    if labels is None:
        labels = [str(i) for i in range(n)]
    print("   " + " ".join(labels))
    for i in range(n):
        row_str = " ".join(str(x) for x in mat[i])
        print(labels[i], row_str)

vertices = ["A", "B", "C", "D", "E"]
n = 5

col_pointers_1 = [0, 2, 5, 8, 11, 12]
row_indices_1 = [1, 2, 0, 2, 3, 0, 1, 3, 1, 2, 4, 3]

adj1 = csc_to_adj(col_pointers_1, row_indices_1, n, directed=False)
print("Graph 1 (undirected) adjacency matrix:")
print_matrix(adj1, vertices)
print()

col_pointers_2 = [0, 0, 2, 4, 5, 7]
row_indices_2 = [0, 3, 0, 1, 2, 1, 3]

adj2 = csc_to_adj(col_pointers_2, row_indices_2, n, directed=True)
print("Graph 2 (directed) adjacency matrix:")
print_matrix(adj2, vertices)
print()
print("Unique directed cycle in Graph 2: B -> C -> D -> B")

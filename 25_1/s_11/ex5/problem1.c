#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// ----- Graph structure using adjacency matrix -----
typedef struct
{
    int V;     // number of vertices
    int **adj; // adjacency matrix
} Graph;

// Create graph with V vertices
Graph *createGraph(int V)
{
    Graph *graph = (Graph *)malloc(sizeof(Graph));
    graph->V = V;

    graph->adj = (int **)malloc(V * sizeof(int *));
    for (int i = 0; i < V; i++)
    {
        graph->adj[i] = (int *)calloc(V, sizeof(int));
    }

    return graph;
}

// Add undirected edge
void addEdge(Graph *graph, int v, int w)
{
    graph->adj[v][w] = 1;
    graph->adj[w][v] = 1;
}

// Print adjacency matrix
void printAdjMatrix(Graph *graph)
{
    printf("\nAdjacency Matrix (%d x %d):\n", graph->V, graph->V);

    for (int i = 0; i < graph->V; i++)
    {
        for (int j = 0; j < graph->V; j++)
        {
            printf("%d ", graph->adj[i][j]);
        }
        printf("\n");
    }

    printf("\n");
}

// DFS to detect cycle
bool isCyclicUtil(Graph *graph, int v, bool visited[], int parent)
{
    visited[v] = true;

    for (int u = 0; u < graph->V; u++)
    {
        if (graph->adj[v][u] == 1)
        {

            if (!visited[u])
            {
                if (isCyclicUtil(graph, u, visited, v))
                    return true;
            }
            else if (u != parent)
            {
                return true; // found a cycle
            }
        }
    }

    return false;
}

// Check if graph is a tree
bool isTree(Graph *graph)
{
    bool *visited = (bool *)calloc(graph->V, sizeof(bool));

    // 1. Check cycle
    if (isCyclicUtil(graph, 0, visited, -1))
        return false;

    // 2. Check connectivity
    for (int i = 0; i < graph->V; i++)
    {
        if (!visited[i])
            return false;
    }

    return true;
}

// ---------- MAIN ----------
int main()
{

    // First graph (Tree)
    Graph *g1 = createGraph(5);
    addEdge(g1, 1, 0);
    addEdge(g1, 0, 2);
    addEdge(g1, 0, 3);
    addEdge(g1, 3, 4);

    printf("Graph 1:\n");
    printAdjMatrix(g1);

    if (isTree(g1))
        printf("Graph 1 is a Tree\n");
    else
        printf("Graph 1 is NOT a Tree\n");

    // Second graph (NOT a Tree because it has a cycle)
    Graph *g2 = createGraph(5);
    addEdge(g2, 1, 0);
    addEdge(g2, 0, 2);
    addEdge(g2, 2, 1); // creates cycle
    addEdge(g2, 0, 3);
    addEdge(g2, 3, 4);

    printf("\nGraph 2:\n");
    printAdjMatrix(g2);

    if (isTree(g2))
        printf("Graph 2 is a Tree\n");
    else
        printf("Graph 2 is NOT a Tree\n");

    return 0;
}

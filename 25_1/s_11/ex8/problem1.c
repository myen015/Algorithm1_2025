#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct AdjListNode
{
    int dest;
    struct AdjListNode *next;
} AdjListNode;

typedef struct AdjList
{
    AdjListNode *head;
} AdjList;

typedef struct Graph
{
    int V;
    AdjList *array;
} Graph;

AdjListNode *newAdjListNode(int dest)
{
    AdjListNode *newNode = (AdjListNode *)malloc(sizeof(AdjListNode));
    newNode->dest = dest;
    newNode->next = NULL;
    return newNode;
}

Graph *createGraph(int V)
{
    Graph *graph = (Graph *)malloc(sizeof(Graph));
    graph->V = V;
    graph->array = (AdjList *)malloc(V * sizeof(AdjList));
    for (int i = 0; i < V; ++i)
    {
        graph->array[i].head = NULL;
    }
    return graph;
}

void addEdge(Graph *graph, int src, int dest)
{
    AdjListNode *newNode = newAdjListNode(dest);
    newNode->next = graph->array[src].head;
    graph->array[src].head = newNode;
}

Graph *getTranspose(Graph *graph)
{
    int V = graph->V;
    Graph *transpose = createGraph(V);

    for (int v = 0; v < V; v++)
    {
        AdjListNode *pCrawl = graph->array[v].head;
        while (pCrawl)
        {

            addEdge(transpose, pCrawl->dest, v);
            pCrawl = pCrawl->next;
        }
    }
    return transpose;
}

void DFSUtil(int v, bool visited[], struct Graph *graph)
{
    visited[v] = true;
    printf("%d ", v);

    AdjListNode *i = graph->array[v].head;
    for (; i != NULL; i = i->next)
    {
        if (!visited[i->dest])
        {
            DFSUtil(i->dest, visited, graph);
        }
    }
}

void fillOrder(int v, bool visited[], struct Graph *graph, int *stack, int *stackIndex)
{
    visited[v] = true;

    AdjListNode *i = graph->array[v].head;
    for (; i != NULL; i = i->next)
    {
        if (!visited[i->dest])
        {
            fillOrder(i->dest, visited, graph, stack, stackIndex);
        }
    }

    stack[(*stackIndex)++] = v;
}

void printSCCs(Graph *graph)
{
    int V = graph->V;
    int *stack = (int *)malloc(V * sizeof(int));
    int stackIndex = 0;
    bool *visited = (bool *)calloc(V, sizeof(bool));

    for (int i = 0; i < V; i++)
    {
        if (!visited[i])
        {
            fillOrder(i, visited, graph, stack, &stackIndex);
        }
    }

    Graph *gr = getTranspose(graph);

    for (int i = 0; i < V; i++)
    {
        visited[i] = false;
    }

    printf("\nStrongly Connected Components are:\n");
    while (stackIndex > 0)
    {

        int v = stack[--stackIndex];

        if (!visited[v])
        {
            printf("SCC: ");
            DFSUtil(v, visited, gr);
            printf("\n");
        }
    }

    free(stack);
    free(visited);
}

int main()
{

    /* Example Graph from SCC algorithms:
       5 vertices, 0 to 4
       1 -> 0 -> 2
       ^    |
       |    v
       4 <- 3
       2 -> 3
    */
    int V = 5;
    Graph *g = createGraph(V);

    addEdge(g, 1, 0);
    addEdge(g, 0, 2);
    addEdge(g, 2, 3);
    addEdge(g, 3, 4);
    addEdge(g, 4, 0);

    /* Example 2:
       0 -> 1 -> 2 -> 0
       3 -> 4 -> 5 -> 3
       2 -> 3
       SCCs: {0, 1, 2}, {3, 4, 5}
    */
    V = 6;
    Graph *g2 = createGraph(V);

    addEdge(g2, 0, 1);
    addEdge(g2, 1, 2);
    addEdge(g2, 2, 0);
    addEdge(g2, 3, 4);
    addEdge(g2, 4, 5);
    addEdge(g2, 5, 3);
    addEdge(g2, 2, 3);

    printf("Running Kosaraju's Algorithm on Example Graph (Vertices 0-5):\n");
    printSCCs(g2);

    return 0;
}
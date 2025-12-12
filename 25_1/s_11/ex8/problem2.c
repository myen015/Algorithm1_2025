#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_VERTICES 100
#define MAX_EDGES 200

typedef struct
{
    int neighbor;
    bool used;
} Edge;

typedef struct
{
    Edge edges[MAX_EDGES];
    int count;
    int nextEdge;
} VertexAdj;

VertexAdj adj[MAX_VERTICES];
int in_degree[MAX_VERTICES] = {0};
int out_degree[MAX_VERTICES] = {0};
int V_count = 0;
int E_count = 0;

int tour[MAX_EDGES + 1];
int tourIndex = 0;

void addEdge_Euler(int u, int v)
{
    if (u >= V_count)
        V_count = u + 1;
    if (v >= V_count)
        V_count = v + 1;

    if (adj[u].count < MAX_EDGES)
    {
        adj[u].edges[adj[u].count].neighbor = v;
        adj[u].edges[adj[u].count].used = false;
        adj[u].count++;
        out_degree[u]++;
        in_degree[v]++;
        E_count++;
    }
}

bool checkEulerCondition()
{
    for (int i = 0; i < V_count; i++)
    {

        if (in_degree[i] != out_degree[i])
        {
            printf("Vertex %d fails condition: in-degree(%d) = %d, out-degree(%d) = %d\n",
                   i, i, in_degree[i], i, out_degree[i]);
            return false;
        }
    }
    return true;
}

void findEulerTour(int u)
{

    while (adj[u].nextEdge < adj[u].count)
    {
        Edge *currentEdge = &adj[u].edges[adj[u].nextEdge];

        if (currentEdge->used)
        {
            adj[u].nextEdge++;
            continue;
        }

        currentEdge->used = true;
        int v = currentEdge->neighbor;
        adj[u].nextEdge++;

        findEulerTour(v);
    }

    tour[tourIndex++] = u;
}

int main()
{

    addEdge_Euler(0, 1);
    addEdge_Euler(1, 2);
    addEdge_Euler(2, 0);
    addEdge_Euler(2, 3);
    addEdge_Euler(3, 2);

    printf("--- Euler Tour Problem ---\n");
    printf("Checking Euler Tour Condition (in-degree = out-degree):\n");

    if (checkEulerCondition())
    {
        printf("Condition satisfied. An Euler Tour exists (O(E) time)[cite: 9, 10].\n");

        findEulerTour(0);

        printf("Euler Tour: ");

        for (int i = tourIndex - 1; i >= 0; i--)
        {
            printf("%d%s", tour[i], (i == 0) ? "" : " -> ");
        }
        printf("\n");
    }
    else
    {
        printf("Condition failed. No Euler Tour exists.\n");
    }

    return 0;
}
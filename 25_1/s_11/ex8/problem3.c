#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define NUM_COURSES 7

int charToInt(char c)
{
    if (c >= 'A' && c <= 'G')
        return c - 'A';
    return -1;
}

typedef struct
{
    int adj[NUM_COURSES][NUM_COURSES];
    int V;
} CourseGraph;

typedef struct
{
    int items[NUM_COURSES];
    int front, rear;
} Queue;

void initQueue(Queue *q)
{
    q->front = -1;
    q->rear = -1;
}
void enqueue(Queue *q, int item)
{
    if (q->rear == NUM_COURSES - 1)
        return;
    if (q->front == -1)
        q->front = 0;
    q->rear++;
    q->items[q->rear] = item;
}
int dequeue(Queue *q)
{
    if (q->front == -1 || q->front > q->rear)
        return -1;
    int item = q->items[q->front];
    q->front++;
    return item;
}

/**
 * Perform Topological Sort on the course graph using Kahn's Algorithm.
 */
void topologicalSort(CourseGraph *graph)
{
    int V = graph->V;
    int in_degree[NUM_COURSES] = {0};
    int top_order[NUM_COURSES];
    int order_index = 0;
    Queue q;
    initQueue(&q);

    for (int u = 0; u < V; u++)
    {
        for (int v = 0; v < V; v++)
        {
            if (graph->adj[u][v] == 1)
            {
                in_degree[v]++;
            }
        }
    }

    for (int i = 0; i < V; i++)
    {
        if (in_degree[i] == 0)
        {
            enqueue(&q, i);
        }
    }

    while (q.front != -1 && q.front <= q.rear)
    {
        int u = dequeue(&q);
        top_order[order_index++] = u;

        for (int v = 0; v < V; v++)
        {
            if (graph->adj[u][v] == 1)
            {
                in_degree[v]--;

                if (in_degree[v] == 0)
                {
                    enqueue(&q, v);
                }
            }
        }
    }

    if (order_index != V)
    {
        printf("Error: The graph contains a cycle (not a valid course dependency).");
        return;
    }

    printf("One Topological Sort Order:\n");
    for (int i = 0; i < V; i++)
    {
        printf("%c ", (char)('A' + top_order[i]));
    }
    printf("\n");
}

int main()
{

    CourseGraph graph;
    graph.V = NUM_COURSES;
    for (int i = 0; i < NUM_COURSES; i++)
        for (int j = 0; j < NUM_COURSES; j++)
            graph.adj[i][j] = 0;

    graph.adj[charToInt('A')][charToInt('B')] = 1;
    graph.adj[charToInt('A')][charToInt('C')] = 1;
    graph.adj[charToInt('B')][charToInt('C')] = 1;
    graph.adj[charToInt('B')][charToInt('D')] = 1;
    graph.adj[charToInt('C')][charToInt('E')] = 1;
    graph.adj[charToInt('D')][charToInt('E')] = 1;
    graph.adj[charToInt('D')][charToInt('F')] = 1;
    graph.adj[charToInt('G')][charToInt('F')] = 1;
    graph.adj[charToInt('G')][charToInt('E')] = 1;

    printf("Topological Sort on Course Dependencies:\n");
    topologicalSort(&graph);

    printf("\nTwo possible sortings (by choosing different 0-degree nodes):\n");
    printf("Sorting 1 (A before G, B before D, etc.): A B C D G E F\n");
    printf("Sorting 2 (G before A, B before D, etc.): G A B D C E F\n");

    return 0;
}
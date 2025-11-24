#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/*
 * Node of an N-ary tree.
 * Every node has:
 *  - weight
 *  - depth level
 *  - number of children N
 *  - array of children pointers
 */
typedef struct Node
{
    double weight;
    int depth;
    int N;
    struct Node **children;
} Node;

/*
 * This function creates a whole N-ary tree up to some depth.
 * Each new node divides the parent weight by N.
 */
Node *generate_tree(int N, int max_depth, int current_depth, double parent_weight)
{
    Node *node = (Node *)malloc(sizeof(Node));
    if (!node)
    {
        printf("Error: cannot allocate node\n");
        exit(1);
    }

    node->weight = parent_weight / N;
    node->depth = current_depth;
    node->N = N;

    // If we still haven't reached the bottom, make children
    if (current_depth < max_depth - 1)
    {
        node->children = (Node **)malloc(N * sizeof(Node *));
        if (!node->children)
        {
            printf("Error allocating children array\n");
            free(node);
            exit(1);
        }

        for (int i = 0; i < N; i++)
        {
            node->children[i] = generate_tree(N, max_depth, current_depth + 1, node->weight);
        }
    }
    else
    {
        node->children = NULL; // leaf node
    }

    return node;
}

/*
 * Free all nodes recursively
 */
void free_tree(Node *node)
{
    if (!node)
        return;

    if (node->children)
    {
        for (int i = 0; i < node->N; i++)
        {
            free_tree(node->children[i]);
        }
        free(node->children);
    }

    free(node);
}

/*
 * Simple DFS: just add all weights
 */
double depth_first_sum_recursive(Node *node)
{
    if (!node)
        return 0.0;

    double sum = node->weight;

    if (node->children)
    {
        for (int i = 0; i < node->N; i++)
        {
            sum += depth_first_sum_recursive(node->children[i]);
        }
    }

    return sum;
}

/*
 * DFS but the sign flips every level (even = +, odd = -)
 */
double depth_first_signed_sum_recursive(Node *node, int negative)
{
    if (!node)
        return 0.0;

    double w = negative ? -node->weight : node->weight;
    double sum = w;

    int next_negative = !negative;

    if (node->children)
    {
        for (int i = 0; i < node->N; i++)
        {
            sum += depth_first_signed_sum_recursive(node->children[i], next_negative);
        }
    }
    return sum;
}

/*
 * Basic queue used for BFS
 */
typedef struct Queue
{
    Node **array;
    int front, rear, count, capacity;
} Queue;

Queue *create_queue(int cap)
{
    Queue *q = (Queue *)malloc(sizeof(Queue));
    q->capacity = cap;
    q->front = 0;
    q->rear = -1;
    q->count = 0;

    q->array = (Node **)malloc(cap * sizeof(Node *));
    return q;
}

void enqueue(Queue *q, Node *node)
{
    if (q->count == q->capacity)
    {
        q->capacity *= 2;
        q->array = (Node **)realloc(q->array, q->capacity * sizeof(Node *));
    }
    q->rear = (q->rear + 1) % q->capacity;
    q->array[q->rear] = node;
    q->count++;
}

Node *dequeue(Queue *q)
{
    if (q->count == 0)
        return NULL;

    Node *node = q->array[q->front];
    q->front = (q->front + 1) % q->capacity;
    q->count--;
    return node;
}

void free_queue(Queue *q)
{
    free(q->array);
    free(q);
}

/*
 * BFS but non-recursive: just sum all weights
 */
double breadth_first_sum_non_recursive(Node *root)
{
    if (!root)
        return 0.0;

    double sum = 0;
    int max_nodes = root->N * root->N * root->N + root->N + 1;
    Queue *q = create_queue(max_nodes);

    enqueue(q, root);

    while (q->count > 0)
    {
        Node *node = dequeue(q);
        sum += node->weight;

        if (node->children)
        {
            for (int i = 0; i < node->N; i++)
            {
                enqueue(q, node->children[i]);
            }
        }
    }

    free_queue(q);
    return sum;
}

/*
 * BFS signed version (depth decides the sign)
 */
double breadth_first_signed_sum_non_recursive(Node *root)
{
    if (!root)
        return 0.0;

    double sum = 0;
    int max_nodes = root->N * root->N * root->N + root->N + 1;

    Queue *q = create_queue(max_nodes);
    enqueue(q, root);

    while (q->count > 0)
    {
        Node *node = dequeue(q);

        int sign = (node->depth % 2 == 0) ? 1 : -1;
        sum += sign * node->weight;

        if (node->children)
        {
            for (int i = 0; i < node->N; i++)
            {
                enqueue(q, node->children[i]);
            }
        }
    }

    free_queue(q);
    return sum;
}

/*
 * Just tests to see if calculations work
 */
void run_tests()
{
    int N = 4;
    int DEPTH = 3;

    printf("--- Testing N=%d, Depth=%d ---\n", N, DEPTH);

    Node *tree = generate_tree(N, DEPTH, 0, 1.0);

    double expected = (double)DEPTH / N;

    double dfs = depth_first_sum_recursive(tree);
    double bfs = breadth_first_sum_non_recursive(tree);

    printf("Unsigned expected = %.4f\n", expected);
    printf("DFS = %.4f\n", dfs);
    printf("BFS = %.4f\n", bfs);

    double signed_expected = 1.0 / N;
    double dfs_s = depth_first_signed_sum_recursive(tree, 0);
    double bfs_s = breadth_first_signed_sum_non_recursive(tree);

    printf("\nSigned expected = %.4f\n", signed_expected);
    printf("DFS signed = %.4f\n", dfs_s);
    printf("BFS signed = %.4f\n", bfs_s);

    free_tree(tree);
}

int main()
{
    run_tests();
    return 0;
}

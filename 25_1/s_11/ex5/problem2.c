/// Computer Science
/// Student Number is 11

#include <stdio.h>
#include <string.h>

#define N 5 // number of vertices A,B,C,D,E

void buildAdjMatrix(int n, int col_ptr[], int row_idx[], int directed, int adj[][N])
{
    // initialize the matrix with zeros
    memset(adj, 0, sizeof(int) * N * N);

    // reconstruct from CSC
    for (int col = 0; col < n; col++)
    {
        int start = col_ptr[col];
        int end = col_ptr[col + 1];

        for (int k = start; k < end; k++)
        {
            int row = row_idx[k];
            adj[row][col] = 1; // edge row -> col

            if (!directed)
            {
                adj[col][row] = 1; // make symmetric for undirected graph
            }
        }
    }
}

void printMatrix(int n, int adj[][N])
{
    printf("    A B C D E\n");
    for (int i = 0; i < n; i++)
    {
        printf("%c [ ", 'A' + i);
        for (int j = 0; j < n; j++)
        {
            printf("%d ", adj[i][j]);
        }
        printf("]\n");
    }
    printf("\n");
}

int main()
{

    // -----------------------------
    // Graph 1 (undirected)
    // -----------------------------
    int col1[] = {0, 2, 5, 8, 11, 12};
    int row1[] = {1, 2, 0, 2, 3, 0, 1, 3, 1, 2, 4, 3};

    int adj1[N][N];
    buildAdjMatrix(N, col1, row1, 0, adj1);

    printf("Adjacency Matrix: Graph 1 (Undirected)\n");
    printMatrix(N, adj1);

    // -----------------------------
    // Graph 2 (directed)
    // -----------------------------
    int col2[] = {0, 0, 2, 4, 5, 7};
    int row2[] = {0, 3, 0, 1, 2, 1, 3};

    int adj2[N][N];
    buildAdjMatrix(N, col2, row2, 1, adj2);

    printf("Adjacency Matrix: Graph 2 (Directed)\n");
    printMatrix(N, adj2);

    return 0;
}

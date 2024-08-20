#include "t2.h"
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

// helper function to allocate memory for adjacency matrix
int** allocatematrix(int rows, int cols) {
    int** matrix = (int**)malloc(rows * sizeof(int*));              // alloc mem for rows
    for (int i = 0; i < rows; ++i) {                                // iterate through rows
        matrix[i] = (int*)calloc(cols, sizeof(int));                // alloc mem for each column in row
    }
    return matrix;
}

// creates graph with num_nodes nodes
Graph* create_graph(int num_nodes) {
    Graph* graph = (Graph*)malloc(sizeof(graph));                   // alloc mem for graph structure
    graph->num_nodes = num_nodes;                                   // set number of nodes in graph
    graph->adjacency_matrix = allocatematrix(num_nodes, num_nodes); // alloc mem for adjacency matrix
    return graph;
}

// add an edge between two nodes
void add_edge(Graph *g, int from, int to, int weight) {
    if (from >= 0 && from < g->num_nodes && to >= 0 && to < g->num_nodes) { // if nodes are within range
        g->adjacency_matrix[from][to] = weight;                             // set weight for edge from 'from' to 'to'
        g->adjacency_matrix[to][from] = weight;                             // set weight for edge from 'to' to 'from'
    }
}

// helper function to find next node with the minimum distance
int minDistance(int* distances, int* visited, int num_nodes) { 
    int min = INT_MAX, min_index = -1;                              // init minimum distance and its index
    for (int i = 0; i < num_nodes; ++i) {                           // iterate through nodes
        if (visited[i] == 0 && distances[i] <= min) {               // if node is unvisited and has a smaller distance
            min = distances[i];                                     // update minimum distance
            min_index = i;                                          // update index of node with minimum distance
        }
    }
    return min_index;
}

// preform Dijkstra's algorithm
void dijkstra(Graph* g, int origin) {
    int num_nodes = g->num_nodes;                                   // get number of nodes in graph
    int* distances = (int*)malloc(num_nodes * sizeof(int));         // alloc mem for distances from origin
    int* visited = (int*)calloc(num_nodes, sizeof(int));            // alloc mem to track visited nodes
    char* nodes_order = (char*)malloc(num_nodes * sizeof(char));    // alloc mem for nodes in order of traversal
    int nodes_order_index = 0;                                      // init index for nodes_order array

    for (int i = 0; i < num_nodes; ++i) {                           // iterate through nodes
        distances[i] = INT_MAX;                                     // set initial distances to infinity(INT_MAX)
    }

    distances[origin] = 0;                                          // set distance of origin node to itself as 0

    for (int count = 0; count < num_nodes; ++count) {               // iterate through all nodes
        int u = minDistance(distances, visited, num_nodes);         // find next node with minimum distance
        visited[u] = 1;                                             // mark node as visited
        nodes_order[nodes_order_index++] = u + 'A';                 // store node's label in traversal order

        for (int v = 0; v < num_nodes; ++v) {                       // iterate through neighboring nodes
            if (!visited[v] && g->adjacency_matrix[u][v] && distances[u] != INT_MAX && distances[u] + g->adjacency_matrix[u][v] < distances[v]) {
                distances[v] = distances[u] + g->adjacency_matrix[u][v]; // update distance to v
            }
        }
    }

    for (int i = 0; i < nodes_order_index; ++i) {                   // iterate through nodes_order array
        printf("%c ", nodes_order[i]);                              // print order of traversal
    }
    printf("\n");

    for (int i = 0; i < num_nodes; ++i) {                           // iterate through all nodes
         printf("The length of the shortest path between %c and %c is %d\n", origin + 'A', i + 'A', distances[i]);
    }

    free(distances);                                                // free mem for distances array
    free(visited);                                                  // free mem for visited array
    free(nodes_order);                                              // free mem for nodes_order array
}

// deallocate memory for graph and its structures
void delete_graph(Graph* g) {
    for (int i = 0; i < g->num_nodes; ++i) {                        // iterate through each row of adjacency matrix
        free(g->adjacency_matrix[i]);                               // free mem for each row
    }
    free(g->adjacency_matrix);                                      // free mem for entire adjacency matrix
    free(g);                                                        // free mem for graph structure
}

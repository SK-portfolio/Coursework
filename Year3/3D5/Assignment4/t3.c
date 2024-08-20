#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <limits.h>
#include "t3.h"

Vertex* vertices = NULL;                                    // declare pointer-named vertices-type Vertex-initialize to NULL

// helper function to create a new edge
Edge* createEdge(int start, int end, double weight) {
    Edge* newEdge = (Edge*)malloc(sizeof(Edge));            // allocate memory for a new edge struct
    if (newEdge != NULL) {                                  // if memory allocation was successful
        newEdge->startNode = start;                         // assign start node value to newedge's startnode field
        newEdge->endNode = end;                             // assign end node value to newedge's endnode field
        newEdge->weight = weight;                           // assign weight value to newedge's weight field
        newEdge->next = NULL;                               // set next pointer of newedge to NULL (last element for now)
    } else {
        printf("Memory allocation failed for Edge creation.\n");
    }
    return newEdge;                                          // return created edge(/null if mem alloc fail)
}

// helper function to find a vertex in list
Vertex* findVertex(int node) {  
    Vertex* temp = vertices;                                // assign vertices address to temporary pointer
    while (temp != NULL) {                                  // while temp not pointing to null
        if (temp->node == node) {                           // if node value of current vertex equals input node
            return temp;                                    // return current vertex
        }
        temp = temp->next;                                  // move temp pointer to next vertex
    }
    return NULL;
}

int load_edges(char *fname) {
    FILE* file = fopen(fname, "r");
    if (file == NULL) {
        printf("Failed to load edges.csv");
        return 0; // Failed to open file
    }

    int startNode, endNode;                                 // variables to store node indices
    double weight;                                          // variable to store edge weight
    while (fscanf(file, "%d,%d,%lf\n", &startNode, &endNode, &weight) == 3) {   // read three values at a time from file until end of file
        Edge* newEdge = createEdge(startNode, endNode, weight);                 // create new edge with read values
        if (newEdge == NULL) {                                                  // if mem alloc for edge failed
            fclose(file);
            return 0;
        }

        // add the edge to both vertices
        Vertex* startVertex = findVertex(startNode);            // findVertex for startNode
        Vertex* endVertex = findVertex(endNode);                // findVertex for endNode

        if (startVertex != NULL && endVertex != NULL) {         //if both vertices not NULL(/exist)
            newEdge->next = startVertex->edges;                 // link new edge to start vertex's edge list
            startVertex->edges = newEdge;                       // update start vertex's edge list with new edge

            newEdge = createEdge(endNode, startNode, weight);   // create new edge with reversed nodes
            newEdge->next = endVertex->edges;                   // link reversed edge to end vertex's edge list
            endVertex->edges = newEdge;                         // update end vertex's edge list with reversed edge
        }
    }

    fclose(file);
    return 1; // success
}

int load_vertices(char *fname) {                                
    FILE* file = fopen(fname, "r");
    if (file == NULL) {
        printf("Failed to load vertices.csv");
        return 0;
    }

    int node;                                                   // variable to store each vertex/node
    while (fscanf(file, "%d\n", &node) == 1) {                  // read integers from file until end
        Vertex* newVertex = (Vertex*)malloc(sizeof(Vertex));    // allocate memory for new vertex
        if (newVertex == NULL) {                                // if memory allocation failed
            fclose(file); 
            return 0; 
        }
        newVertex->node = node;                                 // store read node value in new vertex
        newVertex->edges = NULL;                                // init edges of new vertex to NULL
        newVertex->next = vertices;                             // point new vertex to current list of vertices
        vertices = newVertex;                                   // update list of vertices to include new vertex
    }

    fclose(file);
    return 1; // success
}

//modified dijkstra from t2.c to use as helper function in shortest_path
void dijkstra(int start, int end) {
    int num_nodes = 0;                                          // init number of nodes to zero
    Vertex* temp = vertices;                                    // set temporary pointer to start of vertices list
    while (temp != NULL) {                                      // while temp exists
        num_nodes++;                                            // increase num of node count by 1
        temp = temp->next;                                      // go to next vertex
    }

    int* distances = (int*)malloc(num_nodes * sizeof(int));     // alloc mem for array to store distances between nodes
    int* visited = (int*)calloc(num_nodes, sizeof(int));        // alloc mem for array to track visited nodes + init to zero
    int* prev = (int*)malloc(num_nodes * sizeof(int));          // alloc mem for array to store previous node in shortest path

    for (int i = 0; i < num_nodes; ++i) {                       
        distances[i] = INT_MAX;                                 // init current distance to maximum value
        prev[i] = -1;                                           // init previous node to -1
    }

    distances[start] = 0;                                       // init starting node distance to 0

    while (1) {
        int u = -1;                                             // init variable to track node with shortest distance
        for (int i = 0; i < num_nodes; ++i) {                   // find unvisited node with shortest distance from start
            if (!visited[i] && (u == -1 || distances[i] < distances[u])) {
                u = i;
            }
        }

        if (u == -1 || u == end) {                              // no node found OR end node reached
            break;
        }

        visited[u] = 1;                                         // mark current node as visited

        Edge* edge = findVertex(u)->edges;                      // traverse edges of current node to update distances
        while (edge != NULL) {
            int v = edge->endNode;
            if (!visited[v] && distances[u] != INT_MAX && distances[u] + edge->weight < distances[v]) {       // if shorter path found  
                distances[v] = distances[u] + edge->weight;     // update distances
                prev[v] = u;
            }
            edge = edge->next;
        }
    }

    if (distances[end] == INT_MAX) {                            //if no path
        printf("No path found from %d to %d\n", start, end);
    } else {                                                    //if path found
        printf("Shortest path from %d to %d: ", start, end);
        int dest = end;
        while (prev[dest] != -1) {                              // while previous destination has been visited 
            printf("%d <- ", dest);                             // print shortest path by following previous nodes
            dest = prev[dest];
        }
        printf("%d\n", start);
    }
                                                                // free allocated array memory
    free(distances);
    free(visited);
    free(prev);
}

void shortest_path(int startNode, int endNode) {
    dijkstra(startNode, endNode);                               // helper dijkstra called
}

void free_memory(void) {
    while (vertices != NULL) {                                  // while vertices still exist
        Vertex* tempVertex = vertices;                          // store current vertex to be freed
        vertices = vertices->next;                              // move to next vertex

        Edge* edge = tempVertex->edges;                         // get edges of current vertex
        while (edge != NULL) {                                  // while edges still exist
            Edge* tempEdge = edge;                              // store current edge to be freed
            edge = edge->next;                                  // move to next edge
            free(tempEdge);                                     // free current edge
        }
        tempVertex->edges = NULL;                               // set edges pointer to null
        free(tempVertex);                                       // free current vertex
    }
}
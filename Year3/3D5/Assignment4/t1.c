#include "t1.h"
#include <stdio.h>
#include <stdlib.h>
// creates graph with given number of nodes
Graph* create_graph(int num_nodes) {                                
    Graph* graph = (Graph*)malloc(sizeof(Graph));                   // alloc mem for graph structure
    graph->num_nodes = num_nodes;                                   // set number of nodes in graph
    graph->adj_list = (Node**)malloc(num_nodes * sizeof(Node*));    // alloc mem for adjacency list
    for (int i = 0; i < num_nodes; ++i) {
        graph->adj_list[i] = NULL;                                  // init adjacency list of each node as empty
    }
    return graph;
}

// creates new node with destination value
Node* create_node(int dest) {                                       
    Node* newNode = (Node*)malloc(sizeof(Node));                    // alloc mem for new node
    newNode->dest = dest;                                           // init destination value for node
    newNode->next = NULL;                                           // init next pointer of node to NULL(end of list)
    return newNode;
}

// add an edge between two nodes in graph
void add_edge(Graph *g, int from, int to) {
    if (from >= g->num_nodes || to >= g->num_nodes) {               // if nodes are within graph's range
        printf("Invalid edge.\n");
        return;
    }
    Node* newNode = create_node(to);                                // create new node with 'to' destination
    newNode->next = g->adj_list[from];                              // point new node to existing adjacency list of 'from'
    g->adj_list[from] = newNode;                                    // update 'from' adjacency list to include new node
}

// perform breadth-first search from origin node
void bfs(Graph* g, int origin) {                                    
    int* visited = (int*)malloc(g->num_nodes * sizeof(int));        // alloc mem to track visited nodes
    for (int i = 0; i < g->num_nodes; ++i) {
        visited[i] = 0;                                             // init visited array to 0(unvisited)
    }

    int* queue = (int*)malloc(g->num_nodes * sizeof(int));          // alloc mem for queue
    int front = 0, rear = 0;                                        // init front and rear of queue

    visited[origin] = 1;                                            // mark origin node as visited
    queue[rear++] = origin;                                         // add origin node to queue
    printf("bfs: ");

    while (front != rear) {
        int current = queue[front++];                               // retrieve and remove node at front of queue
        printf("%c ", current + 'A');                               // print current node

        Node* temp = g->adj_list[current];                          // access adjacency list of current node
        while (temp != NULL) {                                      // iterate through adjacency list
            int adj_node = temp->dest;                              // retrieve destination node from adjacency list
            if (!visited[adj_node]) {                               // if adjacent node is unvisited
                visited[adj_node] = 1;                              // mark adjacent node as visited
                queue[rear++] = adj_node;                           // add adjacent node to queue
            }
            temp = temp->next;                                      // move to next node in list
        }
    }
    printf("\n");

    free(visited);                                                  // free mem for visited array
    free(queue);                                                    // free mem for queue
}

// helper function to perform depth-first search
void helperdfs(Graph* g, int origin, int visited[]) { 
    visited[origin] = 1;                                            // mark current node as visited
    printf("%c ", origin + 'A');                                    // print current node

    Node* temp = g->adj_list[origin];                               // access adjacency list of current node
    while (temp != NULL) {                                          
        int adj_node = temp->dest;                                  // get destination node from adjacency list
        if (!visited[adj_node]) {                                   // if adjacent node is unvisited
            helperdfs(g, adj_node, visited);                        // recursively call for unvisited node
        }
        temp = temp->next;                                          // move to next node in adjacency list
    }
}

// perform depth-first search (DFS)
void dfs(Graph* g, int origin) {
    int* visited = (int*)malloc(g->num_nodes * sizeof(int));        // alloc mem to track visited nodes
    for (int i = 0; i < g->num_nodes; ++i) {                        
        visited[i] = 0;                                             // init visited array to 0(unvisited)
    }

    printf("dfs: ");
    helperdfs(g, origin, visited);                                  // start DFS traversal from specified origin node
    printf("\n");

    free(visited);                                                  // free mem for visited array
}

// delete entire graph and free memory
void delete_graph(Graph* g) { 
    for (int i = 0; i < g->num_nodes; ++i) { 
        Node* current = g->adj_list[i];                             // access adjacency list of current node
        while (current != NULL) {                                   // traverse adjacency list
            Node* temp = current;                                   // store current node temporarily
            current = current->next;                                // move to next node in adjacency list
            free(temp);                                             // free mem for node
        }
    }
    free(g->adj_list);                                              // free mem for array of adjacency lists
    free(g);                                                        // free mem for graph structure
}


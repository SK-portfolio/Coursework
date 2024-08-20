#ifndef T1_H_
#define T1_H_

typedef struct Node {
    int dest;               // destination node
    struct Node* next;      // pointer to next node in linked list
} Node;

typedef struct Graph {
    int num_nodes;          // number of nodes in graph
    Node** adj_list;        // pointer to array of node pointers (adjacency lists)
} Graph;

Graph* create_graph(int num_nodes);
void add_edge(Graph *g, int from, int to);
void bfs(Graph* g, int origin);
void dfs(Graph* g, int origin);
void delete_graph(Graph* g);

#endif

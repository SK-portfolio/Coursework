#ifndef T3_H_
#define T3_H_

typedef struct Edge {
    int startNode;      //start of edge
    int endNode;        //end of edge
    double weight;      // distance in meters
    struct Edge* next;  //next edge in data structure
} Edge;

typedef struct Vertex {
    int node;
    Edge* edges;            // linked list of edges
    struct Vertex* next;    // next vertex in data structure
} Vertex;

int load_edges(char *fname); // loads the edges from the CSV file of name fname
int load_vertices(char *fname); // loads the vertices from the CSV file of name fname
void shortest_path(int startNode, int endNode); // prints the shortest path between startNode and endNode, if there is any
void free_memory(void); // frees any memory that was used

#endif

#ifndef BST_H_
#define BST_H_
typedef struct Tree_Node {
    char data;              // store node info
    int count;              // count of occurrences
    struct Tree_Node* left; // left child
    struct Tree_Node* right;// right child
} Tree_Node;


void tree_insert ( Tree_Node** root, char data );
Tree_Node* create_bst (char data[]);
Tree_Node* tree_search ( Tree_Node* root, char data );
void tree_print_sorted ( Tree_Node* root );
void tree_delete ( Tree_Node* root );


#endif
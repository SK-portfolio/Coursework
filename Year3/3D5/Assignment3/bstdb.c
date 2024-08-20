#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bstdb.h"

//book structure
typedef struct Book {
    int doc_id;
    char *name;
    int word_count;
    struct Book *left;
    struct Book *right;
} Book;

//database structure
typedef struct {
    Book *root;
    int next_doc_id;
} BSTDB;

//database variable
static BSTDB *db = NULL;                                

//helper function - create new book node
Book *createBookNode(char *name, int word_count) {
    Book *newBook = (Book *)malloc(sizeof(Book));       //allocate memory for new book node
    if (newBook == NULL) {
        return NULL;                                    //memory allocation failed
    }

    // Initialize fields
    newBook->doc_id = 0;
    newBook->name = strdup(name);
    newBook->word_count = word_count;
    newBook->left = NULL;
    newBook->right = NULL;

    return newBook;
}

//helper function - recursively insert node into BST
void insertNode(Book *root, Book *newBook) {
    if (newBook->word_count < root->word_count) {
        if (root->left == NULL) {
            root->left = newBook;
        } else {
            insertNode(root->left, newBook);
        }
    } else {
        if (root->right == NULL) {
            root->right = newBook;
        } else {
            insertNode(root->right, newBook);
        }
    }
}

//helper function - recursively search for book by its document ID
Book *searchByID(Book *root, int doc_id) {
    if (root == NULL || root->doc_id == doc_id) {
        return root;
    }

    if (doc_id < root->doc_id) {
        return searchByID(root->left, doc_id);
    } else {
        return searchByID(root->right, doc_id);
    }
}

//helper function - recursively free memory used by BST
void freeBST(Book *root) {
    if (root != NULL) {
        freeBST(root->left);
        freeBST(root->right);
        free(root->name);
        free(root);
    }
}

//helper function - calculate height of BST
int getTreeHeight(Book *root) {
    if (root == NULL) {
        return 0;
    } else {
        int leftHeight = getTreeHeight(root->left);
        int rightHeight = getTreeHeight(root->right);

        return (leftHeight > rightHeight ? leftHeight : rightHeight) + 1;
    }
}

//helper function - check if BST is balanced
int isTreeBalanced(Book *root) {
    if (root == NULL) {
        return 1; // An empty tree is balanced
    }

    int leftHeight = getTreeHeight(root->left);
    int rightHeight = getTreeHeight(root->right);

    return abs(leftHeight - rightHeight) <= 1 && isTreeBalanced(root->left) && isTreeBalanced(root->right);
}

//helper function - count number of stored books
int countBooks(Book *root) {
    if (root == NULL) {
        return 0;
    } else {
        return 1 + countBooks(root->left) + countBooks(root->right);
    }
}

//helper function - count number of nodes visited during search
int countNodesVisited(Book *root, int doc_id) {
    if (root == NULL || root->doc_id == doc_id) {
        return 1; // Count current node
    }

    if (doc_id < root->doc_id) {
        return 1 + countNodesVisited(root->left, doc_id);
    } else {
        return 1 + countNodesVisited(root->right, doc_id);
    }
}

//-------------------------------------------------------------------------------------------

//initialize BST database
int bstdb_init(void) {
    db = (BSTDB *)malloc(sizeof(BSTDB));                    //allocate database memory 
    if (db == NULL) {
        return 0;                                           // Initialization failed
    }

    // Initialize fields
    db->root = NULL;
    db->next_doc_id = 1;

    return 1; // Initialization successful
}

//add new book to BST database
int bstdb_add(char *name, int word_count, char *author) {
    Book *newBook = createBookNode(name, word_count);       //create new book node
    if (newBook == NULL) {
        return 0;                                           //adding book failed
    }

                                                            //assign unique document ID
    newBook->doc_id = db->next_doc_id++;

    
    if (db->root == NULL) {
        db->root = newBook;
    } else {
        insertNode(db->root, newBook);                      //insert new book into BST
    }

    return newBook->doc_id;                                 //return unique document ID
}

//get word count of book using its document ID
int bstdb_get_word_count(int doc_id) {
    Book *book = searchByID(db->root, doc_id);
    if (book != NULL) {
        return book->word_count;
    } else {
        return -1;                                          //book not found
    }
}

//get name of book using its document ID
char *bstdb_get_name(int doc_id) {
    Book *book = searchByID(db->root, doc_id);
    if (book != NULL) {
        return book->name;
    } else {
        return NULL;                                        //book not found
    }
}

//run tests and print statistics
void bstdb_stat(void) {
    printf("Binary Search Tree Statistics\n");
    printf("-------------------------------------------\n\n");

    printf("Total Inserts: %d\n", db->next_doc_id - 1);     //assumes next_doc_id incremented on each insert

    //verify number of stored books
    int storedBooks = countBooks(db->root);
    printf("Stored Books: %d\n", storedBooks);

    //compute average number of nodes visited when retrieving result
    int totalNodesVisited = 0;
    int totalSearches = 0;

    //add some sample searches and track number of nodes visited
    for (int i = 1; i <= db->next_doc_id - 1; ++i) {
        totalNodesVisited += countNodesVisited(db->root, i);
        totalSearches++;
    }

    double averageNodesVisited = totalNodesVisited / (double)totalSearches;
    printf("Average Nodes Visited: %.2lf\n", averageNodesVisited);

    //print binary tree's balance info
    int height = getTreeHeight(db->root);
    printf("Tree Height: %d\n", height);
}
    

//free allocated database memory
void bstdb_quit(void) {
    freeBST(db->root);
    free(db);
}

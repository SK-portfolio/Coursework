#include <stdio.h>
#include <stdlib.h>
#include "bst.h"

void tree_insert(Tree_Node** root, char data) {
    if (*root == NULL) {                                    //if current node empty
        *root = (Tree_Node*)malloc(sizeof(Tree_Node));      //{allocate memory for new node
        (*root)->data = data;                               //set data of new node to given data
        (*root)->count = 1;                                 //set count of new node to 1
        (*root)->left = NULL;                               //set left child pointers of new node to NULL
        (*root)->right = NULL;                              //set rigth child pointers of new node to NULL}
    } else {                                            //curr node not empty
        if (data == (*root)->data) {                        //if given data same as data of curr node
            (*root)->count++;                               //{increment count of curr node}
        } else {
            if (data < (*root)->data) {                     //if given data less than data of curr node
                tree_insert(&((*root)->left), data);        //{insert new node into left subtree}
            } else if (data > (*root)->data) {              //if given data more than data of curr node
                tree_insert(&((*root)->right), data);       //{insert new node into right subtree}
            }
        }
    }
}

Tree_Node* create_bst(char data[]) {
    Tree_Node* root = NULL;                                 //initialize root of tree to NULL
    int i = 0;                                              //set index to 0
    while (data[i] != '\0') {                               //go through data array until null terminator is encountered
        tree_insert(&root, data[i]);                        //insert current element into BST
        i++;
    }
    return root;                                            //return root of created BST
}

Tree_Node* tree_search(Tree_Node* root, char data) {
    if (root == NULL || root->data == data) {               //if root NULL or root's data same as data
        return root;
    }
    if (data < root->data) {                                //if data less than root's data 
        return tree_search(root->left, data);               //search in left subtree
    } else {
        return tree_search(root->right, data);              //search in right subtree
    }
}

void tree_print_sorted(Tree_Node* root) {
    if (root != NULL) {                                     //if root not empty
        tree_print_sorted(root->left);                      //print sorted data in left subtree
        for (int i = 0; i < root->count; i++) {
            printf("%c", root->data);
        }
        tree_print_sorted(root->right);                     //print sorted data in right subtree
    }
}

void tree_delete(Tree_Node* root) {
    if (root != NULL) {                                     //if root not empty
        tree_delete(root->left);                            //delete nodes in left subtree
        tree_delete(root->right);                           //delete nodes in right subtree
        free(root);                                         //memory deallocated
    }
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_STRING_SIZE 20
#define ARRAY_SIZE 59
#define NAME_PROMPT "Enter term to get frequency or type \"quit\" to escape\n>>> "
#define NEW_LINE_PROMPT ">>> "

struct Surname {
    char name[MAX_STRING_SIZE];
    int frequency;
    struct Surname* next;
};

int hash1(char* s) {
    int hash = 0;
    while (*s) {
        hash = (hash + *s - 'A') % ARRAY_SIZE;
        s++;
    }
    return hash;
}

int hash3(char* s) {
    int hash = 0;
    while (*s) {
        hash = 1 + (hash + *s - 'A') % (ARRAY_SIZE - 1);
        s++;
    }
    return hash;
}

void insert(struct Surname* hash_table[], char* name, int* collisionCount) {
    int index = hash1(name);
    int index3 = hash3(name);

    while (hash_table[index] != NULL) {
        (*collisionCount)++;
        index = (index + index3) % ARRAY_SIZE;
    }


    struct Surname* new_node = malloc(sizeof(struct Surname));
    if (new_node == NULL) {
        fprintf(stderr, "Memory allocation error\n");
        exit(EXIT_FAILURE);
    }


    strncpy(new_node->name, name, sizeof(new_node->name));
    new_node->frequency = 1;
    new_node->next = NULL;


    hash_table[index] = new_node;
}

void load_file(struct Surname* hash_table[], char* filename, int* termCount, int* collisionCount) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Error opening file\n");
        exit(EXIT_FAILURE);
    }
    printf("names.csv loaded!\n");
    char buffer[MAX_STRING_SIZE];
    while (fgets(buffer, sizeof(buffer), file)) {
        buffer[strcspn(buffer, "\n")] = '\0';
        insert(hash_table, buffer, collisionCount);
        (*termCount)++;
    }
    fclose(file);
}

void Input2Frequency(struct Surname* hash_table[]) {
    char name[50];
    printf(NAME_PROMPT);
    scanf(" %[^\n]", name);                                 //input name (%[^\n] reads all charas until newline)
    
    while (strcmp(name, "quit") != 0) {                     //~while 'quit' has not been entered
        int index = hash1(name);                            //get hash index
        struct Surname* curr_name = hash_table[index];      //find current name occupying index

        if (curr_name == NULL){                             //if no current name occuping
            printf("%s not in table\n", name);
        }

        while (curr_name != NULL) {     	                //~~while index is occupied by current name
            if (strcmp(curr_name->name, name) == 0) {       //compare current name and input name- if same name 
                printf("%s %d\n", name, curr_name->frequency);
                break;
            }
            curr_name = curr_name->next;                    //move to next index~~
        }

        printf(NEW_LINE_PROMPT);
        scanf(" %[^\n]", name);                             //input another name~
    }
    exit(EXIT_SUCCESS);                                     //'quit' entered so exit function
}

int main() {
    struct Surname* hash_table[ARRAY_SIZE];
    for (int i = 0; i < ARRAY_SIZE; i++) {
        hash_table[i] = NULL;
    }
    int termCount = 0;
    int collisionCount = 0;

    load_file(hash_table, "names.csv", &termCount, &collisionCount);

    float load = termCount / (float)ARRAY_SIZE;

    printf("\tCapacity\t: %d\n", ARRAY_SIZE);
    printf("\tNum Terms\t: %d\n", termCount);
    printf("\tCollisions\t: %d\n", collisionCount);
    printf("\tLoad\t: %.2f%%\n", load);

    Input2Frequency(hash_table);

    for (int i = 0; i < ARRAY_SIZE; i++) {
        struct Surname* curr_name = hash_table[i];
        while (curr_name != NULL) {
            struct Surname* temp = curr_name;
            curr_name = curr_name->next;
            free(temp);
        }
        hash_table[i] = NULL;
    }

    return 0;
}

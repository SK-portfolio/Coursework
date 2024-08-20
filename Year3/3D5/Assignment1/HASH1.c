#include<stdio.h>
#include<stdlib.h>
#include <string.h> //for strcpy and strcmp
#include <ctype.h>  //for isalnum

#define MAX_STRING_SIZE 20
#define ARRAY_SIZE 59
#define NAME_PROMPT "Enter term to get frequency or type \"quit\" to escape\n>>> "
#define NEW_LINE_PROMPT ">>> " 


struct Surname {
    char name[MAX_STRING_SIZE];
    int frequency;
    struct Surname* next;                       //points to next Surname in table
};

int hash1(char* s){
    int hash = 0;
    while(*s){
       hash = (hash + *s - 'A') %ARRAY_SIZE;
        s++;
    }
    return hash;
}

void insert(struct Surname* hash_table[], char* name) {                                 //inserrts name into hash table
    int index = hash1(name);                                                            //calculates the hash value of given name
    struct Surname* curr_name = hash_table[index];                                      //find current name occupying index

    while (curr_name != NULL) {                                                         //~while index is occupied by current name 
        if (strcmp(curr_name->name, name) == 0) {                                       //compare current name and input name||if same name(/name already exists)
            curr_name->frequency++;                                                     //increment frequency
            return;
        }
        curr_name = curr_name->next;                                                    //move to next index~
    }
    //no current name occuping index
    struct Surname* new_name = (struct Surname*)malloc(sizeof(struct Surname));         //create new_name (new node for new name) || allocate enough memory for node field size
    if (new_name == NULL) {                                                             //if memory allocation fail                                                        
        fprintf(stderr, "Memory allocation error\n");
        exit(EXIT_FAILURE);
    }
    //memory allocation success
    strncpy(new_name->name, name, sizeof(new_name->name));                              //copy input name into field of new name node
    new_name->frequency = 1;                                                            //set frequency of new name to 1|| first instance of specific name in hash table 
    new_name->next = hash_table[index];                                                 //set next pointer of new name to current head of hash table|| link newly made name node to the top of list
    hash_table[index] = new_name;                                                       //update hash table to make sure new name is current head 
}

/*//made to see if all names loaded correctly from file
void printHashTable(struct Surname* hash_table[]) {                     //prints contents of hash table
    printf("Hash Table:\n");
    for (int i = 0; i < ARRAY_SIZE; i++) {
        struct Surname* curr_name = hash_table[i];                      //find current name occupying the i_th index
        while (curr_name != NULL) {                                     //~while index is occupied by current name 
            printf("%s: %d\n", curr_name->name, curr_name->frequency);  //output the name and its frequency
            curr_name = curr_name->next;                                //move to next index~ 
        }
    }
}*/

void load_file(struct Surname* hash_table[], char* filename) {    //loads surnames from .cvs file to Hash table          
    FILE* file = fopen(filename, "r");                            //find and opens [filename].csv (read only)
    if (file == NULL) {                                           //if no file with that name
        fprintf(stderr, "Error opening file\n");
        exit(EXIT_FAILURE);
    }
    printf("names.csv loaded!\n");
    char buffer[MAX_STRING_SIZE];
    while (fgets(buffer, sizeof(buffer), file)) {                 //while reading each line from file 

        buffer[strcspn(buffer, "\n")] = '\0';                     //remove newline(\n) chara if present
        insert(hash_table, buffer);                               //do insert into table function
    }

    fclose(file);
}

int numTerms(struct Surname* hash_table[]) {                //counts # of collisions in hash table
    int terms = 0;
    for (int i = 0; i < ARRAY_SIZE; i++) {
        struct Surname* curr_name = hash_table[i];          //find current name occupying the i_th index
        while (curr_name != NULL) {                         //~while index is occupied by current name
            terms++;                                        //increment term count
            curr_name = curr_name->next;                    //move to next index~
        }
    }
    return terms;
}

int numCollisions(struct Surname* hash_table[]) {           //counts # of collisions in hash table
    int collisions = 0;
    for (int i = 0; i < ARRAY_SIZE; i++) {
        struct Surname* curr_name = hash_table[i];          //find current name occupying the i_th index
        if (curr_name != NULL && curr_name->next != NULL) { //if the i_th & i+1_th index is occupied by current name & next name rspctvly
            collisions++;                                   //increment collision count
        }
    }                                                       //next iteration 
    return collisions;
}

void Input2Frequency(struct Surname* hash_table[]) {        //reads all inputs until 'quit' is entered
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

    load_file(hash_table, "names.csv");

    //printHashTable(hash_table);

    int termCount = numTerms(hash_table);
    int collisionCount = numCollisions(hash_table);
    float load = termCount / (float)ARRAY_SIZE;

    printf("\tCapacity\t: %d\n", ARRAY_SIZE);
    printf("\tNum Terms\t: %d\n", termCount);
    printf("\tCollisions\t: %d\n", collisionCount);
    printf("\tLoad\t: %.2f%%\n", load);

    Input2Frequency(hash_table);

    // Free allocated memory
    for (int i = 0; i < ARRAY_SIZE; i++) {
        struct Surname* curr_name = hash_table[i];
        while (curr_name != NULL) {
            struct Surname* temp = curr_name;
            curr_name = curr_name->next;
            free(temp);
        }
    }

    return 0;
}
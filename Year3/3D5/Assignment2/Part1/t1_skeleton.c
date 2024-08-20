#include <stdio.h>
#include <stdlib.h>
#include "t1.h"

//function to swap elements(Insertion Sort Algorithm 2 slide 9)
void swap (int *curr, int *next) 
{ 
    int temp = *curr; 
    *curr = *next; 
    *next = temp; 
} 

//Fills the array with ascending, consecutive numbers, starting from 0.
void fill_ascending(int *array, int size) { 
    for (int i = 0; i < size; i++) {
        array[i] = i;
    }
}    
//Fills the array with descending numbers, starting from size-1
void fill_descending(int *array, int size)
{
    for (int i = 0; i < size; i++) {
        array[i] = size - 1 - i;
    }
}

//Fills the array with uniform numbers.
void fill_uniform(int *array, int size)
{
    for (int i = 0; i < size; i++) {
        array[i] = 3; //choose any value.
    } 
}

//Fills the array with random numbers within 0 and size-1. Duplicates are allowed.
void fill_with_duplicates(int *array, int size)
{
    for (int i = 0; i < size; i++) {
        array[i] = rand() % size; //chooses random number btwn 0 and 5
    }
}


//Fills the array with unique numbers between 0 and size-1 in a shuffled order. Duplicates are not allowed.
void fill_without_duplicates(int *array, int size)
{
    fill_ascending(array, size); //start with setting up array with ascending values
    
    //use Fisher-Yates algorithm to shuffle array(https://www.geeksforgeeks.org/shuffle-a-given-array-using-fisher-yates-shuffle-algorithm/)
    for (int i = size - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        swap(&array[i], &array[j]); //swap array[i] and array[j]
    }
    
}

void printArray(int *arr, int size){
  int i;
  for(i=0; i<size;i++){
    printf("%d ", arr[i]);
  }
  printf("\n");
}

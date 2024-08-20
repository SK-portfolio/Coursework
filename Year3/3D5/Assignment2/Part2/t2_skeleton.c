#include <stdio.h> 
#include "t2.h"

int number_comparisons = 0;
int number_swaps = 0;

//another function to swap elements is identical to one in t1
void swap2(int *curr, int *next) 
{ 
    int temp = *curr; 
    *curr = *next; 
    *next = temp; 
} 

void selectionSort(int array[], int size) 
{ 
  int i, j, min_idx;
    for (i = 0; i < size - 1; i++) {
        min_idx = i;
        for (j = i + 1; j < size; j++) {
            number_comparisons++;                   //+1 to comparisons count
            if (array[j] < array[min_idx]) {
                min_idx = j;
            }
        }
        //swap minimum element with current element
        swap2(&array[i], &array[min_idx]);   
        number_swaps++;
    }
} 

void insertionSort(int array[], int size) 
{ 
    int i, key, j;

    for (i = 1; i < size; i++) {
        key = array[i];
        j = i - 1;
        
        while (j >= 0 && array[j] > key) {          //move elements greater than key to one position ahead of current position (next)
            number_comparisons++;                   //+1 to comparisons count
            array[j + 1] = array[j];
            j--;
            number_swaps++;
        }
        array[j + 1] = key;
    }
}

//places pivot element in correct position and rearrange array
int partition(int array[], int low, int high){      //partition scheme: Lomuto (https://www.geeksforgeeks.org/hoares-vs-lomuto-partition-scheme-quicksort/)
    int pivot = array[high];                        //pivot: last element
    int i = (low - 1);                              //index of smaller element

    for (int j = low; j < high; j++) {
        number_comparisons++;                       //+1 to comparisons count
        if (array[j] <= pivot) {
            i++;
            swap2(&array[i], &array[j]);             //swap array[i] and array[j]
            number_swaps++;
        }
    }
    swap2(&array[i+1], &array[high]);                //swap array[i+1] and array[high] (pivot)
    number_swaps++;
    return i + 1;
}

//prefoms sorting for quickSort()
void quickSortHelper(int array[], int low, int high){
    if (low < high) {
        int piv = partition(array, low, high);       //choose pivot as last element
        //sort elements before and after partition
        quickSortHelper(array, low, piv - 1);
        quickSortHelper(array, piv + 1, high);
    }
}

void quickSort(int array[], int size)
{
    quickSortHelper(array, 0, size - 1);
}
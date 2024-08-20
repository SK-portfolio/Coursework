#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_REVIEWS 15000

//define structure for review info
struct GameReview {
    char title[256];
    char system[256];
    int score;
    int year;
};

//comparison function for qsort to sort reviews by year (https://www.geeksforgeeks.org/comparator-function-of-qsort-in-c/)
int compareReviews(const void *a, const void *b) {
    int L = ((struct GameReview *)a)->year;             //inits L as year taken from object pointed to by a
    int R = ((struct GameReview *)b)->year;             //inits R as year taken from object pointed to by a
    return (L - R);                                     //return difference between years
}

//function to load and read reviews from .csv file (input file through terminal)
int loadGameReviews(const char *filename, struct GameReview reviews[], int max_reviews) {   //load reviews from file
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Error opening the file");
        return 0;
    }

    int review_count = 0;                                           // init review count
    char line[512];

    while (fgets(line, sizeof(line), file) && review_count < max_reviews) {     //>>while a line of characters(at most 512 char) read from .csv file 
        char *title, *system, *score_str, *year_str;                            //is stored in line array AND review count is less than maxcount

        title = strtok(line, ",");                                  //(strtok)split line into sections using comma as separator(delim)
        system = strtok(NULL, ",");
        score_str = strtok(NULL, ",");
        year_str = strtok(NULL, ",");

        if (title && system && score_str && year_str) {             // if all variables are defined
            int year = atoi(year_str);                              //(atoi)convert string into integer
            int score = atoi(score_str);                            //(atoi)convert string into integer

            
            if ((year >= 1996 && year <= 2016) && (score == 10)) {  //if review is in 20-year range AND has a score of 10
                
                strcpy(reviews[review_count].title, title);         //copy data into separate array of review objects at index [whatever review_count is currently]
                strcpy(reviews[review_count].system, system);
                reviews[review_count].score = score;                //score & year are int -> don't need (strcpy())
                reviews[review_count].year = year;
                review_count++;                                     //review load success so increment review count>>
            }
        }
    }

    fclose(file);
    return review_count;
}

//function to print top games list
void printTopGames(const struct GameReview reviews[], int review_count) {
    if (review_count == 0) {                                                        //if no reviews loaded
        printf("No top-rated games found in the specified year range.\n");
        return;
    }
    //reviews present
    
    struct GameReview *sortedReviews = malloc(review_count * sizeof(struct GameReview));    //allocate memory for new array to store sorted reviews
    if (!sortedReviews) {                                                                   //if malloc fails
        perror("Memory allocation error");
        return;
    }
    //malloc success

    memcpy(sortedReviews, reviews, review_count * sizeof(struct GameReview));       //copy memory from review[] to sortedReviews[] 
    qsort(sortedReviews, review_count, sizeof(struct GameReview), compareReviews);  //sorts array using compareReviews to tell it order elements should be sorted in

    int current_year = 0;       //init to keep track
    int count = 0;

    printf("-----------------------------------------------------------------------\n"); 
    printf("-----Top 10 most popular games of the last 20 years (1996 to 2016)-----");    //headline(start of output)
    //get current year

    for (int i = 0; i < review_count; i++) {                    //>>loop through the sorted reviews for [review_count-1] iterations
        if (sortedReviews[i].year != current_year) {            //{if year of review not same as current year
            current_year = sortedReviews[i].year;               //update current year to be year of review
            count = 1;                                          //reset count
            printf("\n-----------------------------------------------------------------------\n"); //list divider
            printf("\nYear: %d\n", current_year);               //print year as header for list}
        }
        //make list
        if (count <= 10) {                                      //{if count less/equal to 10
            printf("%d. Title: %s, System: %s, Score: %d\n", count, sortedReviews[i].title, sortedReviews[i].system, sortedReviews[i].score); //Print position(current count num), title, system, and score of game 
            count++;                                            //increment count}
        }
    }                                                           //increment i>>
    free(sortedReviews);                                        //free allocated memory
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <input_file>\n", argv[0]);                                //ask for input file [to read file use -> ./t4 t4_ign.csv]
        return 1;                                                                   //terminate code(as error)}
    }

    struct GameReview *reviews = malloc(MAX_REVIEWS * sizeof(struct GameReview));   //allocate memory for storing reviews
    if (!reviews) {                                                                 //{if malloc fails
        perror("Memory allocation error");
        return 1;                                                                   //terminate code(as error)}
    }

    int review_count = loadGameReviews(argv[1], reviews, MAX_REVIEWS);              //init review_count as loaded reviews from file

    
    printTopGames(reviews, review_count); 

    free(reviews);                                                                  //free allocated memory
    return 0;                                                                       //terminate code
}

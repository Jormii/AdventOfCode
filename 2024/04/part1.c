#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>  // NOTE: malloc() not required but it's for comparison purposes
#include <time.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (2378)

#define ROWS (140)
#define COLUMNS (140 + 1)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define XMAS_LEN (4)
#define MATRIX_ARRLEN (ROWS * COLUMNS)

typedef struct Matrix_st {
    char *arr;
    int rows, columns;
} Matrix;

int find(const Matrix *matrix);

int main() {
    struct timespec ts0, tsf;
    clock_gettime(CLOCK_MONOTONIC_RAW, &ts0);

    FILE *file = fopen(INPUT, "r");

    Matrix matrix = {
        .arr = malloc(MATRIX_ARRLEN),
        .rows = ROWS,
        .columns = COLUMNS,
    };

    for (int i = 0; i < MATRIX_ARRLEN; ++i) {
        matrix.arr[i] = fgetc(file);
    }

    fclose(file);

    int total = find(&matrix);

    clock_gettime(CLOCK_MONOTONIC_RAW, &tsf);
    uint64_t t = ((uint64_t)(ts0.tv_sec) * 1000000000) + (uint64_t)(ts0.tv_nsec);
    uint64_t tf = ((uint64_t)(tsf.tv_sec) * 1000000000) + (uint64_t)(tsf.tv_nsec);

    int success = total == SOLUTION;
    fprintf(stderr, "%f\n", ((double)(tf - t)) / 1000000000.0);
    printf("Solution: %d (%d)\n", total, success);

    return (success) ? 0 : 1;
}

int find(const Matrix *matrix) {
    int total = 0;

    int rows = matrix->rows;
    int columns = matrix->columns;

    const char *row_up_3 = 0;
    const char *row_up_2 = 0;
    const char *row_up_1 = 0;
    const char *row = matrix->arr;
    const char *row_down_1 = row + columns;
    const char *row_down_2 = row_down_1 + columns;
    const char *row_down_3 = row_down_2 + columns;

    for (int r = 0; r < rows; ++r) {
        int check_down = (r + XMAS_LEN) <= rows;
        int check_up = (r - XMAS_LEN) >= -1;

        for (int c = 0; c < columns; ++c) {
            if (row[c] != 'X') {
                continue;
            }

            int check_right = (c + XMAS_LEN) <= columns;
            int check_left = (c - XMAS_LEN) >= -1;

            if (check_right) {
                total += (row[c + 1] == 'M' && row[c + 2] == 'A' && row[c + 3] == 'S');
            }
            if (check_left) {
                total += (row[c - 1] == 'M' && row[c - 2] == 'A' && row[c - 3] == 'S');
            }
            if (check_down) {
                total += (row_down_1[c] == 'M' && row_down_2[c] == 'A' && row_down_3[c] == 'S');
            }
            if (check_up) {
                total += (row_up_1[c] == 'M' && row_up_2[c] == 'A' && row_up_3[c] == 'S');
            }
            if (check_right && check_down) {
                total += (row_down_1[c + 1] == 'M' && row_down_2[c + 2] == 'A' && row_down_3[c + 3] == 'S');
            }
            if (check_right && check_up) {
                total += (row_up_1[c + 1] == 'M' && row_up_2[c + 2] == 'A' && row_up_3[c + 3] == 'S');
            }
            if (check_left && check_down) {
                total += (row_down_1[c - 1] == 'M' && row_down_2[c - 2] == 'A' && row_down_3[c - 3] == 'S');
            }
            if (check_left && check_up) {
                total += (row_up_1[c - 1] == 'M' && row_up_2[c - 2] == 'A' && row_up_3[c - 3] == 'S');
            }
        }

        row_up_3 = row_up_2;
        row_up_2 = row_up_1;
        row_up_1 = row;
        row = row_down_1;
        row_down_1 = row_down_2;
        row_down_2 = row_down_3;
        row_down_3 += columns;
    }

    return total;
}

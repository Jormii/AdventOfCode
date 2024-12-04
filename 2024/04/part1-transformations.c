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
#define SOLUTION (7025140)

#define ROWS (15000)
#define COLUMNS (15000 + 1)
#endif

#define XMAS_LEN (4)
#define MATRIX_ARRLEN (ROWS * COLUMNS)

typedef struct Matrix_st {
    char *arr;
    int rows, columns;
} Matrix;

typedef struct RolledMatrices_st {
    Matrix left, right;
} RolledMatrices;

int find(const Matrix *matrix);
Matrix transpose(const Matrix *matrix);
RolledMatrices roll_then_transpose(const Matrix *matrix);

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

    Matrix matrix_T = transpose(&matrix);
    RolledMatrices rolled_matrices = roll_then_transpose(&matrix);

    int total = 0;
    total += find(&matrix);
    total += find(&matrix_T);
    total += find(&(rolled_matrices.left));
    total += find(&(rolled_matrices.right));

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

    const char *row = matrix->arr;
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < (columns - (XMAS_LEN - 1)); ++c) {
            total += (row[c] == 'X' && row[c + 1] == 'M' && row[c + 2] == 'A' && row[c + 3] == 'S');
            total += (row[c + 3] == 'X' && row[c + 2] == 'M' && row[c + 1] == 'A' && row[c] == 'S');
        }

        row += columns;
    }

    return total;
}

Matrix transpose(const Matrix *matrix) {
    int rows = matrix->rows;
    int columns = matrix->columns;

    Matrix transposed = {
        .arr = malloc(MATRIX_ARRLEN),
        .rows = columns,
        .columns = rows,
    };

    int idx = 0;
    for (int r = 0; r < rows; ++r) {
        int idx_T = r;

        for (int c = 0; c < columns; ++c) {
            transposed.arr[idx_T] = matrix->arr[idx];

            ++idx;
            idx_T += transposed.columns;
        }
    }

    return transposed;
}

RolledMatrices roll_then_transpose(const Matrix *matrix) {
    int rows = matrix->rows;
    int columns = matrix->columns;

    Matrix rolled_left_T = {
        .arr = malloc(MATRIX_ARRLEN),
        .rows = columns,
        .columns = rows,
    };
    Matrix rolled_right_T = {
        .arr = malloc(MATRIX_ARRLEN),
        .rows = columns,
        .columns = rows,
    };

    const char *row = matrix->arr;
    for (int r = 0; r < rows; ++r) {
        char *left_row = rolled_left_T.arr;
        char *right_row = rolled_right_T.arr;

        for (int c = 0; c < columns; ++c) {
            int c_left = (c + r) % columns;
            int c_right = (c - r) % columns;
            if (c_right < 0) {
                c_right += columns;
            }

            left_row[r] = row[c_left];
            right_row[r] = row[c_right];

            left_row += rolled_left_T.columns;
            right_row += rolled_right_T.columns;
        }

        row += columns;
    }

    return (RolledMatrices){rolled_left_T, rolled_right_T};
}

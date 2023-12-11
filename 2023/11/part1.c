#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (10228230)

#define WIDTH (140)
#define HEIGHT (140)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define ABS(x) (((x) >= 0) ? (x) : -(x))

typedef struct Cell_st
{
    int row, column;
} Cell;

int empty_row[HEIGHT];
int empty_column[WIDTH];

int galaxies_count = 0;
Cell galaxies[WIDTH * HEIGHT];

void parse_row(int row, char *out_c, FILE *file);

int main()
{
    FILE *file = fopen(INPUT, "r");

    for (int i = 0; i < HEIGHT; ++i)
    {
        empty_row[i] = 1;
    }
    for (int i = 0; i < WIDTH; ++i)
    {
        empty_column[i] = 1;
    }

    char c = fgetc(file);
    for (int row = 0; row < HEIGHT; ++row)
    {
        parse_row(row, &c, file);
    }

    int expanded_row[HEIGHT];
    expanded_row[0] = empty_row[0];
    for (int i = 1; i < HEIGHT; ++i)
    {
        expanded_row[i] = 1 + expanded_row[i - 1] + empty_row[i];
    }

    int expanded_column[WIDTH];
    expanded_column[0] = empty_column[0];
    for (int i = 1; i < WIDTH; ++i)
    {
        expanded_column[i] = 1 + expanded_column[i - 1] + empty_column[i];
    }

    int sum = 0;
    for (int i = 0; i < galaxies_count - 1; ++i)
    {
        int ith_row = expanded_row[galaxies[i].row];
        int ith_column = expanded_column[galaxies[i].column];

        for (int j = i + 1; j < galaxies_count; ++j)
        {
            int jth_row = expanded_row[galaxies[j].row];
            int jth_column = expanded_column[galaxies[j].column];

            sum += ABS(ith_row - jth_row) + ABS(ith_column - jth_column);
        }
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %d (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

void parse_row(int row, char *out_c, FILE *file)
{
    char c = *out_c;
    for (int column = 0; column < WIDTH; ++column)
    {
        if (c == '#')
        {
            Cell *cell = galaxies + galaxies_count;
            cell->row = row;
            cell->column = column;

            ++galaxies_count;
            empty_row[row] = 0;
            empty_column[column] = 0;
        }

        c = fgetc(file);
    }

    *out_c = fgetc(file);
}

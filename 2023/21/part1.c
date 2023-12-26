#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (3687)

#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define STEPS (64)
#define NOT_ACCESSIBLE (-1)
#define EVEN_STEPS ((STEPS & 1) == 0)
#define WIDTH (131)
#define HEIGHT (131)
#define GARDEN_SIZE (WIDTH * HEIGHT)
#define ABS(x) (((x) >= 0) ? (x) : -(x))
#define MIN(x, y) (((x) <= (y)) ? (x) : (y))
#define IDX(row, column) (WIDTH * (row) + (column))

typedef struct Cell_st
{
    char grid;
    int steps;
} Cell;

Cell garden[GARDEN_SIZE];
int start_row, start_column;

void parse_row(int row, char *out_c, FILE *file);
int check_accessible(int row, int column, int steps);

int main()
{
    FILE *file = fopen(INPUT, "r");

    char c = fgetc(file);
    for (int row = 0; row < HEIGHT; ++row)
    {
        parse_row(row, &c, file);
    }

    int accessible = 0;
    for (int row = start_row - STEPS; row <= start_row + STEPS; ++row)
    {
        if (row < 0 || row >= HEIGHT)
        {
            continue;
        }

        int rd = STEPS - ABS(start_row - row);

        int left = start_column - rd;
        int right = start_column + rd;
        for (int column = left; column <= right; ++column)
        {
            if (column < 0 || column >= WIDTH)
            {
                continue;
            }

            int steps = check_accessible(row, column, 0);
            if (steps != NOT_ACCESSIBLE)
            {
                int even_steps = (steps & 1) == 0;
                accessible += even_steps == EVEN_STEPS;
            }
        }
    }

    fclose(file);

    int success = accessible == SOLUTION;
    printf("Solution: %d (%d)\n", accessible, success);

    return (success) ? 0 : 1;
}

void parse_row(int row, char *out_c, FILE *file)
{
    char c = *out_c;
    for (
        int column = 0, idx = IDX(row, column);
        column < WIDTH;
        ++column, ++idx, c = fgetc(file))
    {
        garden[idx].grid = c;

        if (c == 'S')
        {
            start_row = row;
            start_column = column;
            garden[idx].steps = 0;
        }
        else
        {
            garden[idx].steps = NOT_ACCESSIBLE;
        }
    }

    *out_c = fgetc(file);
}

int check_accessible(int row, int column, int steps)
{
    if (row < 0 || row >= HEIGHT || column < 0 || column >= WIDTH)
    {
        return NOT_ACCESSIBLE;
    }

    int manhattan = ABS(row - start_row) + ABS(column - start_column);
    if (manhattan > (STEPS - steps))
    {
        return NOT_ACCESSIBLE;
    }

    Cell *cell = garden + IDX(row, column);
    if (cell->steps != NOT_ACCESSIBLE)
    {
        int total = steps + cell->steps;
        return (total > STEPS) ? NOT_ACCESSIBLE : total;
    }

    int steps_needed = NOT_ACCESSIBLE;
    if (cell->grid != '#' && steps != STEPS)
    {
        int n = check_accessible(row - 1, column, steps + 1);
        int w = check_accessible(row, column - 1, steps + 1);
        int s = check_accessible(row + 1, column, steps + 1);
        int e = check_accessible(row, column + 1, steps + 1);

        steps_needed = GARDEN_SIZE;
        if (n != NOT_ACCESSIBLE)
        {
            steps_needed = MIN(steps_needed, n);
        }
        if (w != NOT_ACCESSIBLE)
        {
            steps_needed = MIN(steps_needed, w);
        }
        if (s != NOT_ACCESSIBLE)
        {
            steps_needed = MIN(steps_needed, s);
        }
        if (e != NOT_ACCESSIBLE)
        {
            steps_needed = MIN(steps_needed, e);
        }

        steps_needed = (steps_needed == GARDEN_SIZE) ? NOT_ACCESSIBLE : steps_needed;
    }

    if (steps_needed != NOT_ACCESSIBLE)
    {
        cell->steps = steps_needed - steps;
    }

    return steps_needed;
}

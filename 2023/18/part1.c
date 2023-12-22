#include <stdio.h>
#include <stdlib.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (41019)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define LINES (606)

#define MIN(x, y) (((x) <= (y)) ? (x) : (y))
#define MAX(x, y) (((x) >= (y)) ? (x) : (y))
#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')
#define IDX(row, column, width) ((width) * (row) + (column))

typedef struct Plan_st
{
    char vx, vy;
    char meters;
    int hex_color;
} Plan;

Plan dig_plan[LINES];

Plan parse_row(int *out_row, int *out_column, char *out_c, FILE *file);
int dig_trench(int row, int column, char *terrain, int width);
int count_interior(const char *terrain, int width, int height);

int main()
{
    FILE *file = fopen(INPUT, "r");

    int row = 0;
    int column = 0;
    int top_row = 0, left_column = 0;
    int bottom_row = 0, right_column = 0;

    char c = fgetc(file);
    for (int i = 0; i < LINES; ++i)
    {
        dig_plan[i] = parse_row(&row, &column, &c, file);

        top_row = MIN(top_row, row);
        left_column = MIN(left_column, column);
        bottom_row = MAX(bottom_row, row);
        right_column = MAX(right_column, column);
    }

    int height = bottom_row - top_row + 1;
    int width = right_column - left_column + 1;

    char *terrain = malloc((size_t)(width * height) * sizeof(char));
    for (int i = 0; i < (width * height); ++i)
    {
        terrain[i] = '.';
    }

    row = -top_row;
    column = -left_column;
    int cubic_meters = dig_trench(row, column, terrain, width);

    cubic_meters += count_interior(terrain, width, height);

    fclose(file);
    free(terrain);

    int success = cubic_meters == SOLUTION;
    printf("Solution: %d (%d)\n", cubic_meters, success);

    return (success) ? 0 : 1;
}

Plan parse_row(int *out_row, int *out_column, char *out_c, FILE *file)
{
    Plan plan = {.vx = 0, .vy = 0, .meters = 0, .hex_color = 0};
    char c = *out_c;

    switch (c)
    {
    case 'U':
        plan.vx = 0;
        plan.vy = -1;
        break;
    case 'L':
        plan.vx = -1;
        plan.vy = 0;
        break;
    case 'D':
        plan.vx = 0;
        plan.vy = 1;
        break;
    case 'R':
        plan.vx = 1;
        plan.vy = 0;
        break;
    default:
        break;
    }

    fgetc(file);
    c = fgetc(file);
    for (; c != ' '; c = fgetc(file))
    {
        plan.meters = 10 * plan.meters + (c - '0');
    }

    fgetc(file);
    fgetc(file);
    c = fgetc(file);
    for (int i = 0; i < 6; ++i, c = fgetc(file))
    {
        int digit = 0;
        if (CHAR_IS_NUM(c))
        {
            digit = c - '0';
        }
        else
        {
            digit = 10 + c - 'a';
        }

        plan.hex_color = 16 * plan.hex_color + digit;
    }
    fgetc(file);

    *out_c = fgetc(file);
    *out_row += plan.meters * plan.vy;
    *out_column += plan.meters * plan.vx;

    return plan;
}

int dig_trench(int row, int column, char *terrain, int width)
{
    int cubic_meters = 0;

    terrain[IDX(row, column, width)] = '#';

    const Plan *plan = dig_plan;
    const Plan *end = dig_plan + LINES;
    for (; plan != end; ++plan)
    {
        for (int i = 0; i < plan->meters; ++i)
        {
            row += plan->vy;
            column += plan->vx;

            ++cubic_meters;
            terrain[IDX(row, column, width)] = '#';
        }
    }

    return cubic_meters;
}

int count_interior(const char *terrain, int width, int height)
{
    int cubic_meters = 0;

    for (int row = 0; row < height; ++row)
    {
        int intersections = 0;
        for (int column = 0; column < width; ++column)
        {
            const char *tile = terrain + IDX(row, column, width);

            if (*tile == '.')
            {
                cubic_meters += (intersections & 1);
            }
            else
            {
                int e = (column + 1) != width && terrain[IDX(row, column + 1, width)] == '#';

                int ne = e &&
                         (row - 1) >= 0 && terrain[IDX(row - 1, column, width)] == '#';
                int se = e &&
                         (row + 1) != height && terrain[IDX(row + 1, column, width)] == '#';

                if (!(ne || se))
                {
                    ++intersections;
                }
                else
                {
                    ++column;
                    const char *corner = tile + 1;

                    int nw = 0, sw = 0;
                    for (; !(nw || sw); ++column, ++corner)
                    {
                        nw = (row - 1) >= 0 && terrain[IDX(row - 1, column, width)] == '#';
                        sw = (row + 1) != height && terrain[IDX(row + 1, column, width)] == '#';
                    }
                    --column;

                    intersections += (ne && sw) || (se && nw);
                }
            }
        }
    }

    return cubic_meters;
}

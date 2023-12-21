#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (7324)

#define WIDTH (110)
#define HEIGHT (110)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define LAYOUT_SIZE (WIDTH * HEIGHT)
#define MAX(x, y) (((x) >= (y)) ? (x) : (y))
#define IDX(row, column) (WIDTH * (row) + (column))

typedef struct Cell_st
{
    char tile;
    int energized;
    int activated_splitter;
} Cell;

int energized = 0;
Cell layout[LAYOUT_SIZE];

void parse_row(int row, char *out_c, FILE *file);
void reset_layout();
void project_beam(int row, int column, int vx, int vy);

int main()
{
    FILE *file = fopen(INPUT, "r");

    char c = fgetc(file);
    for (int row = 0; row < HEIGHT; ++row)
    {
        parse_row(row, &c, file);
    }

    int maximum = 0;
    for (int row = 0; row < HEIGHT; ++row)
    {
        reset_layout();
        project_beam(row, 0, 1, 0);
        maximum = MAX(maximum, energized);

        reset_layout();
        project_beam(row, WIDTH - 1, -1, 0);
        maximum = MAX(maximum, energized);
    }
    for (int column = 0; column < WIDTH; ++column)
    {
        reset_layout();
        project_beam(0, column, 0, 1);
        maximum = MAX(maximum, energized);

        reset_layout();
        project_beam(HEIGHT - 1, column, 0, -1);
        maximum = MAX(maximum, energized);
    }

    fclose(file);

    int success = maximum == SOLUTION;
    printf("Solution: %d (%d)\n", maximum, success);

    return (success) ? 0 : 1;
}

void parse_row(int row, char *out_c, FILE *file)
{
    char c = *out_c;
    for (
        int col = 0, idx = IDX(row, col);
        col < WIDTH;
        ++col, ++idx, c = fgetc(file))
    {
        layout[idx].tile = c;
        layout[idx].energized = 0;
        layout[idx].activated_splitter = 0;
    }

    *out_c = fgetc(file);
}

void reset_layout()
{
    energized = 0;

    const Cell *end = layout + LAYOUT_SIZE;
    for (Cell *cell = layout; cell < end; ++cell)
    {
        cell->energized = 0;
        cell->activated_splitter = 0;
    }
}

void project_beam(int row, int column, int vx, int vy)
{
    while (!(row < 0 || row >= HEIGHT || column < 0 || column >= WIDTH))
    {
        Cell *cell = layout + IDX(row, column);

        cell->energized += 1;
        energized += cell->energized == 1;

        if (cell->tile == '|')
        {
            if (vx != 0)
            {
                if (!cell->activated_splitter)
                {
                    cell->activated_splitter = 1;
                    project_beam(row - 1, column, 0, -1);
                    project_beam(row + 1, column, 0, 1);
                }
                break;
            }
        }
        else if (cell->tile == '-')
        {
            if (vy != 0)
            {
                if (!cell->activated_splitter)
                {
                    cell->activated_splitter = 1;
                    project_beam(row, column - 1, -1, 0);
                    project_beam(row, column + 1, 1, 0);
                }
                break;
            }
        }
        else if (cell->tile == '/')
        {
            int tmp = vx;
            vx = -vy;
            vy = -tmp;
        }
        else if (cell->tile == '\\')
        {
            int tmp = vx;
            vx = vy;
            vy = tmp;
        }

        row += vy;
        column += vx;
    }
}

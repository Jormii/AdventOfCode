#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (6947)

#define WIDTH (140)
#define HEIGHT (140)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define MAZE_SIZE (WIDTH * HEIGHT)
#define MIN(x, y) (((x) <= (y)) ? (x) : (y))
#define MAX(x, y) (((x) >= (y)) ? (x) : (y))
#define IDX(row, column) (WIDTH * (row) + (column))

typedef enum Pipe_en
{
    START,
    GROUND,
    VERTICAL,
    HORIZONTAL,
    NE,
    NW,
    SW,
    SE,
} Pipe;

typedef struct Cell_st
{
    Pipe pipe;
    int distance;
} Cell;

Cell maze[MAZE_SIZE];
int start_row, start_column;

void parse_row(int row, char *out_c, FILE *file);
Pipe get_pipe(int row, int column);
int explore_maze(int row, int column, int distance);

int main()
{
    FILE *file = fopen(INPUT, "r");

    char c = fgetc(file);
    for (int row = 0; row < HEIGHT; ++row)
    {
        parse_row(row, &c, file);
    }

    Pipe pipe;
    int n, s, w, e;
    n = s = w = e = MAZE_SIZE;

    pipe = get_pipe(start_row - 1, start_column);
    if (pipe == VERTICAL || pipe == SW || pipe == SE)
    {
        n = explore_maze(start_row - 1, start_column, 1);
    }

    pipe = get_pipe(start_row + 1, start_column);
    if (pipe == VERTICAL || pipe == NW || pipe == NE)
    {
        s = explore_maze(start_row + 1, start_column, 1);
    }

    pipe = get_pipe(start_row, start_column - 1);
    if (pipe == HORIZONTAL || pipe == NE || pipe == SE)
    {
        w = explore_maze(start_row, start_column - 1, 1);
    }

    pipe = get_pipe(start_row, start_column + 1);
    if (pipe == HORIZONTAL || pipe == NW || pipe == SW)
    {
        e = explore_maze(start_row, start_column + 1, 1);
    }

    int farthest = MIN(n, s);
    farthest = MIN(farthest, w);
    farthest = MIN(farthest, e);

    fclose(file);

    int success = farthest == SOLUTION;
    printf("Solution: %d (%d)\n", farthest, success);

    return (success) ? 0 : 1;
}

void parse_row(int row, char *out_c, FILE *file)
{
    char c = *out_c;
    Cell *cell = maze + IDX(row, 0);
    for (int column = 0; column < WIDTH; ++column, ++cell)
    {
        cell->distance = MAZE_SIZE;

        switch (c)
        {
        case 'S':
            start_row = row;
            start_column = column;

            cell->pipe = START;
            cell->distance = 0;
            break;
        case '.':
            cell->pipe = GROUND;
            break;
        case '|':
            cell->pipe = VERTICAL;
            break;
        case '-':
            cell->pipe = HORIZONTAL;
            break;
        case 'L':
            cell->pipe = NE;
            break;
        case 'J':
            cell->pipe = NW;
            break;
        case '7':
            cell->pipe = SW;
            break;
        case 'F':
            cell->pipe = SE;
            break;
        default:
            break;
        }

        c = fgetc(file);
    }

    *out_c = fgetc(file);
}

Pipe get_pipe(int row, int column)
{
    if (row < 0 || row >= HEIGHT || column < 0 || column >= WIDTH)
    {
        return GROUND;
    }
    else
    {
        return maze[IDX(row, column)].pipe;
    }
}

int explore_maze(int row, int column, int distance)
{
    if (row < 0 || row >= HEIGHT || column < 0 || column >= WIDTH)
    {
        return MAZE_SIZE;
    }

    Cell *cell = maze + IDX(row, column);
    if (cell->pipe == GROUND)
    {
        return MAZE_SIZE;
    }
    else if (cell->distance <= distance)
    {
        return cell->distance;
    }

    cell->distance = distance;

    int next_rows[2];
    int next_columns[2];
    switch (cell->pipe)
    {
    case VERTICAL:
        next_rows[0] = row - 1;
        next_rows[1] = row + 1;
        next_columns[0] = next_columns[1] = column;
        break;
    case HORIZONTAL:
        next_columns[0] = column - 1;
        next_columns[1] = column + 1;
        next_rows[0] = next_rows[1] = row;
        break;
    case NE:
        next_rows[0] = row;
        next_columns[0] = column + 1;
        next_rows[1] = row - 1;
        next_columns[1] = column;
        break;
    case NW:
        next_rows[0] = row;
        next_columns[0] = column - 1;
        next_rows[1] = row - 1;
        next_columns[1] = column;
        break;
    case SW:
        next_rows[0] = row;
        next_columns[0] = column - 1;
        next_rows[1] = row + 1;
        next_columns[1] = column;
        break;
    case SE:
        next_rows[0] = row;
        next_columns[0] = column + 1;
        next_rows[1] = row + 1;
        next_columns[1] = column;
        break;
    default:
        return MAZE_SIZE;
    }

    int n = explore_maze(next_rows[0], next_columns[0], distance + 1);
    int m = explore_maze(next_rows[1], next_columns[1], distance + 1);

    int farthest = distance;
    if (n != MAZE_SIZE)
    {
        farthest = MAX(farthest, n);
    }
    if (m != MAZE_SIZE)
    {
        farthest = MAX(farthest, m);
    }

    return farthest;
}

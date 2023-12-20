#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (273)

#define WIDTH (140)
#define HEIGHT (140)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define MAZE_SIZE (WIDTH * HEIGHT)
#define IDX(row, column) (WIDTH * (row) + (column))

typedef enum Pipe_en
{
    VERTICAL,
    HORIZONTAL,
    NE,
    NW,
    SW,
    SE,
    _PIPES_COUNT_,
    START,
    GROUND,
} Pipe;

typedef enum Direction_en
{
    NORTH,
    WEST,
    SOUTH,
    EAST,
    _DIRECTIONS_COUNT_,
} Direction;

typedef struct Offset_st
{
    int row_offset, column_offset;
} Offset;

typedef struct PipeData_st
{
    int compatible[_DIRECTIONS_COUNT_];
    Direction outcoming[_DIRECTIONS_COUNT_];
} PipeData;

typedef struct Cell_st
{
    Pipe pipe;
    int main_loop;
} Cell;

Cell maze[MAZE_SIZE];
int start_row, start_column;

PipeData pipes[_PIPES_COUNT_];
Offset offsets[_DIRECTIONS_COUNT_] = {
    {.row_offset = -1, .column_offset = 0},
    {.row_offset = 0, .column_offset = -1},
    {.row_offset = 1, .column_offset = 0},
    {.row_offset = 0, .column_offset = 1},
};

void parse_row(int row, char *out_c, FILE *file);
int explore_maze(Pipe start_pipe, Direction moving);
int count_enclosed();

int main()
{
    FILE *file = fopen(INPUT, "r");

    for (Pipe pipe = 0; pipe < _PIPES_COUNT_; ++pipe)
    {
        PipeData *data = pipes + pipe;
        for (Direction direction = 0; direction < _DIRECTIONS_COUNT_; ++direction)
        {
            data->compatible[direction] = 0;
        }
    }

    pipes[VERTICAL].compatible[NORTH] = 1;
    pipes[VERTICAL].outcoming[NORTH] = NORTH;
    pipes[VERTICAL].compatible[SOUTH] = 1;
    pipes[VERTICAL].outcoming[SOUTH] = SOUTH;

    pipes[HORIZONTAL].compatible[WEST] = 1;
    pipes[HORIZONTAL].outcoming[WEST] = WEST;
    pipes[HORIZONTAL].compatible[EAST] = 1;
    pipes[HORIZONTAL].outcoming[EAST] = EAST;

    pipes[NE].compatible[WEST] = 1;
    pipes[NE].outcoming[WEST] = NORTH;
    pipes[NE].compatible[SOUTH] = 1;
    pipes[NE].outcoming[SOUTH] = EAST;

    pipes[NW].compatible[EAST] = 1;
    pipes[NW].outcoming[EAST] = NORTH;
    pipes[NW].compatible[SOUTH] = 1;
    pipes[NW].outcoming[SOUTH] = WEST;

    pipes[SW].compatible[NORTH] = 1;
    pipes[SW].outcoming[NORTH] = WEST;
    pipes[SW].compatible[EAST] = 1;
    pipes[SW].outcoming[EAST] = SOUTH;

    pipes[SE].compatible[NORTH] = 1;
    pipes[SE].outcoming[NORTH] = EAST;
    pipes[SE].compatible[WEST] = 1;
    pipes[SE].outcoming[WEST] = SOUTH;

    char c = fgetc(file);
    for (int row = 0; row < HEIGHT; ++row)
    {
        parse_row(row, &c, file);
    }

    int loop_length = MAZE_SIZE;
    for (Pipe start_pipe = VERTICAL; loop_length == MAZE_SIZE && start_pipe < _PIPES_COUNT_; ++start_pipe)
    {
        for (Direction moving = NORTH; loop_length == MAZE_SIZE && moving < _DIRECTIONS_COUNT_; ++moving)
        {
            loop_length = explore_maze(start_pipe, moving);
        }
    }

    int enclosed = count_enclosed();

    fclose(file);

    int success = enclosed == SOLUTION;
    printf("Solution: %d (%d)\n", enclosed, success);

    return (success) ? 0 : 1;
}

void parse_row(int row, char *out_c, FILE *file)
{
    char c = *out_c;
    Cell *cell = maze + IDX(row, 0);
    for (int column = 0; column < WIDTH; ++column, ++cell)
    {
        cell->main_loop = 0;

        switch (c)
        {
        case 'S':
            start_row = row;
            start_column = column;

            cell->pipe = START;
            cell->main_loop = 1;
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

int explore_maze(Pipe start_pipe, Direction moving)
{
    Direction opposite = (moving + _DIRECTIONS_COUNT_ / 2) % _DIRECTIONS_COUNT_;
    if (!(pipes[start_pipe].compatible[opposite]))
    {
        return MAZE_SIZE;
    }

    Cell *start_cell = maze + IDX(start_row, start_column);

    start_cell->main_loop = 1;
    start_cell->pipe = start_pipe;

    int row = start_row + offsets[moving].row_offset;
    int column = start_column + offsets[moving].column_offset;

    int loop_length = 1;
    while (!(row == start_row && column == start_column))
    {
        if (row < 0 || row >= HEIGHT || column < 0 || column >= WIDTH)
        {
            loop_length = MAZE_SIZE;
        }
        else
        {
            Cell *cell = maze + IDX(row, column);
            if (cell->pipe == GROUND || !(pipes[cell->pipe].compatible[moving]))
            {
                loop_length = MAZE_SIZE;
            }
            else
            {
                ++loop_length;
                cell->main_loop = 1;

                moving = pipes[cell->pipe].outcoming[moving];

                row += offsets[moving].row_offset;
                column += offsets[moving].column_offset;
            }
        }

        if (loop_length == MAZE_SIZE)
        {
            break;
        }
    }

    if (!(pipes[start_pipe].compatible[moving]))
    {
        loop_length = MAZE_SIZE;
    }

    if (loop_length == MAZE_SIZE)
    {
        start_cell->pipe = START;
        start_cell->main_loop = 1;

        opposite = (moving + _DIRECTIONS_COUNT_ / 2) % _DIRECTIONS_COUNT_;

        row += offsets[opposite].row_offset;
        column += offsets[opposite].column_offset;
        while (!(row == start_row && column == start_column))
        {
            Cell *cell = maze + IDX(row, column);

            cell->main_loop = 0;
            opposite = pipes[cell->pipe].outcoming[opposite];

            row += offsets[opposite].row_offset;
            column += offsets[opposite].column_offset;
        }
    }

    return loop_length;
}

int count_enclosed()
{
    int enclosed = 0;

    for (int row = 0; row < HEIGHT; ++row)
    {
        int intersections = 0;
        for (int column = 0; column < WIDTH; ++column)
        {
            const Cell *cell = maze + IDX(row, column);
            if (!(cell->main_loop))
            {
                enclosed += (intersections & 1);
            }
            else if (!(cell->pipe == NE || cell->pipe == SE))
            {
                ++intersections;
            }
            else
            {
                ++column;
                const Cell *corner = cell + 1;
                for (
                    ;
                    !(corner->pipe == NW || corner->pipe == SW);
                    ++column, ++corner)
                {
                    ;
                }

                if ((cell->pipe == NE && corner->pipe == SW) ||
                    (cell->pipe == SE && corner->pipe == NW))
                {
                    ++intersections;
                }
            }
        }
    }

    return enclosed;
}

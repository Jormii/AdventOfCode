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
#define SOLUTION (5016002)

#define WIDTH (1002)
#define HEIGHT (15002)
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

Pipe maze[MAZE_SIZE];
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

    int farthest = loop_length / 2;

    fclose(file);

    int success = farthest == SOLUTION;
    printf("Solution: %d (%d)\n", farthest, success);

    return (success) ? 0 : 1;
}

void parse_row(int row, char *out_c, FILE *file)
{
    char c = *out_c;
    Pipe *pipe = maze + IDX(row, 0);
    for (int column = 0; column < WIDTH; ++column, ++pipe)
    {
        switch (c)
        {
        case 'S':
            start_row = row;
            start_column = column;

            *pipe = START;
            break;
        case '.':
            *pipe = GROUND;
            break;
        case '|':
            *pipe = VERTICAL;
            break;
        case '-':
            *pipe = HORIZONTAL;
            break;
        case 'L':
            *pipe = NE;
            break;
        case 'J':
            *pipe = NW;
            break;
        case '7':
            *pipe = SW;
            break;
        case 'F':
            *pipe = SE;
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

    maze[IDX(start_row, start_column)] = start_pipe;

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
            Pipe pipe = maze[IDX(row, column)];
            if (pipe == GROUND || !(pipes[pipe].compatible[moving]))
            {
                loop_length = MAZE_SIZE;
            }
            else
            {
                ++loop_length;

                moving = pipes[pipe].outcoming[moving];

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
        maze[IDX(start_row, start_column)] = START;
    }

    return loop_length;
}

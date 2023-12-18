#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (109939)

#define WIDTH (100)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (101231625)

#define WIDTH (1000)
#endif

typedef struct ParsedRow_st
{
    int sum, rocks_count;
} ParsedRow;

int to_occupy[WIDTH];

ParsedRow parse_row(int row, char *out_c, FILE *file);

int main()
{
    FILE *file = fopen(INPUT, "r");

    for (int i = 0; i < WIDTH; ++i)
    {
        to_occupy[i] = 0;
    }

    int sum = 0;
    int rock_count = 0;
    char c = fgetc(file);
    for (int row = 0; c != EOF; ++row)
    {
        ParsedRow parsed_row = parse_row(row, &c, file);

        sum += rock_count + parsed_row.sum;
        rock_count += parsed_row.rocks_count;
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %d (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

ParsedRow parse_row(int row, char *out_c, FILE *file)
{
    char c = *out_c;
    ParsedRow parsed_row = {.sum = 0, .rocks_count = 0};
    for (int i = 0; i < WIDTH; ++i, c = fgetc(file))
    {
        if (c == '#')
        {
            to_occupy[i] = row + 1;
        }
        else if (c == 'O')
        {
            parsed_row.rocks_count += 1;
            parsed_row.sum += row - to_occupy[i] + 1;

            to_occupy[i] += 1;
        }
    }

    *out_c = fgetc(file);
    return parsed_row;
}

#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (33183)

#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define WIDTH (18)
#define HEIGHT (18)
#define PATTERN_SIZE (WIDTH * HEIGHT)
#define IDX(row, width, col) ((width) * (row) + (col))

int solve_pattern(char *out_c, FILE *file);

int main()
{
    FILE *file = fopen(INPUT, "r");

    int sum = 0;
    char c = fgetc(file);
    while (c != EOF)
    {
        sum += solve_pattern(&c, file);
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %d (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

int solve_pattern(char *out_c, FILE *file)
{
    char c = *out_c;
    char pattern[PATTERN_SIZE];

    int idx = 0;
    int width = 0;
    for (; c != '\n'; ++idx, ++width, c = fgetc(file))
    {
        pattern[idx] = c;
    }
    c = fgetc(file);

    int height = 1;
    for (; c != '\n' && c != EOF; ++height, c = fgetc(file))
    {
        for (int col = 0; col < width; ++idx, ++col, c = fgetc(file))
        {
            pattern[idx] = c;
        }
    }

    int solution = 0;

    for (int col = 0; col < (width - 1); ++col)
    {
        int differences = 0;
        for (int row = 0; row < height; ++row)
        {
            for (
                int left = col, right = col + 1;
                left >= 0 && right < width;
                --left, ++right)
            {
                differences += pattern[IDX(row, width, left)] != pattern[IDX(row, width, right)];
            }
        }

        if (differences == 1)
        {
            solution += col + 1;
        }
    }

    for (int row = 0; row < (height - 1); ++row)
    {
        int differences = 0;
        for (int col = 0; col < width; ++col)
        {
            for (
                int above = row, below = row + 1;
                above >= 0 && below < height;
                --above, ++below)
            {
                differences += pattern[IDX(above, width, col)] != pattern[IDX(below, width, col)];
            }
        }

        if (differences == 1)
        {
            solution += 100 * (row + 1);
        }
    }

    *out_c = fgetc(file);
    return solution;
}

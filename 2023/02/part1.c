#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (2406)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (71327370192)
#endif

#define R_TOTAL (12)
#define G_TOTAL (13)
#define B_TOTAL (14)

typedef struct RGB_st
{
    int r, g, b;
} RGB;

RGB parse_set(char *out_c, FILE *file);

int main()
{
    FILE *file = fopen(INPUT, "r");

    long sum = 0;
    char c = fgetc(file);
    for (int game = 1; c != EOF; ++game)
    {
        while (c != ':')
        {
            c = fgetc(file);
        }
        fgetc(file);
        c = fgetc(file);

        int possible = 1;
        while (possible && c != '\n')
        {
            RGB set = parse_set(&c, file);
            possible = set.r <= R_TOTAL && set.g <= G_TOTAL && set.b <= B_TOTAL;

            if (c == ';')
            {
                fgetc(file);
                c = fgetc(file);
            }
        }

        if (possible)
        {
            sum += game;
        }

        while (c != '\n')
        {
            c = fgetc(file);
        }
        c = fgetc(file);
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %ld (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

RGB parse_set(char *out_c, FILE *file)
{
    char c = *out_c;
    RGB set = {.r = 0, .g = 0, .b = 0};

    while (1)
    {
        int tens = 0;
        int units = c - '0';

        c = fgetc(file);
        if (c != ' ')
        {
            tens = units;
            units = c - '0';

            c = fgetc(file);
        }
        c = fgetc(file);

        int balls = 10 * tens + units;
        switch (c)
        {
        case 'r':
            set.r = balls;
            break;
        case 'g':
            set.g = balls;
            break;
        case 'b':
            set.b = balls;
            break;
        default:
            break;
        }

        while (!(c == ',' || c == ';' || c == '\n'))
        {
            c = fgetc(file);
        }

        if (c == ',')
        {
            fgetc(file);
            c = fgetc(file);
        }
        else if (c == ';' || c == '\n')
        {
            break;
        }
    }

    *out_c = c;
    return set;
}

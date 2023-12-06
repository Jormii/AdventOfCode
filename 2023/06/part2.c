#include <math.h>
#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (46561107)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

typedef struct Race_st
{
    long time, distance;
} Race;

int solve(const Race *race);
long parse_row(char *out_c, FILE *file);

int main()
{
    FILE *file = fopen(INPUT, "r");

    char c = fgetc(file);
    Race race = {
        .time = parse_row(&c, file),
        .distance = parse_row(&c, file)};

    int solution = solve(&race);

    fclose(file);

    int success = solution == SOLUTION;
    printf("Solution: %d (%d)\n", solution, success);

    return (success) ? 0 : 1;
}

int solve(const Race *race)
{
    double sqr_root = sqrt(race->time * race->time - 4 * race->distance);
    double left_root = 0.5 * (race->time - sqr_root);
    double right_root = 0.5 * (race->time + sqr_root);

    int least = (int)left_root + 1;
    int most = (int)right_root;

    most -= (most * (race->time - most)) == race->distance;

    return most - least + 1;
}

long parse_row(char *out_c, FILE *file)
{
#define DIGITS_LEN (16)

    int digits_count = 0;
    char digits[DIGITS_LEN];

    char c = *out_c;
    while (!CHAR_IS_NUM(c))
    {
        c = fgetc(file);
    }
    while (c != '\n')
    {
        if (CHAR_IS_NUM(c))
        {
            digits[digits_count++] = c - '0';
        }
        c = fgetc(file);
    }

    long number = 0;
    long power_of_ten = 1;
    for (int i = digits_count - 1; i >= 0; --i)
    {
        number += digits[i] * power_of_ten;
        power_of_ten *= 10;
    }

    *out_c = c;
    return number;
}

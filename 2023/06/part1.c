#include <math.h>
#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (160816)

#define RACES_COUNT (4)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

typedef struct Race_st
{
    int time, distance;
} Race;

int solve(const Race *race);
int parse_number(char *out_c, FILE *file);

int main()
{
    FILE *file = fopen(INPUT, "r");

    char c = fgetc(file);
    Race races[RACES_COUNT];
    for (int i = 0; i < RACES_COUNT; ++i)
    {
        while (!CHAR_IS_NUM(c))
        {
            c = fgetc(file);
        }

        races[i].time = parse_number(&c, file);
    }

    for (int i = 0; i < RACES_COUNT; ++i)
    {
        while (!CHAR_IS_NUM(c))
        {
            c = fgetc(file);
        }

        races[i].distance = parse_number(&c, file);
    }

    int product = 1;
    for (int i = 0; i < RACES_COUNT; ++i)
    {
        product *= solve(races + i);
    }

    fclose(file);

    int success = product == SOLUTION;
    printf("Solution: %d (%d)\n", product, success);

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

int parse_number(char *out_c, FILE *file)
{
#define DIGITS_LEN (4)

    char digits[DIGITS_LEN];

    char c = *out_c;
    int digits_count = 0;
    while (CHAR_IS_NUM(c))
    {
        digits[digits_count++] = c - '0';
        c = fgetc(file);
    }

    int number = 0;
    int power_of_ten = 1;
    for (int i = digits_count - 1; i >= 0; --i)
    {
        number += digits[i] * power_of_ten;
        power_of_ten *= 10;
    }

    *out_c = c;
    return number;
}

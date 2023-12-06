/**
 * SOLUTION = 1181555926
 */

#include <stdio.h>

#define SEED_COUNT (20)
#define MIN(x, y) (((x) <= (y)) ? (x) : (y))
#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

typedef struct Value_st
{
    int mapped;
    long number;
} Value;

typedef struct Mapping_st
{
    long to, from, range;
} Mapping;

long parse_number(char *out_c, FILE *file);
Mapping parse_row(char *out_c, FILE *file);

int main()
{
    FILE *file = fopen("input.txt", "r");

    char c = fgetc(file);
    while (c != ':')
    {
        c = fgetc(file);
    }
    fgetc(file);
    c = fgetc(file);

    Value arr[SEED_COUNT];
    for (int i = 0; i < SEED_COUNT; ++i)
    {
        arr[i].number = parse_number(&c, file);
        c = fgetc(file);
    }

    while (c != EOF)
    {
        while (c != ':')
        {
            c = fgetc(file);
        }
        fgetc(file);
        c = fgetc(file);

        for (int i = 0; i < SEED_COUNT; ++i)
        {
            arr[i].mapped = 0;
        }

        while (c != EOF && c != '\n')
        {
            Mapping mapping = parse_row(&c, file);

            long end = mapping.from + mapping.range;
            long offset = mapping.to - mapping.from;
            for (int i = 0; i < SEED_COUNT; ++i)
            {
                Value *value = arr + i;
                if (value->number >= mapping.from && value->number < end && !(value->mapped))
                {
                    value->mapped = 1;
                    value->number += offset;
                }
            }
        }
    }

    long location = arr[0].number;
    for (int i = 1; i < SEED_COUNT; ++i)
    {
        location = MIN(location, arr[i].number);
    }

    fclose(file);
    printf("%ld\n", location);

    return 0;
}

long parse_number(char *out_c, FILE *file)
{
#define DIGITS_LEN (16)

    char digits[DIGITS_LEN];

    char c = *out_c;
    int digits_count = 0;
    while (CHAR_IS_NUM(c))
    {
        digits[digits_count++] = c - '0';
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

Mapping parse_row(char *out_c, FILE *file)
{
    char c = *out_c;

    long to = parse_number(&c, file);
    c = fgetc(file);

    long from = parse_number(&c, file);
    c = fgetc(file);

    long range = parse_number(&c, file);
    c = fgetc(file);

    *out_c = c;
    return (Mapping){.to = to, .from = from, .range = range};
}

/**
 * SOLUTION = 37806486
 */

#include <stdio.h>

#define RANGES_COUNT (10)
#define MAX_ARRLEN (2187 * RANGES_COUNT) // 3^7 * N (7=mapping sections)
#define MIN(x, y) (((x) <= (y)) ? (x) : (y))
#define MAX(x, y) (((x) >= (y)) ? (x) : (y))
#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

typedef struct Range_st
{
    int mapped;
    long begin, end;
} Range;

typedef struct Mapping_st
{
    long to, from, range;
} Mapping;

typedef struct Intersection_st
{
    int idx;
    int count;
    Range ranges[3];
} Intersection;

long parse_number(char *out_c, FILE *file);
Mapping parse_row(char *out_c, FILE *file);
Intersection intersect_ranges(long r_begin, long r_end, long m_begin, long m_end);

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

    int arrlen = 0;
    Range arr[MAX_ARRLEN];
    for (int i = 0; i < RANGES_COUNT; ++i)
    {
        long begin = parse_number(&c, file);
        c = fgetc(file);

        long range = parse_number(&c, file);
        c = fgetc(file);

        arr[arrlen].begin = begin;
        arr[arrlen].end = begin + range;
        ++arrlen;
    }

    while (c != EOF)
    {
        while (c != ':')
        {
            c = fgetc(file);
        }
        fgetc(file);
        c = fgetc(file);

        for (int i = 0; i < arrlen; ++i)
        {
            arr[i].mapped = 0;
        }

        while (c != EOF && c != '\n')
        {
            Mapping mapping = parse_row(&c, file);

            long end = mapping.from + mapping.range;
            long offset = mapping.to - mapping.from;
            for (int i = 0; i < arrlen; ++i)
            {
                Range *range = arr + i;
                if (range->mapped)
                {
                    continue;
                }

                Intersection intersection = intersect_ranges(
                    range->begin, range->end, mapping.from, end);
                if (intersection.count == 1)
                {
                    if (intersection.idx == 1)
                    {
                        range->mapped = 1;
                        range->begin += offset;
                        range->end += offset;
                    }
                }
                else
                {
                    const Range *A = intersection.ranges;
                    const Range *B = intersection.ranges + 1;
                    const Range *C = intersection.ranges + 2;

                    range->mapped = 1;
                    range->begin = B->begin + offset;
                    range->end = B->end + offset;

                    if (A->begin < A->end)
                    {
                        arr[arrlen].mapped = 0;
                        arr[arrlen].begin = A->begin;
                        arr[arrlen].end = A->end;

                        ++arrlen;
                    }
                    if (C->begin < C->end)
                    {
                        arr[arrlen].mapped = 0;
                        arr[arrlen].begin = C->begin;
                        arr[arrlen].end = C->end;

                        ++arrlen;
                    }
                }
            }
        }
    }

    long location = arr[0].begin;
    for (int i = 1; i < arrlen; ++i)
    {
        location = MIN(location, arr[i].begin);
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

Intersection intersect_ranges(long r_begin, long r_end, long m_begin, long m_end)
{
    Intersection intersection = {.idx = -1, .count = 0};

    intersection.ranges[0].begin = r_begin;
    intersection.ranges[0].end = MIN(m_begin, r_end);

    intersection.ranges[1].begin = MAX(m_begin, r_begin);
    intersection.ranges[1].end = MIN(m_end, r_end);

    intersection.ranges[2].begin = MAX(m_end, r_begin);
    intersection.ranges[2].end = r_end;

    for (int i = 0; i < 3; ++i)
    {
        const Range *range = intersection.ranges + i;
        if (range->begin < range->end)
        {
            intersection.idx = i;
            intersection.count += 1;
        }
    }

    return intersection;
}

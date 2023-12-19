#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (7025)

#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define GROUPS_LEN (6)
#define SPRINGS_LEN (20)

int groups[GROUPS_LEN];
char springs[SPRINGS_LEN];
int groups_len, springs_len;

void parse_row(char *out_c, FILE *file);
int advance(int springs_idx);
int arrangements(int springs_idx, int groups_idx);

int main()
{
    FILE *file = fopen(INPUT, "r");

    int sum = 0;
    char c = fgetc(file);
    while (c != EOF)
    {
        parse_row(&c, file);
        sum += arrangements(advance(0), 0);
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %d (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

void parse_row(char *out_c, FILE *file)
{
    char c = *out_c;
    groups_len = springs_len = 0;

    for (; c != ' '; c = fgetc(file))
    {
        springs[springs_len++] = c;
    }

    while (c != '\n')
    {
        c = fgetc(file);

        int number = 0;
        for (; c != ',' && c != '\n'; c = fgetc(file))
        {
            number = 10 * number + (c - '0');
        }

        groups[groups_len++] = number;
    }

    *out_c = fgetc(file);
}

int advance(int springs_idx)
{
    for (
        ;
        springs_idx < springs_len && springs[springs_idx] == '.';
        ++springs_idx)
    {
    }

    return springs_idx;
}

int arrangements(int springs_idx, int groups_idx)
{
    if (groups_idx == groups_len)
    {
        int correct = 1;
        for (int i = springs_idx; correct && i < springs_len; ++i)
        {
            correct = springs[i] != '#';
        }

        return correct;
    }

    int arrange = 0;
    int end = springs_idx + groups[groups_idx];
    if (end <= springs_len)
    {
        int correct = 1;
        if (end < springs_len)
        {
            correct = springs[end] != '#';
        }
        for (int i = springs_idx; correct && i < end; ++i)
        {
            correct = springs[i] != '.';
        }

        if (correct)
        {
            arrange += arrangements(advance(end + 1), groups_idx + 1);
        }
        if (springs[springs_idx] == '?')
        {
            arrange += arrangements(advance(springs_idx + 1), groups_idx);
        }
    }

    return arrange;
}

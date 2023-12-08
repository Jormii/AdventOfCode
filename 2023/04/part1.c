#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (20117)

#define WINNING_NUMBERS (10)
#define PLAYING_NUMBERS (25)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (1475828)

#define WINNING_NUMBERS (20)
#define PLAYING_NUMBERS (50)
#endif

int winning[WINNING_NUMBERS];
int playing[PLAYING_NUMBERS];

void parse_row(char *out_c, FILE *file);
void insert_ordered(int number, int *array, int arrlen);

int main()
{
    FILE *file = fopen(INPUT, "r");

    int sum = 0;
    char c = fgetc(file);
    while (c != EOF)
    {
        parse_row(&c, file);

        int won = 0;
        int winning_idx = 0;
        int playing_idx = 0;
        while (winning_idx < WINNING_NUMBERS && playing_idx < PLAYING_NUMBERS)
        {
            int winning_number = winning[winning_idx];
            int playing_number = playing[playing_idx];

            if (winning_number == playing_number)
            {
                ++won;
                ++winning_idx;
                ++playing_idx;
            }
            else if (winning_number < playing_number)
            {
                ++winning_idx;
            }
            else
            {
                ++playing_idx;
            }
        }

        sum += 1 << (won - 1);
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %d (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

void parse_row(char *out_c, FILE *file)
{
    char c = *out_c;

    while (c != ':')
    {
        c = fgetc(file);
    }
    fgetc(file);
    c = fgetc(file);

    for (int i = 0; i < WINNING_NUMBERS; ++i)
    {
        char tens = (c == ' ') ? 0 : (c - '0');
        char units = fgetc(file) - '0';

        insert_ordered(10 * tens + units, winning, i);

        fgetc(file);
        c = fgetc(file);
    }

    fgetc(file);
    c = fgetc(file);

    for (int i = 0; i < PLAYING_NUMBERS; ++i)
    {
        char tens = (c == ' ') ? 0 : (c - '0');
        char units = fgetc(file) - '0';

        insert_ordered(10 * tens + units, playing, i);

        fgetc(file);
        c = fgetc(file);
    }

    *out_c = c;
}

void insert_ordered(int number, int *array, int arrlen)
{
    int ins_idx = 0;
    while (array[ins_idx] < number && ins_idx < arrlen)
    {
        ++ins_idx;
    }

    for (int i = arrlen; i > ins_idx; --i)
    {
        array[i] = array[i - 1];
    }
    array[ins_idx] = number;
}

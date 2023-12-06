#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (84399773)

#define SCHEMATIC_WIDTH (140)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (17158526595)

#define SCHEMATIC_WIDTH (5000)
#endif

#define NO_CHAR (-1)
#define ADJ_LIMIT (2)
#define ROWS_COUNT (4)
#define MIN(x, y) (((x) <= (y)) ? (x) : (y))
#define MAX(x, y) (((x) >= (y)) ? (x) : (y))
#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

typedef struct Cell_st
{
    char character; // Or digit
    int number_begin, number_end;

    unsigned char adj_count;
    const struct Cell_st *adjacent[ADJ_LIMIT];
    const struct Cell_st *adjacent_row[ADJ_LIMIT];
} Cell;

void clear_row(Cell *row);
void parse_row(Cell *row, Cell *upper_row, Cell *lower_row, char *out_c, FILE *file);

long calculate_row_sum(const Cell *row);
int parse_cell_number(const Cell *cell, const Cell *row);

int main()
{
    FILE *file = fopen(INPUT, "r");

    Cell rows[ROWS_COUNT][SCHEMATIC_WIDTH];
    for (int i = 0; i < ROWS_COUNT - 1; ++i)
    {
        clear_row(rows[i]);
    }

    char c = fgetc(file);
    parse_row(rows[0], rows[3], rows[1], &c, file);
    parse_row(rows[1], rows[0], rows[2], &c, file);

    int i = 2;
    long sum = 0;
    for (; c != EOF; ++i)
    {
        Cell *to_calculate = rows[(i - 2) % ROWS_COUNT];
        sum += calculate_row_sum(to_calculate);

        Cell *row = rows[i % ROWS_COUNT];
        Cell *upper_row = rows[(i - 1) % ROWS_COUNT];
        Cell *lower_row = rows[(i + 1) % ROWS_COUNT];

        clear_row(lower_row);
        parse_row(row, upper_row, lower_row, &c, file);
    }
    sum += calculate_row_sum(rows[(i - 2) % ROWS_COUNT]);
    sum += calculate_row_sum(rows[(i - 1) % ROWS_COUNT]);

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %ld (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

void clear_row(Cell *row)
{
    for (int i = 0; i < SCHEMATIC_WIDTH; ++i)
    {
        Cell *cell = row + i;

        cell->adj_count = 0;
        cell->character = NO_CHAR;
    }
}

void parse_row(Cell *row, Cell *upper_row, Cell *lower_row, char *out_c, FILE *file)
{
    char c = *out_c;
    Cell *rows[3] = {row, upper_row, lower_row};

    for (int i = 0; i < SCHEMATIC_WIDTH; ++i)
    {
        if (CHAR_IS_NUM(c))
        {
            int number_begin = i;
            int number_end = number_begin;

            for (; CHAR_IS_NUM(c); ++i, ++number_end)
            {
                row[i].character = c - '0';
                row[i].number_begin = number_begin;

                c = fgetc(file);
            }

            for (i = number_begin; i < number_end; ++i)
            {
                row[i].number_end = number_end;
            }

            for (int j = MAX(0, number_begin - 1); j < MIN(number_end + 1, SCHEMATIC_WIDTH); ++j)
            {
                for (int r = 0; r < 3; ++r)
                {
                    Cell *cell = rows[r] + j;

                    if (cell->adj_count < ADJ_LIMIT)
                    {
                        cell->adjacent_row[cell->adj_count] = row;
                        cell->adjacent[cell->adj_count] = row + number_begin;
                    }
                    cell->adj_count += 1;
                }
            }

            --i;
        }
        else
        {
            row[i].character = c;

            c = fgetc(file);
        }
    }

    *out_c = fgetc(file);
}

long calculate_row_sum(const Cell *row)
{
    long row_sum = 0;
    for (int i = 0; i < SCHEMATIC_WIDTH; ++i)
    {
        const Cell *cell = row + i;
        if (cell->character == '*' && cell->adj_count == ADJ_LIMIT)
        {
            row_sum += parse_cell_number(cell->adjacent[0], cell->adjacent_row[0]) *
                       parse_cell_number(cell->adjacent[1], cell->adjacent_row[1]);
        }
    }

    return row_sum;
}

int parse_cell_number(const Cell *cell, const Cell *row)
{
    int number = 0;
    int power_of_ten = 1;
    for (int i = cell->number_end - 1; i >= cell->number_begin; --i)
    {
        number += row[i].character * power_of_ten;
        power_of_ten *= 10;
    }

    return number;
}

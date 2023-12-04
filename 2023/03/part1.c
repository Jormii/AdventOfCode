/**
 * SOLUTION = 526404
 */

#include <stdio.h>

#define NO_NUM (-1)
#define ROWS_COUNT (3)
#define SCHEMATIC_WIDTH (410)
#define MIN(x, y) (((x) <= (y)) ? (x) : (y))
#define MAX(x, y) (((x) >= (y)) ? (x) : (y))
#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

typedef struct Cell_st
{
    char digit;
    unsigned char symbol_count;
    unsigned char number_begin, number_end;
} Cell;

void clear_row(Cell *row);
void parse_row(Cell *row, Cell *upper_row, Cell *lower_row, char *out_c, FILE *file);

int calculate_row_sum(const Cell *row);
int parse_cell_number(const Cell *cell, const Cell *row);

int main()
{
    FILE *file = fopen("input.txt", "r");

    Cell rows[ROWS_COUNT][SCHEMATIC_WIDTH];
    for (int i = 0; i < ROWS_COUNT - 1; ++i)
    {
        clear_row(rows[i]);
    }

    char c = fgetc(file);
    parse_row(rows[0], rows[2], rows[1], &c, file);

    int i = 1;
    int sum = 0;
    for (; c != EOF; ++i)
    {
        Cell *row = rows[i % ROWS_COUNT];
        Cell *upper_row = rows[(i - 1) % ROWS_COUNT];
        Cell *lower_row = rows[(i + 1) % ROWS_COUNT];

        clear_row(lower_row);
        parse_row(row, upper_row, lower_row, &c, file);
        sum += calculate_row_sum(upper_row);
    }
    sum += calculate_row_sum(rows[(i - 1) % ROWS_COUNT]);

    fclose(file);
    printf("%d\n", sum);

    return 0;
}

void clear_row(Cell *row)
{
    for (int i = 0; i < SCHEMATIC_WIDTH; ++i)
    {
        Cell *cell = row + i;

        cell->digit = NO_NUM;
        cell->symbol_count = 0;
    }
}

void parse_row(Cell *row, Cell *upper_row, Cell *lower_row, char *out_c, FILE *file)
{
    char c = *out_c;
    for (int i = 0; i < SCHEMATIC_WIDTH; ++i)
    {
        if (CHAR_IS_NUM(c))
        {
            unsigned char number_begin = i;
            unsigned char number_end = number_begin;

            for (; CHAR_IS_NUM(c); ++i, ++number_end)
            {
                row[i].digit = c - '0';
                row[i].number_begin = number_begin;

                c = fgetc(file);
            }

            for (i = number_begin; i < number_end; ++i)
            {
                row[i].number_end = number_end;
            }
            --i;
        }
        else
        {
            if (c != '.')
            {
                for (int j = MAX(0, i - 1); j < MIN(i + 2, SCHEMATIC_WIDTH); ++j)
                {
                    upper_row[j].symbol_count += 1;
                    row[j].symbol_count += 1;
                    lower_row[j].symbol_count += 1;
                }
            }

            c = fgetc(file);
        }
    }

    *out_c = fgetc(file);
}

int calculate_row_sum(const Cell *row)
{
    int row_sum = 0;
    for (int i = 0; i < SCHEMATIC_WIDTH; ++i)
    {
        const Cell *cell = row + i;
        if (cell->symbol_count != 0 && cell->digit != NO_NUM)
        {
            row_sum += parse_cell_number(cell, row);
            i = cell->number_end - 1;
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
        number += row[i].digit * power_of_ten;
        power_of_ten *= 10;
    }

    return number;
}

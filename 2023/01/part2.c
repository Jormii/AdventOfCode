/**
 * SOLUTION = 55652
 */

#include <stdio.h>

#define NO_NUM (-1)
#define BUFFER_SIZE (64)
#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

const char *DIGITS_STR[] = {
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"};

int buffer_length = 0;
char buffer[BUFFER_SIZE];

int get_num(int buffer_idx);
int is_digit_str(int digit, int buffer_idx, int offset);

int main()
{
    FILE *file = fopen("input.txt", "r");

    int sum = 0;
    char c = fgetc(file);
    while (c != EOF)
    {
        buffer_length = 0;
        while (c != '\n')
        {
            buffer[buffer_length++] = c;
            c = fgetc(file);
        }

        c = fgetc(file);
        buffer[buffer_length] = '\0';

        int i = 0;
        int first = NO_NUM;
        for (; first == NO_NUM; ++i)
        {
            first = get_num(i);
        }

        int last = first;
        for (; i < buffer_length; ++i)
        {
            int tmp = get_num(i);
            if (tmp != NO_NUM)
            {
                last = tmp;
            }
        }

        sum += 10 * first + last;
    }

    fclose(file);
    printf("%d\n", sum);

    return 0;
}

int get_num(int buffer_idx)
{
    char c = buffer[buffer_idx];
    if (CHAR_IS_NUM(c))
    {
        return c - '0';
    }

    int number = NO_NUM;
    char c2 = buffer[buffer_idx + 1];
    switch (c)
    {
    case 'o':
        number = is_digit_str(1, buffer_idx, 1);
        break;
    case 't':
    {
        switch (c2)
        {
        case 'w':
            number = is_digit_str(2, buffer_idx, 2);
            break;
        case 'h':
            number = is_digit_str(3, buffer_idx, 2);
            break;
        default:
            break;
        }
    }
    break;
    case 'f':
        switch (c2)
        {
        case 'o':
            number = is_digit_str(4, buffer_idx, 2);
            break;
        case 'i':
            number = is_digit_str(5, buffer_idx, 2);
            break;
        default:
            break;
        }
        break;
    case 's':
        switch (c2)
        {
        case 'i':
            number = is_digit_str(6, buffer_idx, 2);
            break;
        case 'e':
            number = is_digit_str(7, buffer_idx, 2);
            break;
        default:
            break;
        }
        break;
    case 'e':
        number = is_digit_str(8, buffer_idx, 1);
        break;
    case 'n':
        number = is_digit_str(9, buffer_idx, 1);
        break;
    default:
        break;
    }

    return number;
}

int is_digit_str(int digit, int buffer_idx, int offset)
{
    const char *b = buffer + (buffer_idx + offset);
    const char *d = DIGITS_STR[digit - 1] + offset;
    for (; *d && (*b == *d); ++b, ++d)
    {
        ;
    }

    if (*d != '\0')
    {
        return NO_NUM;
    }
    else
    {
        return digit;
    }
}

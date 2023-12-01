// TODO: FIX ME. Ex: Twone
// 64 char buffer

#include <stdio.h>

#define NO_NUM (-1)
#define CHAR_IS_NUM(_c) ((_c) >= '0' && (_c) <= '9')
#define STRLEN(str) (sizeof((str)) / sizeof((str)[0]))

#define NUM_F(fname) int fname(int c, FILE *file, int *out_number)

int DIGITS[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

NUM_F(get_num);
NUM_F(get_two_or_three);
NUM_F(get_four_or_five);
NUM_F(get_six_or_seven);
int get_alphabetic_num(int c, FILE *file, int *out_number,
                       int value, const char *str, int strlen);

int ffgetc(FILE *file)
{
    int c = fgetc(file);
    printf("%c", c);
    fflush(stdout);

    return c;
}

NUM_F(get_num)
{
    *out_number = NO_NUM;

    switch (c)
    {
    case 'o':
        c = get_alphabetic_num(c, file, out_number, 1, "ne", 2);
        break;
    case 't':
        c = get_two_or_three(c, file, out_number);
        break;
    case 'f':
        c = get_four_or_five(c, file, out_number);
        break;
    case 's':
        c = get_six_or_seven(c, file, out_number);
        break;
    case 'e':
        c = get_alphabetic_num(c, file, out_number, 8, "ight", 4);
        break;
    case 'n':
        c = get_alphabetic_num(c, file, out_number, 9, "ine", 3);
        break;
    default:
    {
        if (!CHAR_IS_NUM(c))
        {
            c = ffgetc(file);
        }
        else
        {
            *out_number = DIGITS[c - '0'];
        }
    }
    break;
    }

    if (*out_number != NO_NUM)
    {
        c = ffgetc(file);
    }
    return c;
}

NUM_F(get_two_or_three)
{
    // We know c='t'
    c = ffgetc(file);
    switch (c)
    {
    case 'w':
        return get_alphabetic_num(c, file, out_number, 2, "o", 1);
    case 'h':
        return get_alphabetic_num(c, file, out_number, 3, "ree", 3);
    default:
        return c;
    }
}

NUM_F(get_four_or_five)
{
    // We know c='f'
    c = ffgetc(file);
    switch (c)
    {
    case 'o':
        return get_alphabetic_num(c, file, out_number, 4, "ur", 2);
    case 'i':
        return get_alphabetic_num(c, file, out_number, 5, "ve", 2);
    default:
        return c;
    }
}

NUM_F(get_six_or_seven)
{
    // We know c='s'
    c = ffgetc(file);
    switch (c)
    {
    case 'i':
        return get_alphabetic_num(c, file, out_number, 6, "x", 1);
    case 'e':
        return get_alphabetic_num(c, file, out_number, 7, "ven", 3);
    default:
        return c;
    }
}

int get_alphabetic_num(int c, FILE *file, int *out_number,
                       int value, const char *str, int strlen)
{
    for (int i = 0; i < strlen; ++i)
    {
        c = ffgetc(file);
        if (c != str[i])
        {
            return c;
        }
    }

    *out_number = value;
    return c;
}

int main()
{
    FILE *file = fopen("two1nine", "r");

    int sum = 0;
    int c = ffgetc(file);
    while (c != EOF)
    {
        int first;
        c = get_num(c, file, &first);
        while (first == NO_NUM)
        {
            c = get_num(c, file, &first);
        }

        int last = first;

        while (c != '\n')
        {
            int tmp;
            c = get_num(c, file, &tmp);
            if (tmp != NO_NUM)
            {
                last = tmp;
            }
        }
        printf("%d %d\n\n", first, last);
        c = ffgetc(file);

        sum += 10 * first + last;
    }

    fclose(file);
    printf("%d\n", sum);

    return 0;
}

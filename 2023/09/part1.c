#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (1974913025)

#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define BUFFER_LEN (128)
#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

int buffer[BUFFER_LEN];

int predict(char *out_c, FILE *file);

int main()
{
    FILE *file = fopen(INPUT, "r");

    int sum = 0;
    char c = fgetc(file);
    while (c != EOF)
    {
        sum += predict(&c, file);
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %d (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

int predict(char *out_c, FILE *file)
{
    char c = *out_c;

    int arrlen = 0;
    while (1)
    {
        int sign = 1;
        int number = 0;
        if (c == '-')
        {
            sign = -1;
            c = fgetc(file);
        }
        while (CHAR_IS_NUM(c))
        {
            number = 10 * number + (c - '0');
            c = fgetc(file);
        }

        buffer[arrlen++] = sign * number;

        if (c == '\n')
        {
            break;
        }
        c = fgetc(file);
    }

    int step = 0;
    while (1)
    {
        int begin = 0;
        int end = arrlen - step - 1;
        int all_zeros = buffer[end] == 0;
        for (int i = begin; i < end; ++i)
        {
            all_zeros &= buffer[i] == 0;
            buffer[i] = buffer[i + 1] - buffer[i];
        }

        if (all_zeros)
        {
            break;
        }
        ++step;
    }

    int prediction = buffer[arrlen - step];
    for (int i = step - 1; i > 0; --i)
    {
        int end = arrlen - i;
        prediction += buffer[end];
    }

    *out_c = fgetc(file);
    return prediction;
}

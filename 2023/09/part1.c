#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (1974913025)

#define BUFFER_LEN (128)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (8137764536324356)

#define BUFFER_LEN (512)
#endif

#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

long buffer[BUFFER_LEN];

long predict(char *out_c, FILE *file);

int main()
{
    FILE *file = fopen(INPUT, "r");

    long sum = 0;
    char c = fgetc(file);
    while (c != EOF)
    {
        sum += predict(&c, file);
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %ld (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

long predict(char *out_c, FILE *file)
{
    char c = *out_c;

    int arrlen = 0;
    while (1)
    {
        int sign = 1;
        long number = 0;
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

    long prediction = buffer[arrlen - step];
    for (int i = step - 1; i > 0; --i)
    {
        int end = arrlen - i;
        prediction += buffer[end];
    }

    *out_c = fgetc(file);
    return prediction;
}

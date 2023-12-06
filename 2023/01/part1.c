#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (56108)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (55022487)
#endif

#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

int main()
{
    FILE *file = fopen(INPUT, "r");

    int sum = 0;
    char c = fgetc(file);
    while (c != EOF)
    {
        while (!CHAR_IS_NUM(c))
        {
            c = fgetc(file);
        }

        int first = c;
        int last = first;

        c = fgetc(file);
        while (c != '\n')
        {
            if (CHAR_IS_NUM(c))
            {
                last = c;
            }

            c = fgetc(file);
        }
        c = fgetc(file);

        sum += 10 * (first - '0') + (last - '0');
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %d (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

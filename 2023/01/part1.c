/**
 * SOLUTION = 56108
 */

#include <stdio.h>

#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

int main()
{
    FILE *file = fopen("input.txt", "r");
    int DIGITS[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

    int sum = 0;
    int c = fgetc(file);
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

        sum += 10 * DIGITS[first - '0'] + DIGITS[last - '0'];
    }

    fclose(file);
    printf("%d\n", sum);

    return 0;
}

#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (495972)

#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

int calculate_hash(char *out_c, FILE *file);

int main()
{
    FILE *file = fopen(INPUT, "r");

    int sum = 0;
    char c = fgetc(file);
    while (1)
    {
        sum += calculate_hash(&c, file);

        if (c == EOF)
        {
            break;
        }
        else
        {
            c = fgetc(file);
        }
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %d (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

int calculate_hash(char *out_c, FILE *file)
{
    int hash = 0;
    char c = *out_c;
    for (; c != ',' && c != EOF; c = fgetc(file))
    {
        hash = (17 * (hash + c)) % 256;
    }

    *out_c = c;
    return hash;
}

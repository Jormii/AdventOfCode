#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (-1)

#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

int main()
{
    FILE *file = fopen(INPUT, "r");

    char c = fgetc(file);

    fclose(file);

    int success = solution == SOLUTION;
    printf("Solution: %d (%d)\n", solution, success);

    return (success) ? 0 : 1;
}

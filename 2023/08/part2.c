#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (11795205644011)

#define INSTRUCTIONS_ARRLEN (512)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (2214154416012)

#define INSTRUCTIONS_ARRLEN (2 << 20)
#endif

#define BASE ('Z' - 'A' + 1)
#define NODES_ARRLEN (BASE * BASE * BASE)
#define STARTING_INDICES_ARRLEN (BASE * BASE)
#define MIN(x, y) (((x) <= (y)) ? (x) : (y))
#define MAX(x, y) (((x) >= (y)) ? (x) : (y))

typedef enum Direction_en
{
    LEFT = 0,
    RIGHT = 1
} Direction;

typedef union Node_un
{
    int indices[2];
    struct
    {
        int left, right;
    };
} Node;

Node nodes[NODES_ARRLEN];
Direction instructions[INSTRUCTIONS_ARRLEN];

int parse_instructions(char *out_c, FILE *file);
int parse_node(char *out_c, FILE *file);
long lcm(int idx, const int *arr, int arrlen); // I didn't come up with this

int main()
{
    FILE *file = fopen(INPUT, "r");

    char c = fgetc(file);
    int indices_arrlen = 0;
    int node_indices[STARTING_INDICES_ARRLEN];

    int instructions_count = parse_instructions(&c, file);
    while (c != EOF)
    {
        int node_idx = parse_node(&c, file);
        if ((node_idx % BASE) == 0)
        {
            node_indices[indices_arrlen++] = node_idx;
        }
    }

    long steps = 0;
    int inst_idx = 0;
    for (int it_arrlen = indices_arrlen; it_arrlen != 0; ++steps)
    {
        Direction inst = instructions[inst_idx];
        for (int i = 0; i < it_arrlen; ++i)
        {
            int curr_idx = node_indices[i];
            if ((curr_idx % BASE) != ('Z' - 'A'))
            {
                node_indices[i] = nodes[curr_idx].indices[inst];
            }
            else
            {
                --it_arrlen;
                if (i != it_arrlen)
                {
                    node_indices[i] = node_indices[it_arrlen];
                }
                node_indices[it_arrlen] = steps;

                --i;
            }
        }
        inst_idx = (inst_idx + 1) % instructions_count;
    }

    steps = lcm(0, node_indices, indices_arrlen);

    fclose(file);

    int success = steps == SOLUTION;
    printf("Solution: %ld (%d)\n", steps, success);

    return (success) ? 0 : 1;
}

int parse_instructions(char *out_c, FILE *file)
{
    char c = *out_c;
    int instructions_count = 0;
    while (c != '\n')
    {
        instructions[instructions_count++] = c != 'L';
        c = fgetc(file);
    }

    fgetc(file);
    *out_c = fgetc(file);
    return instructions_count;
}

int parse_node(char *out_c, FILE *file)
{
    char c = *out_c;

    int node_idx = 0;
    for (int i = 0; i < 3; ++i)
    {
        node_idx = BASE * node_idx + (c - 'A');
        c = fgetc(file);
    }
    for (int i = 0; i < 4; ++i)
    {
        c = fgetc(file);
    }

    int left_idx = 0;
    for (int i = 0; i < 3; ++i)
    {
        left_idx = BASE * left_idx + (c - 'A');
        c = fgetc(file);
    }
    for (int i = 0; i < 2; ++i)
    {
        c = fgetc(file);
    }

    int right_idx = 0;
    for (int i = 0; i < 3; ++i)
    {
        right_idx = BASE * right_idx + (c - 'A');
        c = fgetc(file);
    }
    for (int i = 0; i < 2; ++i)
    {
        c = fgetc(file);
    }

    nodes[node_idx].left = left_idx;
    nodes[node_idx].right = right_idx;

    *out_c = c;
    return node_idx;
}

long lcm(int idx, const int *arr, int arrlen)
{
    long n = arr[idx];
    long m = arr[idx + 1];
    if ((idx + 2) != arrlen)
    {
        m = lcm(idx + 1, arr, arrlen);
    }

    long a = MAX(n, m);
    long b = MIN(n, m);
    while (b != 0)
    {
        long tmp = b;
        b = a % b;
        a = tmp;
    }

    return (n * m) / a;
}

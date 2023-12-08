#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (16409)

#define INSTRUCTIONS_ARRLEN (512)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (1488003)

#define INSTRUCTIONS_ARRLEN (2 << 20)
#endif

#define BASE ('Z' - 'A' + 1)
#define NODES_ARRLEN (BASE * BASE * BASE)

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

int main()
{
    FILE *file = fopen(INPUT, "r");

    char c = fgetc(file);
    int instructions_count = parse_instructions(&c, file);
    while (c != EOF)
    {
        parse_node(&c, file);
    }

#define ZZZ_IDX (NODES_ARRLEN - 1)
    int steps = 0;
    int inst_idx = 0;
    int node_idx = 0;
    for (; node_idx != ZZZ_IDX; ++steps)
    {
        Direction inst = instructions[inst_idx];
        node_idx = nodes[node_idx].indices[inst];
        inst_idx = (inst_idx + 1) % instructions_count;
    }

    fclose(file);

    int success = steps == SOLUTION;
    printf("Solution: %d (%d)\n", steps, success);

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

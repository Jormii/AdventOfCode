#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (446935)

#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define BASE ('z' - 'a' + 1)
#define HASMAP_SIZE (BASE * BASE * BASE)
#define IN_IDX (('i' - 'a') * BASE + ('n' - 'a'))

typedef enum Category_en
{
    CATEGORY_X,
    CATEGORY_M,
    CATEGORY_A,
    CATEGORY_S,
    _CATEGORIES_COUNT_,
} Category;

typedef enum Operation_en
{
    OP_SEND,
    OP_LESS_THAN,
    OP_GREATER_THAN,
} Operation;

typedef enum SendTo_en
{
    SEND_TO_ACCEPT,
    SEND_TO_REJECT,
    SEND_TO_WORKFLOW,
} SendTo;

typedef union Part_un
{
    struct
    {
        int x, m, a, s;
    };
    int categories[_CATEGORIES_COUNT_];
} Part;

typedef struct Rule_st
{
    int literal;
    Operation op;
    Category category;

    SendTo send_to;
    int send_to_workflow_idx;
} Rule;

typedef struct Workflow_st
{
    int rules_len;
    Rule rules[_CATEGORIES_COUNT_ + 1];
} Workflow;

Workflow hashmap[HASMAP_SIZE];

void parse_workflow(char *out_c, FILE *file);
Part parse_part(char *out_c, FILE *file);
int process_part(const Part *part);

int main()
{
    FILE *file = fopen(INPUT, "r");

    char c = fgetc(file);
    while (c != '\n')
    {
        parse_workflow(&c, file);
    }
    c = fgetc(file);

    int sum = 0;
    while (c != EOF)
    {
        Part part = parse_part(&c, file);
        if (process_part(&part))
        {
            sum += part.x + part.m + part.a + part.s;
        }
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %d (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

void parse_workflow(char *out_c, FILE *file)
{
    char c = *out_c;

    int workflow_idx = 0;
    for (; c != '{'; c = fgetc(file))
    {
        workflow_idx = workflow_idx * BASE + (c - 'a');
    }
    c = fgetc(file);

    Workflow *workflow = hashmap + workflow_idx;

    workflow->rules_len = 0;
    Rule *rule = workflow->rules;
    for (; c != '}'; ++rule)
    {
        workflow->rules_len += 1;

        char next_c = fgetc(file);
        if (c == 'A')
        {
            c = next_c;

            rule->op = OP_SEND;
            rule->send_to = SEND_TO_ACCEPT;
        }
        else if (c == 'R')
        {
            c = next_c;

            rule->op = OP_SEND;
            rule->send_to = SEND_TO_REJECT;
        }
        else if (next_c == '<' || next_c == '>')
        {
            if (c == 'x')
            {
                rule->category = CATEGORY_X;
            }
            else if (c == 'm')
            {
                rule->category = CATEGORY_M;
            }
            else if (c == 'a')
            {
                rule->category = CATEGORY_A;
            }
            else
            {
                rule->category = CATEGORY_S;
            }

            c = next_c;
            if (c == '<')
            {
                rule->op = OP_LESS_THAN;
            }
            else
            {
                rule->op = OP_GREATER_THAN;
            }

            c = fgetc(file);
            rule->literal = 0;
            for (; c != ':'; c = fgetc(file))
            {
                rule->literal = rule->literal * 10 + (c - '0');
            }
            c = fgetc(file);

            if (c == 'A')
            {
                rule->send_to = SEND_TO_ACCEPT;
            }
            else if (c == 'R')
            {
                rule->send_to = SEND_TO_REJECT;
            }
            else
            {
                rule->send_to = SEND_TO_WORKFLOW;

                rule->send_to_workflow_idx = 0;
                for (; c != ',' && c != '}'; c = fgetc(file))
                {
                    rule->send_to_workflow_idx = rule->send_to_workflow_idx * BASE + (c - 'a');
                }
            }
        }
        else
        {
            rule->op = OP_SEND;
            rule->send_to = SEND_TO_WORKFLOW;

            rule->send_to_workflow_idx = c - 'a';

            c = next_c;
            for (; c != '}'; c = fgetc(file))
            {
                rule->send_to_workflow_idx = rule->send_to_workflow_idx * BASE + (c - 'a');
            }
        }

        if (c == ',')
        {
            c = fgetc(file);
        }
        else if (c != '}')
        {
            fgetc(file);
            c = fgetc(file);
        }
    }

    fgetc(file);
    *out_c = fgetc(file);
}

Part parse_part(char *out_c, FILE *file)
{
    Part part;

    char c = fgetc(file);
    for (
        Category category = CATEGORY_X;
        category < _CATEGORIES_COUNT_;
        ++category, c = fgetc(file))
    {
        fgetc(file);
        c = fgetc(file);

        part.categories[category] = 0;
        for (; c != ',' && c != '}'; c = fgetc(file))
        {
            part.categories[category] = part.categories[category] * 10 + (c - '0');
        }
    }

    *out_c = fgetc(file);
    return part;
}

int process_part(const Part *part)
{
    int accepted = 0;
    int processing = 1;

    int rule_idx = 0;
    const Workflow *workflow = hashmap + IN_IDX;
    while (processing)
    {
        const Rule *rule = workflow->rules + rule_idx;
        if (rule->op == OP_SEND)
        {
            if (rule->send_to == SEND_TO_ACCEPT)
            {
                accepted = 1;
                processing = 0;
            }
            else if (rule->send_to == SEND_TO_REJECT)
            {
                accepted = 0;
                processing = 0;
            }
            else
            {
                rule_idx = 0;
                workflow = hashmap + rule->send_to_workflow_idx;
            }
        }
        else
        {
            int true = 0;
            if (rule->op == OP_LESS_THAN)
            {
                true = part->categories[rule->category] < rule->literal;
            }
            else
            {
                true = part->categories[rule->category] > rule->literal;
            }

            if (!true)
            {
                ++rule_idx;
            }
            else
            {
                if (rule->send_to == SEND_TO_ACCEPT)
                {
                    accepted = 1;
                    processing = 0;
                }
                else if (rule->send_to == SEND_TO_REJECT)
                {
                    accepted = 0;
                    processing = 0;
                }
                else
                {
                    rule_idx = 0;
                    workflow = hashmap + rule->send_to_workflow_idx;
                }
            }
        }
    }

    return accepted;
}

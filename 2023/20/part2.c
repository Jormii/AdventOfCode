#include <stdio.h>
#include <stdlib.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (247702167614647)

#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define INPUTS_LEN (16)
#define OUTPUTS_LEN (8)
#define BASE ('z' - 'a' + 1)
#define MODULES_LEN (BASE * BASE)
#define RX_INDEX (('r' - 'a') * BASE + ('x' - 'a'))
#define MIN(x, y) (((x) <= (y)) ? (x) : (y))
#define MAX(x, y) (((x) >= (y)) ? (x) : (y))

#define PANIC(expr)                       \
    {                                     \
        if ((expr))                       \
        {                                 \
            printf("Panic: " #expr "\n"); \
            exit(123);                    \
        }                                 \
    }

typedef enum Signal_en
{
    LOW,
    HIGH
} Signal;

typedef enum ModuleType_en
{
    BROADCAST,
    FLIP_FLOP,
    CONJUNCTION
} ModuleType;

typedef struct Pulse_st
{
    Signal signal;
    struct Module_st *module;
} Pulse;

typedef struct Module_st
{
    ModuleType type;
    int outputs_len;
    struct Module_st *outputs[OUTPUTS_LEN];

    Signal flip_flop;

    int inputs_len;
    Pulse inputs[INPUTS_LEN];
} Module;

Module broadcast;
Module modules[MODULES_LEN];

Module *parse_module(char *out_c, FILE *file);
void press_button(Pulse *queue, size_t queue_len,
                  const Module *rx_input, int *out_input_presses, int button_presses);
long lcm(int idx, const int *arr, int arrlen);

int main()
{
    FILE *file = fopen(INPUT, "r");

    for (int i = 0; i < MODULES_LEN; ++i)
    {
        modules[i].inputs_len = 0;
        modules[i].flip_flop = LOW;
    }

    int max_outputs = 0;
    int modules_count = 0;
    char c = fgetc(file);
    while (c != EOF)
    {
        Module *module = parse_module(&c, file);

        ++modules_count;
        max_outputs = MAX(max_outputs, module->outputs_len);
    }

    size_t queue_len = (size_t)(modules_count * max_outputs);
    Pulse *queue = malloc(queue_len * sizeof(Pulse));

    int input_presses[INPUTS_LEN];
    const Module *rx_input = modules[RX_INDEX].inputs->module;
    for (int i = 0; i < rx_input->inputs_len; ++i)
    {
        input_presses[i] = 0;
    }

    for (int button_presses = 1, finished = 0;
         !finished;
         ++button_presses)
    {
        press_button(queue, queue_len, rx_input, input_presses, button_presses);

        finished = 1;
        for (int i = 0; i < rx_input->inputs_len; ++i)
        {
            finished &= input_presses[i] != 0;
        }
    }

    long solution = lcm(0, input_presses, rx_input->inputs_len);

    free(queue);
    fclose(file);

    int success = solution == SOLUTION;
    printf("Solution: %ld (%d)\n", solution, success);

    return (success) ? 0 : 1;
}

Module *parse_module(char *out_c, FILE *file)
{
    Module *module;
    ModuleType type;
    char c = *out_c;

    if (c == '%' || c == '&')
    {
        type = (c == '%') ? FLIP_FLOP : CONJUNCTION;

        c = fgetc(file);
        int module_idx = 0;
        for (; c != ' '; c = fgetc(file))
        {
            module_idx = module_idx * BASE + (c - 'a');
        }

        module = modules + module_idx;
    }
    else
    {
        type = BROADCAST;
        module = &broadcast;

        for (; c != ' '; c = fgetc(file))
        {
            ;
        }
    }

    for (; !(c >= 'a' && c <= 'z'); c = fgetc(file))
    {
        ;
    }

    module->type = type;
    module->outputs_len = 0;

    while (c != '\n')
    {
        int module_idx = 0;
        for (; c != ',' && c != '\n'; c = fgetc(file))
        {
            module_idx = module_idx * BASE + (c - 'a');
        }

        Module *output = modules + module_idx;

        PANIC(output->inputs_len == INPUTS_LEN);
        PANIC(module->outputs_len == OUTPUTS_LEN);

        module->outputs[module->outputs_len] = output;
        module->outputs_len += 1;

        output->inputs[output->inputs_len].signal = LOW;
        output->inputs[output->inputs_len].module = module;
        output->inputs_len += 1;

        if (c != '\n')
        {
            fgetc(file);
            c = fgetc(file);
        }
    }

    *out_c = fgetc(file);
    return module;
}

void press_button(Pulse *queue, size_t queue_len,
                  const Module *rx_input, int *out_input_presses, int button_presses)
{
    queue[0].signal = LOW;
    queue[0].module = &broadcast;

    for (
        size_t read_idx = 0, write_idx = 1;
        read_idx != write_idx;
        read_idx = (read_idx + 1) % queue_len)
    {
        Pulse *pulse = queue + read_idx;

        Module *module = pulse->module;
        Signal received = pulse->signal;

        Signal send = received;
        if (module->type == FLIP_FLOP)
        {
            if (received == HIGH)
            {
                continue;
            }

            module->flip_flop = !module->flip_flop;

            send = module->flip_flop;
        }
        else if (module->type == CONJUNCTION)
        {
            int all_high = 1;
            for (int i = 0; all_high && i < module->inputs_len; ++i)
            {
                all_high &= module->inputs[i].signal == HIGH;
            }

            send = (all_high) ? LOW : HIGH;
        }

        for (int i = 0; i < module->outputs_len; ++i)
        {
            Module *send_to = module->outputs[i];

            if (send_to->outputs_len == 0)
            {
                continue;
            }

            if (send_to->type == CONJUNCTION)
            {
                int input_idx = 0;
                for (; input_idx < send_to->inputs_len; ++input_idx)
                {
                    if (send_to->inputs[input_idx].module == module)
                    {
                        break;
                    }
                }

                if (send == HIGH && send_to == rx_input && out_input_presses[input_idx] == 0)
                {
                    out_input_presses[input_idx] = button_presses;
                }

                send_to->inputs[input_idx].signal = send;
            }

            PANIC(write_idx == read_idx);

            queue[write_idx].signal = send;
            queue[write_idx].module = send_to;

            write_idx = (write_idx + 1) % queue_len;
        }
    }
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

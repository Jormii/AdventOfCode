#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (101010)

#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define WIDTH (100)
#define HEIGHT (100)
#define CACHE_SIZE (200)
#define CYCLES (1000000000)
#define CYCLE()        \
    {                  \
        slide_north(); \
        slide_west();  \
        slide_south(); \
        slide_east();  \
    }

typedef struct CacheLine_st
{
    int idx;
    long hash;
} CacheLine;

CacheLine cache[CACHE_SIZE];
char platform[WIDTH * HEIGHT];

void parse_platform(char *out_c, FILE *file);
void slide_north();
void slide_west();
void slide_south();
void slide_east();
long platform_hash();
int calculate_load();

int main()
{
    FILE *file = fopen(INPUT, "r");

    char c = fgetc(file);
    parse_platform(&c, file);

    int cycle = 0;
    int loop_begin = -1;
    int cache_begin = 0;
    int cache_end = cache_begin;
    while (cycle < CYCLES && loop_begin == -1)
    {
        CYCLE();

        long hash = platform_hash();
        for (int i = cache_begin; i != cache_end; i = (i + 1) % CACHE_SIZE)
        {
            const CacheLine *cline = cache + i;
            if (cline->hash == hash)
            {
                loop_begin = cline->idx;
                break;
            }
        }

        if (loop_begin == -1)
        {
            CacheLine *cline = cache + cache_end;
            cline->idx = cycle;
            cline->hash = hash;

            cache_end = (cache_end + 1) % CACHE_SIZE;
            if (cache_begin == cache_end)
            {
                cache_begin = (cache_begin + 1) % CACHE_SIZE;
            }

            ++cycle;
        }
    }

    int loop_len = cycle - loop_begin;
    int loop_idx = (CYCLES - 1 - loop_begin) % loop_len;
    for (int i = 0; i < loop_idx; ++i)
    {
        CYCLE();
    }

    int solution = calculate_load();

    fclose(file);

    int success = solution == SOLUTION;
    printf("Solution: %d (%d)\n", solution, success);

    return (success) ? 0 : 1;
}

void parse_platform(char *out_c, FILE *file)
{
    int idx = 0;
    char c = *out_c;
    for (int row = 0; row < HEIGHT; ++row, c = fgetc(file))
    {
        for (int col = 0; col < WIDTH; ++col, c = fgetc(file))
        {
            platform[idx++] = c;
        }
    }
}

void slide_north()
{
    int to_occupy[WIDTH];
    for (int col = 0; col < WIDTH; ++col)
    {
        to_occupy[col] = col;
    }

    int idx = 0;
    for (int row = 0; row < HEIGHT; ++row)
    {
        for (int col = 0; col < WIDTH; ++col)
        {
            char c = platform[idx];
            if (c == '#')
            {
                to_occupy[col] = idx + WIDTH;
            }
            else if (c == 'O')
            {
                platform[idx] = '.';
                platform[to_occupy[col]] = 'O';

                to_occupy[col] += WIDTH;
            }

            ++idx;
        }
    }
}

void slide_west()
{
    int to_occupy[HEIGHT];
    for (int row = 0; row < HEIGHT; ++row)
    {
        to_occupy[row] = row * WIDTH;
    }

    int idx = 0;
    for (int row = 0; row < HEIGHT; ++row)
    {
        for (int col = 0; col < WIDTH; ++col)
        {
            char c = platform[idx];
            if (c == '#')
            {
                to_occupy[row] = idx + 1;
            }
            else if (c == 'O')
            {
                platform[idx] = '.';
                platform[to_occupy[row]] = 'O';

                to_occupy[row] += 1;
            }

            ++idx;
        }
    }
}

void slide_south()
{
    int to_occupy[WIDTH];
    for (int col = 0; col < WIDTH; ++col)
    {
        to_occupy[col] = (HEIGHT - 1) * WIDTH + col;
    }

    int idx = (WIDTH * HEIGHT) - 1;
    for (int row = (HEIGHT - 1); row >= 0; --row)
    {
        for (int col = (WIDTH - 1); col >= 0; --col)
        {
            char c = platform[idx];
            if (c == '#')
            {
                to_occupy[col] = idx - WIDTH;
            }
            else if (c == 'O')
            {
                platform[idx] = '.';
                platform[to_occupy[col]] = 'O';

                to_occupy[col] -= WIDTH;
            }

            --idx;
        }
    }
}

void slide_east()
{
    int to_occupy[HEIGHT];
    for (int row = 0; row < HEIGHT; ++row)
    {
        to_occupy[row] = (row + 1) * WIDTH - 1;
    }

    int idx = (WIDTH * HEIGHT) - 1;
    for (int row = (HEIGHT - 1); row >= 0; --row)
    {
        for (int col = (WIDTH - 1); col >= 0; --col)
        {
            char c = platform[idx];
            if (c == '#')
            {
                to_occupy[row] = idx - 1;
            }
            else if (c == 'O')
            {
                platform[idx] = '.';
                platform[to_occupy[row]] = 'O';

                to_occupy[row] -= 1;
            }

            --idx;
        }
    }
}

long platform_hash()
{
    long prime = 16777619;
    long hash = 2166136261;

    for (int i = 0; i < (WIDTH * HEIGHT); i++)
    {
        hash = (hash ^ platform[i]) * prime;
    }

    return hash;
}

int calculate_load()
{
    int idx = 0;
    int load = 0;
    for (int row = 0; row < HEIGHT; ++row)
    {
        for (int col = 0; col < WIDTH; ++col)
        {
            if (platform[idx++] == 'O')
            {
                load += HEIGHT - row;
            }
        }
    }

    return load;
}

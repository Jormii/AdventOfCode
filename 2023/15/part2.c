#include <stdio.h>
#include <stdlib.h> // TODO: Remove

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (245223)

#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (-1)
#endif

#define LIST_LENGTH (8)
#define HASHMAP_SIZE (256)

typedef struct Lens_st
{
    long hash;
    int focal_length;
} Lens;

typedef struct Hash_st
{
    long hash;
    int _256_hash;
} Hash;

typedef struct HashCell_st
{
    int lens_len;
    Lens lens[LIST_LENGTH];
} HashCell;

HashCell hashmap[HASHMAP_SIZE];

void parse_operation(char *out_c, FILE *file);
void hashmap_remove(const Hash *hash);
void hashmap_update(const Hash *hash, char *out_c, FILE *file);

int main()
{
    FILE *file = fopen(INPUT, "r");

    for (HashCell *cell = hashmap; cell != hashmap + HASHMAP_SIZE; ++cell)
    {
        cell->lens_len = 0;
    }

    char c = fgetc(file);
    while (1)
    {
        parse_operation(&c, file);

        if (c == EOF)
        {
            break;
        }
        else
        {
            c = fgetc(file);
        }
    }

    int sum = 0;
    for (int box = 0; box < HASHMAP_SIZE; ++box)
    {
        const HashCell *cell = hashmap + box;
        for (int slot = 0; slot < cell->lens_len; ++slot)
        {
            sum += (box + 1) * (slot + 1) * (cell->lens[slot].focal_length);
        }
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %d (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

void parse_operation(char *out_c, FILE *file)
{
    char c = *out_c;

    long prime = 16777619;
    Hash hash = {.hash = 2166136261, ._256_hash = 0};
    for (; c != '=' && c != '-'; c = fgetc(file))
    {
        hash.hash = (hash.hash ^ c) * prime;
        hash._256_hash = (17 * (hash._256_hash + c)) % 256;
    }

    char op = c;
    c = fgetc(file);
    if (op == '-')
    {
        hashmap_remove(&hash);
    }
    else
    {
        hashmap_update(&hash, &c, file);
    }

    *out_c = c;
}

void hashmap_remove(const Hash *hash)
{
    int r_idx = 0;
    HashCell *cell = hashmap + hash->_256_hash;
    for (; r_idx < cell->lens_len; ++r_idx)
    {
        const Lens *lens = cell->lens + r_idx;
        if (lens->hash == hash->hash)
        {
            break;
        }
    }

    if (r_idx != cell->lens_len)
    {
        for (int i = r_idx + 1; i < cell->lens_len; ++i)
        {
            cell->lens[i - 1] = cell->lens[i];
        }
        cell->lens_len -= 1;
    }
}

void hashmap_update(const Hash *hash, char *out_c, FILE *file)
{
    char c = *out_c;
    int focal_length = 0;
    for (; c != ',' && c != EOF; c = fgetc(file))
    {
        focal_length = 10 * focal_length + (c - '0');
    }
    *out_c = c;

    HashCell *cell = hashmap + hash->_256_hash;
    for (int i = 0; i < cell->lens_len; ++i)
    {
        Lens *lens = cell->lens + i;
        if (lens->hash == hash->hash)
        {
            lens->focal_length = focal_length;
            return;
        }
    }

    if (cell->lens_len == LIST_LENGTH)
    {
        exit(123);
    }

    Lens *lens = cell->lens + cell->lens_len;
    lens->hash = hash->hash;
    lens->focal_length = focal_length;

    cell->lens_len += 1;
}

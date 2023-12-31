#include <stdio.h>

#ifndef BIGBOY
//
#define INPUT "input.txt"
#define SOLUTION (246163188)

#define HANDS_COUNT (1000)
#else
//
#define INPUT "bigboy.txt"
#define SOLUTION (6678229757944529)

#define HANDS_COUNT (200000)
#endif

#define HAND_SIZE (5)
#define CHAR_IS_NUM(c) ((c) >= '0' && (c) <= '9')

typedef enum Card_en
{
    TWO,
    THREE,
    FOUR,
    FIVE,
    SIX,
    SEVEN,
    EIGHT,
    NINE,
    T,
    J,
    Q,
    K,
    A,
    CARD_ENUM_COUNT,
} Card;

typedef enum HandType_en
{
    HIGH_CARD,
    ONE_PAIR,
    TWO_PAIR,
    THREE_OF_A_KIND,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    FIVE_OF_A_KIND,
} HandType;

typedef struct Hand_st
{
    int bid;
    HandType type;
    Card cards[HAND_SIZE];
} Hand;

Hand parse_hand(char *out_c, FILE *file);
void heap_sort(Hand *hands);
void heapify(Hand *hands, int n, int idx);
void swap_hands(Hand *h1, Hand *h2);
int greater_than(const Hand *h1, const Hand *h2);

int main()
{
    FILE *file = fopen(INPUT, "r");

    char c = fgetc(file);
    Hand hands[HANDS_COUNT];
    for (int i = 0; i < HANDS_COUNT; ++i)
    {
        hands[i] = parse_hand(&c, file);
    }

    size_t sum = 0;
    heap_sort(hands);
    for (size_t i = 0; i < HANDS_COUNT; ++i)
    {
        sum += (i + 1) * (size_t)(hands[i].bid);
    }

    fclose(file);

    int success = sum == SOLUTION;
    printf("Solution: %lu (%d)\n", sum, success);

    return (success) ? 0 : 1;
}

Hand parse_hand(char *out_c, FILE *file)
{
    Hand hand;
    char c = *out_c;

    int different = 0;
    int found_three_or_more = 0;
    int count[CARD_ENUM_COUNT] = {0};
    for (int i = 0; i < HAND_SIZE; ++i)
    {
        if (CHAR_IS_NUM(c))
        {
            hand.cards[i] = (c - '2') + TWO;
        }
        else
        {
            switch (c)
            {
            case 'T':
                hand.cards[i] = T;
                break;
            case 'J':
                hand.cards[i] = J;
                break;
            case 'Q':
                hand.cards[i] = Q;
                break;
            case 'K':
                hand.cards[i] = K;
                break;
            case 'A':
                hand.cards[i] = A;
                break;
            default:
                break;
            }
        }

        count[hand.cards[i]] += 1;
        if (count[hand.cards[i]] == 1)
        {
            ++different;
        }
        if (count[hand.cards[i]] == 3)
        {
            found_three_or_more = 1;
        }

        c = fgetc(file);
    }

    if (different == 1)
    {
        hand.type = FIVE_OF_A_KIND;
    }
    else if (different == 2)
    {
        Card first = hand.cards[0];
        if (count[first] == 1 || count[first] == 4)
        {
            hand.type = FOUR_OF_A_KIND;
        }
        else
        {
            hand.type = FULL_HOUSE;
        }
    }
    else if (different == 3)
    {
        if (found_three_or_more)
        {
            hand.type = THREE_OF_A_KIND;
        }
        else
        {
            hand.type = TWO_PAIR;
        }
    }
    else if (different == 4)
    {
        hand.type = ONE_PAIR;
    }
    else if (different == 5)
    {
        hand.type = HIGH_CARD;
    }

    c = fgetc(file);

    hand.bid = 0;
    while (CHAR_IS_NUM(c))
    {
        hand.bid = 10 * hand.bid + (c - '0');
        c = fgetc(file);
    }

    *out_c = fgetc(file);
    return hand;
}

void heap_sort(Hand *hands)
{
    for (int i = HANDS_COUNT / 2 - 1; i >= 0; --i)
    {
        heapify(hands, HANDS_COUNT, i);
    }

    for (int i = HANDS_COUNT - 1; i >= 0; i--)
    {
        swap_hands(hands, hands + i);
        heapify(hands, i, 0);
    }
}

void heapify(Hand *hands, int n, int idx)
{
    int largest = idx;
    int left = 2 * idx + 1;
    int right = 2 * idx + 2;

    if (left < n && greater_than(hands + left, hands + largest))
    {
        largest = left;
    }

    if (right < n && greater_than(hands + right, hands + largest))
    {
        largest = right;
    }

    if (largest != idx)
    {
        swap_hands(hands + idx, hands + largest);
        heapify(hands, n, largest);
    }
}

void swap_hands(Hand *h1, Hand *h2)
{
    Hand tmp = *h1;
    *h1 = *h2;
    *h2 = tmp;
}

int greater_than(const Hand *h1, const Hand *h2)
{
    if (h1->type > h2->type)
    {
        return 1;
    }
    else if (h1->type == h2->type)
    {
        for (int i = 0; i < HAND_SIZE; ++i)
        {
            if (h1->cards[i] > h2->cards[i])
            {
                return 1;
            }
            else if (h1->cards[i] < h2->cards[i])
            {
                return 0;
            }
        }
    }
    return 0;
}

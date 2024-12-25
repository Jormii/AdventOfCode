import os
import sys
import time
from typing import Dict, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 1405
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')

SequenceT = Tuple[int, int, int, int]


def main() -> int:
    t = time.perf_counter()

    with open(INPUT_FILE) as fd:
        numbers = map(lambda ln: int(ln.strip()), fd.readlines())

    GENERATE = 2000
    SEQUENCE_LEN = 4

    earnings: Dict[SequenceT, int] = {}
    for n in numbers:
        buyer_earnings: Dict[SequenceT, int] = {}

        prices = [n % 10]
        for _ in range(GENERATE):
            n = pseudorandom(n)
            prices.append(n % 10)

        for i in range(SEQUENCE_LEN, len(prices)):
            a, b, c, d, price = prices[i-SEQUENCE_LEN:i+1]

            sequence = (b - a, c - b, d - c, price - d)
            if sequence not in buyer_earnings:
                buyer_earnings[sequence] = price

        for sequence, price in buyer_earnings.items():
            if sequence not in earnings:
                earnings[sequence] = price
            else:
                earnings[sequence] += price

    most_bananas = max(earnings.values())

    tf = time.perf_counter()

    success = most_bananas == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {most_bananas} ({success})')

    return 0 if success else 1


def pseudorandom(n: int) -> int:
    PRUNE = 16777216

    n = ((64 * n) ^ n) % PRUNE
    n = ((n // 32) ^ n) % PRUNE
    n = ((2048 * n) ^ n) % PRUNE

    return n


if __name__ == '__main__':
    exit(main())

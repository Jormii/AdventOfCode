import os
import sys
import time

BIGBOY = False

if not BIGBOY:
    SOLUTION = 12759339434
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


def main() -> int:
    t = time.perf_counter()

    with open(INPUT_FILE) as fd:
        numbers = map(lambda ln: int(ln.strip()), fd.readlines())

    GENERATE = 2000

    sum_ = 0
    for n in numbers:
        for _ in range(GENERATE):
            n = pseudorandom(n)

        sum_ += n

    tf = time.perf_counter()

    success = sum_ == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {sum_} ({success})')

    return 0 if success else 1


def pseudorandom(n: int) -> int:
    PRUNE = 16777216

    n = ((64 * n) ^ n) % PRUNE
    n = ((n // 32) ^ n) % PRUNE
    n = ((2048 * n) ^ n) % PRUNE

    return n


if __name__ == '__main__':
    exit(main())

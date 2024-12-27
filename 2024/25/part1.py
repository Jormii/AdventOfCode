import os
import sys
import time
from typing import List

BIGBOY = False

if not BIGBOY:
    SOLUTION = 3663
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')

PinsT = List[int]

WIDTH = 5
HEIGHT = 7


def main() -> int:
    t = time.perf_counter()

    keys: List[PinsT] = []
    locks: List[PinsT] = []
    with open(INPUT_FILE) as fd:
        it = map(lambda ln: ln.strip(), fd.readlines())

        for line in it:
            pins = [0] * WIDTH

            if line[0] == '.':
                keys.append(pins)
            else:
                locks.append(pins)

            for line in it:
                if len(line) == 0:
                    break

                for i, c in enumerate(line):
                    pins[i] += c == '#'

    fit = 0
    for key in keys:
        for lock in locks:
            key_lock_fit = True
            for k, l in zip(key, lock, strict=True):
                if (k + l) >= HEIGHT:
                    key_lock_fit = False
                    break

            fit += key_lock_fit

    tf = time.perf_counter()

    success = fit == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {fit} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())

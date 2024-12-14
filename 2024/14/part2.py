import os
import re
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Set

BIGBOY = False

if not BIGBOY:
    SOLUTION = 6668
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


@dataclass(slots=True)
class Robot:
    px: int
    py: int
    vx: int
    vy: int


def main() -> int:
    t = time.perf_counter()

    # NOTE: Copied from https://www.reddit.com/r/adventofcode/comments/1hdvhvu/comment/m1z7h5g/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

    w, h = 101, 103
    bots = [[*map(int, re.findall(r'-?\d+', l))] for l in open(INPUT_FILE)]

    def danger(t):
        a = b = c = d = 0

        for x, y, dx, dy in bots:
            x = (x + dx * t) % w
            y = (y + dy * t) % h

            a += x > w//2 and y > h//2
            b += x > w//2 and y < h//2
            c += x < w//2 and y > h//2
            d += x < w//2 and y < h//2

        return a * b * c * d

    solution = (min(range(10_000), key=danger))

    tf = time.perf_counter()

    success = solution == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {solution} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())

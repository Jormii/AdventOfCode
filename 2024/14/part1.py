import os
import re
import sys
import time
import functools

BIGBOY = False

if not BIGBOY:
    SOLUTION = 230461440
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


def main() -> int:
    t = time.perf_counter()

    WIDTH = 101
    HEIGHT = 103
    SECONDS = 100
    REGEX = r'^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$'

    MIDDLE_X = WIDTH // 2
    MIDDLE_Y = HEIGHT // 2
    PATTERN = re.compile(REGEX)

    quadrants = 4*[0]
    with open(INPUT_FILE) as fd:
        for line in fd.readlines():
            assert (search := PATTERN.search(line)) is not None

            px = int(search.group(1))
            py = int(search.group(2))
            vx = int(search.group(3))
            vy = int(search.group(4))

            fx = (px + SECONDS*vx) % WIDTH
            fy = (py + SECONDS*vy) % HEIGHT
            if fx == MIDDLE_X or fy == MIDDLE_Y:
                continue

            quadrant_idx = ((fy > MIDDLE_Y) << 1) + (fx > MIDDLE_X)
            quadrants[quadrant_idx] += 1

    safety_factor = functools.reduce(lambda f, x: f*x, quadrants, 1)

    tf = time.perf_counter()

    success = safety_factor == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {safety_factor} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())

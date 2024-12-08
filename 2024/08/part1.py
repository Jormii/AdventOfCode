import os
import sys
import time
from typing import Dict, List, Set, Tuple

BIGBOY = False

if not BIGBOY:
    SOLUTION = 396
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')

PointT = Tuple[int, int]


def main() -> int:
    t = time.perf_counter()

    antennas: Dict[str, List[PointT]] = {}
    with open(INPUT_FILE) as fd:
        for r, line in enumerate(fd.readlines()):
            for c, char in enumerate(line):
                if char == '.' or char == '\n':
                    continue

                if char not in antennas:
                    antennas[char] = [(r, c)]
                else:
                    antennas[char].append((r, c))

    rows = r + 1
    cols = c

    antinodes: Set[PointT] = set()
    for char, char_antennas in antennas.items():
        for i, (ri, ci) in enumerate(char_antennas):
            for j in range(i + 1, len(char_antennas)):
                rj, cj = char_antennas[j]

                vr = rj - ri
                vc = cj - ci

                r, c = ri - vr, ci - vc
                if 0 <= r < rows and 0 <= c < cols:
                    antinodes.add((r, c))

                r, c = rj + vr, cj + vc
                if 0 <= r < rows and 0 <= c < cols:
                    antinodes.add((r, c))

    locations_count = len(antinodes)

    tf = time.perf_counter()

    success = locations_count == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {locations_count} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())

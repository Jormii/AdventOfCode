import os
import sys
import time
from typing import Dict, List

BIGBOY = False

if not BIGBOY:
    SOLUTION = 1100663950563322
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = -1
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


def main() -> int:
    t = time.perf_counter()

    with open(INPUT_FILE) as fd:
        lines = fd.readlines()

        patterns = lines[0].strip().split(', ')
        designs = list(map(lambda ln: ln.strip(), lines[2:]))

    key_len = min(map(len, patterns))
    slotted_patterns: Dict[str, Dict[int, List[str]]] = {}
    for pattern in patterns:
        head, tail = pattern[:key_len], pattern[key_len:]

        tail_len = len(tail)
        if head not in slotted_patterns:
            slotted_patterns[head] = {tail_len: [tail]}
        elif tail_len not in slotted_patterns[head]:
            slotted_patterns[head][tail_len] = [tail]
        else:
            slotted_patterns[head][tail_len].append(tail)

    possible = 0
    cache = {'': 1}
    for design in designs:
        possible += is_possible(design, key_len, slotted_patterns, cache)

    tf = time.perf_counter()

    success = possible == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {possible} ({success})')

    return 0 if success else 1


def is_possible(
        design: str,
        key_len: int,
        slotted_patterns: Dict[str, Dict[int, List[str]]],
        cache: Dict[str, int],
) -> int:
    if design in cache:
        return cache[design]

    head = design[:key_len]
    if head not in slotted_patterns:
        return 0

    possible = 0
    for tail_len, tails in slotted_patterns[head].items():
        substr = design[key_len:key_len+tail_len]
        remaining_design = design[key_len+tail_len:]

        for tail in tails:
            if substr == tail:
                possible += is_possible(remaining_design, key_len, slotted_patterns, cache)  # nopep8

    cache[design] = possible
    return possible


if __name__ == '__main__':
    exit(main())

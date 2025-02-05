from __future__ import annotations
import os
import sys
import time
import heapq
from typing import Dict, List

BIGBOY = True

if not BIGBOY:
    SOLUTION = 6408966547049
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 70351090993107482
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


class File:
    id: int
    off: int
    size: int

    __slots__ = ['id', 'off', 'size']

    def __init__(self, id: int, off: int, size: int) -> None:
        self.id = id
        self.off = off
        self.size = size


class FreeSpace:
    off: int
    size: int

    __slots__ = ['off', 'size']

    def __init__(self, off: int, size: int) -> None:
        self.off = off
        self.size = size


def main() -> int:
    t = time.perf_counter()

    files: List[File] = []
    free_spaces: Dict[int, List[int]] = {}  # Size-offset bins
    with open(INPUT_FILE) as fd:
        id = 0
        off = 0
        is_file = True

        for size in map(int, fd.readline()):
            if is_file:
                files.append(File(id, off, size))
                id += 1
            elif size == 0:
                pass
            elif size not in free_spaces:
                free_spaces[size] = [off]
            else:
                heapq.heappush(free_spaces[size], off)

            off += size
            is_file = not is_file

    for file in reversed(files):
        free_space: FreeSpace | None = None
        for size in filter(lambda x: x >= file.size, free_spaces.keys()):
            off = free_spaces[size][0]

            if off > file.off:
                pass
            elif free_space is None:
                free_space = FreeSpace(off, size)
            elif off < free_space.off:
                free_space.off = off
                free_space.size = size

        if free_space is None:
            continue

        file.off = free_space.off

        bin = free_spaces[free_space.size]
        size = free_space.size - file.size

        heapq.heappop(bin)
        
        if size != 0:
            if size not in free_spaces:
                free_spaces[size] = [free_space.off + file.size]
            else:
                heapq.heappush(free_spaces[size], free_space.off + file.size)

    checksum = 0
    for file in files:
        checksum += file.id * sum(range(file.off, file.off + file.size))

    tf = time.perf_counter()

    success = checksum == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {checksum} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())

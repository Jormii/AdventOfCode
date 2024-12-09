import os
import sys
import time
from typing import List
from dataclasses import dataclass

BIGBOY = False

if not BIGBOY:
    SOLUTION = 6384282079460
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = 70317453809507637
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


@dataclass
class File:
    id: int
    off: int
    size: int


@dataclass
class FreeSpace:
    off: int
    size: int


def main() -> int:
    t = time.perf_counter()

    files: List[File] = []
    free_spaces: List[FreeSpace] = []
    with open(INPUT_FILE) as fd:
        id = 0
        off = 0
        is_file = True

        for size in map(int, fd.readline()):
            if is_file:
                files.append(File(id, off, size))
                id += 1
            elif size != 0:
                free_spaces.append(FreeSpace(off, size))

            off += size
            is_file = not is_file

    file_idx = len(files) - 1
    free_space_idx = 0
    while file_idx > 0:
        file = files[file_idx]
        free_space = free_spaces[free_space_idx]
        if file.off < free_space.off:
            break

        if file.size < free_space.size:
            file_idx -= 1
            file.off = free_space.off

            free_space.off += file.size
            free_space.size -= file.size
        elif file.size > free_space.size:
            file.size -= free_space.size
            files.append(File(file.id, free_space.off, free_space.size))

            free_space_idx += 1
        else:
            file_idx -= 1
            file.off = free_space.off

            free_space_idx += 1

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

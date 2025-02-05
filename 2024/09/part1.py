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

# https://topaz.github.io/paste/#XQAAAQBpBAAAAAAAAAAzHIoib6pXbueH4X9F244lVRDcOZab5q1+VXn364pc+UKqMBZudFE4iEVQaGsWDOVUHgJDI64/O5ONxBUqz3zUCPdaFqUWPtP2jgT4nmtITP5XIse15ONDCleQ/X9vm5mAbtlda35HnmeJxDeIIY3gZSNHYk+TykIvfYClvriyMtoxS+2bwROcfTe8IRcQ4pRwEt/prsbVslKytZcarFI10FpaNaK9LinLS9FVm1gb0Rp9UVNGz+tQwjrdvbnMZ3DkFuUCMrClDU6yBdfkGeS2ptRy9ODnwNI9juzlqwluJG6dIbIltlm6KIYmcO6KxJC+kFA1qe+4X7+pHesCSrXANyvZlKuMInHPflEtiEJjU4L8DpT9awMSSFXAY9LRi8kNqs6mUBZS4W7bGk+Xnto0Y/UzeVsqB5fGIH+YbzV0jKClTJ5o06hENkD7uc8Sqi8EjhAAVURATooRdsCirJdJf1GFdjGROPiHfZgbwcbPSnoZTStlGNohv25UkeZbyr8xlp81TDLap3rJwrarbj/UdDP2/HEQp6GYU0LSfIFqvPqK2PpGVbELN6Fl136Tiz9oQFuIq6Bf/3eFSQA=
# https://topaz.github.io/paste/#XQAAAQDbBAAAAAAAAAAzHIoib6pXbueH4X9F244lVRDcOZab5q1+VXY/ex42qR7D+RLbGAmEZMhJ9uw2UMx1yGIpgxPXOsOpTK4ff8xstvS5sI3XbpwSQ6IimouqknFKvmo8/YyCCiiBYfQuDOnz7wRuy3lgcRiyR4DHnVnZ+2ho60KenTyR0daTyb0K0bXmBQNsyWq2gX1hXga4tdpqSFn1ozZ0u4qcfFN/uiPIW1Wj9T/ThB2meMzs+jj7Q5VBX+L9Xh8o/sPYk5ZUDjdNzTQbXI4VzkbfKJ2LClaHOlHg3jVJu2OPxIYtqQEF0GYuxtUyMmP2TKZssZFaFpz1ENN66btf0zcJ8ydDN3zR1hPozASVQTid+jFuZ2kRRZPm2FHCkrvdjtXt76zB/yx56L+sfxKoQT8Yo2aqh3A5oLE2d2JESNqhf7kkA2MV9GHP9A7saQc65Mlb6e3B/RBmS643NUOWEO/ecKGLKe++Ov3UD02GPuyHwPsJliT7XAJwI1C2UnaA4gSyh5QwwDNhLr0j8ejx+/FaEYM9XPLWzbv8GJiHikT6EdaXSPDETR0Y6hFhmcTAamX9Qxz6ILdy6+VBsLToMcpHdht7mz1FqQWEQ6gexZ1NRS5AiPuORp82xMxAVbEPMwAJAFJ/aH5WqwnrtDRIR+p1j+hoIhejlGykczl0NS9HTOeiI7y+RniDEewP28B2HB0WogaSylr45SQggkpkXmI9E938Ui0B


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

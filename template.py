import os
from typing import TypeVar, Union

T = TypeVar("T")
OptT = Union[T, None]

SOLUTION = -1


def main() -> int:
    input_path = os.path.join(os.path.split(__file__)[0], "input.txt")

    fd = open(input_path, "r")

    l = fd.readline().strip()
    while len(l) != 0:
        l = fd.readline().strip()

    fd.close()

    success = solution == SOLUTION
    print(f"Solution: {solution} ({success})")

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())

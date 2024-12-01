import os

SOLUTION = 3246517
INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')


def main() -> int:
    with open(INPUT_FILE) as fd:
        lines = fd.readlines()

        left = [0] * len(lines)
        right = [0] * len(lines)
        for i, line in enumerate(lines):
            split = line.split()

            l_value = int(split[0])
            r_value = int(split[1])

            left[i] = l_value
            right[i] = r_value

    left.sort()
    right.sort()

    distance = 0
    for l_value, r_value in zip(left, right, strict=True):
        distance += abs(l_value - r_value)

    success = distance == SOLUTION
    print(f'Solution: {distance} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())

import os
import re
import sys
import time

BIGBOY = False

if not BIGBOY:
    SOLUTION = 103811193
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    # TODO: Apparently the solution is wrong
    SOLUTION = 748337990746
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


def main() -> int:
    t = time.perf_counter()

    DO_REGEX = r'do\(\)'
    DONT_REGEX = r'don\'t\(\)'
    MUL_REGEX = r'mul\((\d{1,3}),(\d{1,3})\)'

    DO_PATTERN = re.compile(DO_REGEX)
    DONT_PATTERN = re.compile(DONT_REGEX)
    MUL_PATTERN = re.compile(MUL_REGEX)

    total = 0
    with open(INPUT_FILE) as fd:
        enabled = True

        for line in fd.readlines():
            enable_insts = [(m.start(), True)
                            for m in DO_PATTERN.finditer(line)]
            enable_insts.extend([(m.start(), False)
                                for m in DONT_PATTERN.finditer(line)])

            enable_insts.sort()
            enable_insts.append((sys.maxsize, enabled))

            enable_insts_idx = 0
            for mul_inst in MUL_PATTERN.finditer(line):
                begin = mul_inst.start()
                while enable_insts[enable_insts_idx][0] < begin:
                    enabled = enable_insts[enable_insts_idx][1]
                    enable_insts_idx += 1

                if enabled:
                    left = int(mul_inst.group(1))
                    right = int(mul_inst.group(2))

                    total += left * right

    tf = time.perf_counter()

    success = total == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {total} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())

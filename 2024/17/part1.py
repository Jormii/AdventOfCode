import os
import re
import sys
import time
from typing import List
from dataclasses import dataclass

BIGBOY = False

if not BIGBOY:
    SOLUTION = '7,5,4,3,4,5,3,4,6'
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'input.txt')
else:
    SOLUTION = ''
    INPUT_FILE = os.path.join(os.path.split(__file__)[0], 'bigboy.txt')


@dataclass(slots=True)
class Register:
    value: int


def main() -> int:
    t = time.perf_counter()

    PTRN = re.compile(r'\d+')

    with open(INPUT_FILE) as fd:
        lns = fd.readlines()

    A = Register(int(PTRN.search(lns[0]).group()))  # type: ignore[union-attr]
    B = Register(int(PTRN.search(lns[1]).group()))  # type: ignore[union-attr]
    C = Register(int(PTRN.search(lns[2]).group()))  # type: ignore[union-attr]
    program = list(map(lambda m: int(m.group()), PTRN.finditer(lns[4])))

    REGISTERS = {i: Register(i) for i in range(4)}
    REGISTERS[4] = A
    REGISTERS[5] = B
    REGISTERS[6] = C

    pc = 0
    outputs: List[int] = []
    while pc < len(program):
        op_code = program[pc]
        operand = program[pc + 1]

        jumped = False
        match op_code:
            case 0:
                A.value //= 1 << REGISTERS[operand].value
            case 1:
                B.value ^= operand
            case 2:
                B.value = REGISTERS[operand].value % 8
            case 3:
                if A.value != 0:
                    pc = operand
                    jumped = True
            case 4:
                B.value ^= C.value
            case 5:
                outputs.append(REGISTERS[operand].value % 8)
            case 6:
                B.value = A.value // (1 << REGISTERS[operand].value)
            case 7:
                C.value = A.value // (1 << REGISTERS[operand].value)
            case _:
                raise NotImplementedError(op_code)

        if not jumped:
            pc += 2

    solution = ','.join(map(str, outputs))

    tf = time.perf_counter()

    success = solution == SOLUTION
    print(tf - t, file=sys.stderr)
    print(f'Solution: {solution} ({success})')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())

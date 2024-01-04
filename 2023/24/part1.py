import os
import re
import numpy as np
from typing import Tuple, TypeVar, Union

T = TypeVar("T")
OptT = Union[T, None]

SOLUTION = 12015

AREA = (200000000000000, 400000000000000)


def main() -> int:
    input_path = os.path.join(os.path.split(__file__)[0], "input.txt")

    fd = open(input_path, "r")

    positions = np.empty((0, 3))
    velocities = np.empty((0, 3))

    l = fd.readline().strip()
    while len(l) != 0:
        p, v = parse_row(l)
        positions = np.vstack((positions, p))
        velocities = np.vstack((velocities, v))

        l = fd.readline().strip()

    solution = calculate_intersections(positions, velocities)

    fd.close()

    success = solution == SOLUTION
    print(f"Solution: {solution} ({success})")

    return success


def parse_row(line: str) -> Tuple[np.ndarray, np.ndarray]:
    REGEX = r"(-?)(\d+),\s*(-?)(\d+),\s*(-?)(\d+)\s*@\s*(-?)(\d+),\s*(-?)(\d+),\s*(-?)(\d+)"

    values = np.empty(6)
    match = re.search(REGEX, line)
    for i in range(6):
        sign = match.group(1 + 2*i)
        value = match.group(1 + 2*i+1)

        if len(sign) == 0:
            values[i] = float(value)
        else:
            values[i] = -float(value)

    return values[:3], values[3:]


def calculate_intersections(positions: np.ndarray, velocities: np.ndarray) -> int:
    P = positions[:, (0, 1)]
    V = velocities[:, (0, 1)]

    intersections = 0
    for i in range(len(positions)):
        p0 = P[i]
        pf = p0 + V[i]

        for j in range(i + 1, len(positions)):
            I = cramers_rule(p0, pf, P[j], P[j] + V[j])
            if I is not None:
                p, tp, tq = I

                intersections += (tp >= 0 and tq >= 0) \
                    and (p[0] >= AREA[0] and p[0] <= AREA[1]) \
                    and (p[1] >= AREA[0] and p[1] <= AREA[1])

    return intersections


def cramers_rule(p0: np.ndarray, pf: np.ndarray,
                 q0: np.ndarray, qf: np.ndarray) -> OptT[Tuple[np.ndarray, float, float]]:
    v = pf - p0
    u = qf - q0
    w = q0 - p0

    det_A = v[1] * u[0] - v[0] * u[1]
    if np.isclose(det_A, 0):
        return None

    det_PT = w[1] * u[0] - w[0] * u[1]
    det_QT = v[0] * w[1] - v[1] * w[0]

    pt = (det_PT / det_A)
    qt = (det_QT / det_A)

    return p0 + pt*v, pt, qt


if __name__ == "__main__":
    exit(main())

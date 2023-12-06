import os
import re
import subprocess
from subprocess import PIPE

DAY = 1
YEAR = 2023
BIGBOY = False
EXECUTIONS = 100

assert os.name == "posix"

print(f"--- {DAY} / {YEAR} ---")
os.chdir(os.path.join(f"{YEAR}", f"{DAY:02}"))

for part in [1, 2]:
    PATTERN = r"[\.\d]+"
    RUN_ARGS = ["time", "-f", "\"%e3\"", "./a.out"]
    COMPILE_CMD = f"gcc part{part}.c -O2 -pedantic -Wall -Wextra -Wcast-align " \
        "-Wcast-qual -Wdisabled-optimization -Wformat=2 -Winit-self -Wlogical-op " \
        "-Wmissing-declarations -Wmissing-include-dirs -Wredundant-decls -Wshadow " \
        "-Wsign-conversion -Wstrict-overflow -Wswitch-default -Wundef -Werror"

    if BIGBOY:
        COMPILE_CMD = f"{COMPILE_CMD} -D BIGBOY"

    print(f"Part {part}: ", end="")

    process = subprocess.run(COMPILE_CMD.split(" "), stdout=PIPE, stderr=PIPE)
    if process.returncode != 0:
        exit(f"GCC $?={process.returncode}\n{process.stderr.decode()}\n")

    process = subprocess.run(RUN_ARGS, stdout=PIPE, stderr=PIPE)
    if process.returncode != 0:
        exit(f"Run $?={process.returncode}\n{process.stderr.decode()}\n")

    time = 0
    for i in range(EXECUTIONS):
        process = subprocess.run(RUN_ARGS, stdout=PIPE, stderr=PIPE)

        err = process.stderr.decode()
        time += float(re.findall(PATTERN, err)[0])

    print(f"- {time / EXECUTIONS:.3f} s")

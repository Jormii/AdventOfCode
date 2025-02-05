import os
import re
import subprocess
from subprocess import PIPE

DAY = 21
YEAR = 2024
EXECUTIONS = 100

# assert os.name == 'posix'

print(f'--- {DAY} / {YEAR} ---')

for part in [2]:
    RUN_ARGS = ['python', f'{YEAR}/{DAY:02}/part{part}.py']

    print(f'Part {part}: ', end='')

    process = subprocess.run(RUN_ARGS, stdout=PIPE, stderr=PIPE)
    if process.returncode != 0:
        print(f'Run $?={process.returncode}')
        continue

    time = 0.0
    for i in range(EXECUTIONS):
        process = subprocess.run(RUN_ARGS, stdout=PIPE, stderr=PIPE)

        err = process.stderr.decode()
        time += float(err)

    print(f'{time / EXECUTIONS:.6f} s')

import os
import re
import subprocess
from subprocess import PIPE

DAY = 1
YEAR = 2024
EXECUTIONS = 100

assert os.name == 'posix'

print(f'--- {DAY} / {YEAR} ---')

for part in [1, 2]:
    PATTERN = rf'([.0-9]+) part{part}.py:\d+\(main\)'
    RUN_ARGS = [
        'python',
        '-m',
        'cProfile',
        '-s',
        'cumtime',
        f'{YEAR}/{DAY:02}/part{part}.py'
    ]

    print(f'Part {part} ({" ".join(RUN_ARGS)}): ', end='')

    process = subprocess.run(RUN_ARGS, stdout=PIPE, stderr=PIPE)
    if process.returncode != 0:
        print(f'Run $?={process.returncode}')
        continue

    time = 0.0
    for i in range(EXECUTIONS):
        process = subprocess.run(RUN_ARGS, stdout=PIPE, stderr=PIPE)

        out = process.stdout.decode()
        search = re.search(PATTERN, out)
        assert search is not None

        time += float(search.group(1))

    print(f'- {time / EXECUTIONS:.3f} s')

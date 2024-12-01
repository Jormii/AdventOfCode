import os
import re
import subprocess
from subprocess import PIPE

DAY = 1
YEAR = 2024
EXECUTIONS = 100

assert os.name == 'posix'

print(f'--- {DAY} / {YEAR} ---')
os.chdir(os.path.join(f'{YEAR}', f'{DAY:02}'))

for part in [1, 2]:
    PATTERN = r'[\.\d]+'
    RUN_ARGS = ['/usr/bin/time', '-f', '"%e3"', 'python', f'part{part}.py']

    print(f'Part {part}: ', end='')

    process = subprocess.run(RUN_ARGS, stdout=PIPE, stderr=PIPE)
    if process.returncode != 0:
        print(f'Run $?={process.returncode}')
        continue

    time = 0.0
    for i in range(EXECUTIONS):
        process = subprocess.run(RUN_ARGS, stdout=PIPE, stderr=PIPE)

        err = process.stderr.decode()
        time += float(re.findall(PATTERN, err)[0])

    print(f'- {time / EXECUTIONS:.3f} s')

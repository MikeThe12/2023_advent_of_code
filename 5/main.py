from pathlib import Path
import re

p = Path().cwd() / 'input.csv'

with p.open() as src:
    data = {}
    n = -2 # skiprows
    current_group = ''
    digits_regex = re.compile(r'(\d+) (\d+) (\d+)')
    groups_regex = re.compile(r'([a-z]+-to-[a-z]+) map:')

    for line in src.readlines():
        if line == '\n' or line.startswith('seeds:'):
            n += 1
            continue
        if re.match(r'^[a-z]', line):
            current_group = groups_regex.findall(line)[0]
            data[current_group] = []
            continue
        if re.match(r'^\d', line):
            data[current_group].append(list(map(int, digits_regex.findall(line)[0])))

inputs = set(map(int,'629551616 310303897 265998072 58091853 3217788227 563748665 2286940694 820803307 1966060902 108698829 190045874 3206262 4045963015 223661537 1544688274 293696584 1038807941 31756878 1224711373 133647424'.split()))
# Part 1:
for group in data:
    new_inputs = set()
    for row in data[group]:
        for i in inputs:
            if (i >= row[1] and i <= row[1]+row[2]):
                new_inputs.add(row[0] + (i-row[1]))
    inputs = new_inputs

print(min(inputs))
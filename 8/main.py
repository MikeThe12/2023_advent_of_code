from pathlib import Path
import re
from itertools import cycle
import math

p = Path().cwd() / 'input.csv'
instructions = list('LRRRLRRLRLLRLRRLRLRLLRRRLRLRRRLRRRLRLRLRRLRLRRRLRRLLRRLLLRRLRRLRRRLRLRRRLRRLRRRLRRRLRRLRLLRRRLRLRRLRLRLRRRLRRLLRRRLLRRLRLRRLRRRLLLRRRLLRLLRRLRRRLRLRLRRLLLRRRLLRRLLLRLRLRRLLRLLRRLLLRRLLRRRLRLRRRLRLLRRRLRRRLRLRLRRRLRLRRRLRRRLRRRLLRLRLRLRRLRLRRRLRLRLLRRLRRLRRLRRRLRRRLRLLRLLLRRLRLRRRR')
mapping = {}

position = re.compile(r'([A-Z]{3,3}) = \([A-Z]{3,3}, [A-Z]{3,3}\)')
left = re.compile(r'[A-Z]{3,3} = \(([A-Z]{3,3}), [A-Z]{3,3}\)')
right = re.compile(r'[A-Z]{3,3} = \([A-Z]{3,3}, ([A-Z]{3,3})\)')

with p.open() as src:
    for line in src:
        mapping[position.findall(line)[0]] = {
            'L': left.findall(line)[0],
            'R': right.findall(line)[0]
        }

# Part 1
current = 'AAA'
for i, side in enumerate(cycle(instructions), start=1):
    current = mapping[current][side]
    if current == 'ZZZ':
        print(f'Reached the end in {i} steps')
        break

# Part 2
visits_steps = {}
for _map in mapping:
    if _map.endswith("A"):
        visits_steps[_map] = []
        current = _map
        visits_positions = set()
        for i, side in enumerate(cycle(instructions), start=1):
            current = mapping[current][side]
            if current.endswith("Z"):
                # I am only interested in positions ending with "Z"
                # not visited previously
                if current in visits_positions:
                    break
                visits_steps[_map].append(i)
                visits_positions.add(current)

print(f'It takes {math.lcm(*[visits_steps[v][0] for v in visits_steps])} steps for part 2')
from pathlib import Path
import re

p = Path.cwd() / 'input.csv'

# Part 1
with p.open() as src:
    total=0
    for line in src:
        line_sep = re.findall(r'.*: (.*) \| (.*)', line)
        winning_nums = set(re.findall(r'(\d+)', line_sep[0][0]))
        my_nums = set(re.findall(r'(\d+)', line_sep[0][1]))
        if (my_win_len := len(winning_nums.intersection(my_nums)) - 1) >= 0:
            total += 2**my_win_len

    print(total)

# Part 2
with p.open() as src:
    total=0
    my_win_lens = []
    for line in src:
        line_sep = re.findall(r'.*: (.*) \| (.*)', line)
        winning_nums = set(re.findall(r'(\d+)', line_sep[0][0]))
        my_nums = set(re.findall(r'(\d+)', line_sep[0][1]))
        my_win_lens.append(len(winning_nums.intersection(my_nums)))

    # in the begenning I have 1 copy of each card:
    winning_cards = {i+1: 1 for i in range(len(my_win_lens))}
    for i, n in enumerate(my_win_lens):
        total += winning_cards[i+1]
        for _ in range(winning_cards[i+1]):
            for j in range(1, my_win_lens[i] + 1):
                winning_cards[i+j+1] += 1

    print(total)
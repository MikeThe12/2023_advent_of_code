from pathlib import Path
import numpy as np

p = Path().cwd() / 'input.csv'
m = np.genfromtxt(p, delimiter=' ', dtype=np.int64)

# Part 1
s = 0
for i in range(m.shape[0]):
    last_el = np.array([])
    array = m[i]
    while np.any(array):
        last_el = np.append(last_el, array[-1])
        array = np.diff(array)
    s += last_el.sum()   

print(s)

# Part 2
s = 0
for i in range(m.shape[0]):
    first_el = np.array([])
    array = m[i]
    while np.any(array):
        first_el = np.append(first_el, array[0])
        array = np.diff(array)
    first_el = first_el[::-1]
    diff = 0
    for j in range(first_el.shape[0]):
        diff = first_el[j] - diff
    s += diff

print(s)
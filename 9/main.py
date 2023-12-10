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

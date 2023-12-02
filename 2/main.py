import pandas as pd
import numpy as np
from pathlib import Path


p = Path.cwd() / 'input.csv'
df = pd.read_csv(p, sep=':', names=('game', 'numbers'))
# Part 1
print((df
    .assign(game = lambda df_: df_.game.str.extract(r'(\d+)'))
    .numbers.str.extractall(r'(\d+) (\w+)')
    .droplevel(level=1)
    .reset_index(names='game_id')
    .rename({0: 'number', 1: 'color'}, axis=1)
    .assign(
        game_id = lambda df_: df_.game_id.astype(int) + 1,
        number = lambda df_: df_.number.astype(int),
        cond = lambda df_: np.where(
            ((df_.color == 'red') & (df_.number > 12) |
            (df_.color == 'green') & (df_.number > 13) |
            (df_.color == 'blue') & (df_.number > 14)),
            1, 0
        ))
    .groupby('game_id')['cond']
    .agg('sum')
    .reset_index()
    .query('cond == 0')
    .game_id
    .unique()
    .sum()
))
# Part 2
print((df
    .assign(game = lambda df_: df_.game.str.extract(r'(\d+)'))
    .numbers.str.extractall(r'(\d+) (\w+)')
    .droplevel(level=1)
    .reset_index(names='game_id')
    .rename({0: 'number', 1: 'color'}, axis=1)
    .assign(
        game_id = lambda df_: df_.game_id.astype(int) + 1,
        number = lambda df_: df_.number.astype(int))
    .groupby(['game_id', 'color'], as_index=False)['number']
    .agg('max')
    .groupby('game_id')['number']
    .prod()
    .sum()
))
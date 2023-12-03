import pandas as pd
import numpy as np
from pathlib import Path

p = Path.cwd() / 'input.csv'

data = []
with p.open() as src:
    for line in src.readlines():
        data.append(list(line))
# Part 1:
df = (
    pd.DataFrame(data)
    .drop(140, axis=1)
    .rename(columns={i: i+1 for i in range(140)})
    .reset_index(names='row_num')
    .assign(row_num = lambda df_:df_.row_num + 1)
    .melt(id_vars='row_num', var_name='col_num')
    .assign(
        is_num = lambda df_: df_.value.str.contains(r'\d+'),
        is_symbol = lambda df_: df_.value.str.contains(r'[^\.\d]'))
    .sort_values(by=['row_num', 'col_num'])
)
df = (
    df
    .merge( # left
        right=(
            df
            .assign(
                #col_num_orig = lambda df_:df_.col_num,
                col_num = lambda df_: df_.groupby('row_num').col_num.shift(-1),
                value_left = lambda df_: df_.value,
                left = lambda df_: df_.is_symbol)
            .loc[:,['row_num', 'col_num', 'value_left', 'left']]      
            ),
        how='left',
        on=['row_num', 'col_num']
        )
    .merge( # upperleft
        right=(
            df
            .assign(
                col_num_orig = lambda df_:df_.col_num,
                row_num_orig = lambda df_:df_.row_num,
                col_num = lambda df_: df_.groupby('row_num_orig').col_num.shift(-1),
                row_num = lambda df_: df_.groupby('col_num_orig').row_num.shift(-1),
                value_upperleft = lambda df_: df_.value,
                upperleft = lambda df_: df_.is_symbol)
            .loc[:,['col_num', 'row_num', 'value_upperleft', 'upperleft']]),
        how='left',
        on = ['row_num', 'col_num']
        )
    .merge( # upper
        right=(
            df
            .assign(
                row_num = lambda df_: df_.groupby('col_num').row_num.shift(-1),
                value_upper = lambda df_: df_.value,
                upper = lambda df_: df_.is_symbol)
            .loc[:,['col_num', 'row_num', 'value_upper', 'upper']]),
        how='left',
        on = ['row_num', 'col_num']        
        )   
    .merge( # upperright
        right=(
            df
            .assign(
                col_num_orig = lambda df_:df_.col_num,
                row_num_orig = lambda df_:df_.row_num,
                col_num = lambda df_: df_.groupby('row_num_orig').col_num.shift(1),
                row_num = lambda df_: df_.groupby('col_num_orig').row_num.shift(-1),
                value_upperright = lambda df_: df_.value,
                upperright = lambda df_: df_.is_symbol)
            .loc[:,['col_num', 'row_num', 'value_upperright', 'upperright']]),
        how='left',
        on = ['row_num', 'col_num']
        )
    .merge( # right
        right=(
            df
            .assign(
                #col_num_orig = lambda df_:df_.col_num,
                col_num = lambda df_: df_.groupby('row_num').col_num.shift(1),
                value_right = lambda df_: df_.value,
                right = lambda df_: df_.is_symbol)
            .loc[:,['row_num', 'col_num', 'value_right', 'right']]      
            ),
        how='left',
        on=['row_num', 'col_num']
        )
    .merge( # lowerright
        right=(
            df
            .assign(
                col_num_orig = lambda df_:df_.col_num,
                row_num_orig = lambda df_:df_.row_num,
                col_num = lambda df_: df_.groupby('row_num_orig').col_num.shift(1),
                row_num = lambda df_: df_.groupby('col_num_orig').row_num.shift(1),
                value_lowerright = lambda df_: df_.value,
                lowerright = lambda df_: df_.is_symbol)
            .loc[:,['col_num', 'row_num', 'value_lowerright', 'lowerright']]),
        how='left',
        on = ['row_num', 'col_num']
        )
    .merge( # lower
        right=(
            df
            .assign(
                row_num = lambda df_: df_.groupby('col_num').row_num.shift(1),
                value_lower = lambda df_: df_.value,
                lower = lambda df_: df_.is_symbol)
            .loc[:,['col_num', 'row_num', 'value_lower', 'lower']]),
        how='left',
        on = ['row_num', 'col_num']        
        ) 
    .merge( # lowerleft
        right=(
            df
            .assign(
                col_num_orig = lambda df_:df_.col_num,
                row_num_orig = lambda df_:df_.row_num,
                col_num = lambda df_: df_.groupby('row_num_orig').col_num.shift(-1),
                row_num = lambda df_: df_.groupby('col_num_orig').row_num.shift(1),
                value_lowerleft = lambda df_: df_.value,
                lowerleft= lambda df_: df_.is_symbol)
            .loc[:,['col_num', 'row_num', 'value_lowerleft', 'lowerleft']]),
        how='left',
        on = ['row_num', 'col_num']
        )
    .assign(
        valid_single_digit = lambda df_: np.where(
            (df_.is_num) &
            (df_.loc[:, [
                'left', 
                'upperleft', 
                'upper', 
                'upperright', 
                'right', 
                'lowerright', 
                'lower', 
                'lowerleft']]
                .any(axis=1)),
            True, False),
        )
    .loc[:, ['row_num', 'col_num', 'value', 'is_num', 'valid_single_digit']]   
)

print(
    df
    .merge(
        right=(
            df
            .assign(
                col_num = lambda df_: df_.col_num.add(-1),
                is_num = lambda df_: df_.is_num,
                valid_single_digit_one_right = lambda df_: df_.valid_single_digit,
                value_one_right = lambda df_: df_.value)
            .loc[:, ['row_num', 'col_num', 'is_num', 'valid_single_digit_one_right', 'value_one_right']]
        ),
        how = 'left',
        on = ['row_num', 'col_num', 'is_num'])
    .merge(
        right=(
            df
            .assign(
                col_num = lambda df_: df_.col_num.add(-2),
                is_num = lambda df_: df_.is_num,
                valid_single_digit_two_right = lambda df_: df_.valid_single_digit,
                value_two_right = lambda df_: df_.value)
            .loc[:, ['row_num', 'col_num', 'is_num', 'valid_single_digit_two_right', 'value_two_right']]
        ),
        how = 'left',
        on = ['row_num', 'col_num', 'is_num'])
    .query('is_num == True')
    .assign(col_num_shift = lambda df_: (df_
        .groupby('row_num')
        .col_num
        .shift(1, fill_value=-1))
        )
    .query('(col_num != col_num_shift.add(1)) and '
        '(valid_single_digit == True or '
        'valid_single_digit_one_right == True or '
        'valid_single_digit_two_right == True)')
    .assign(
        value_one_right = lambda df_: df_.value_one_right.fillna(''),
        value_two_right = lambda df_: df_.value_two_right.fillna(''),
        part_number = lambda df_: (df_
            .loc[:, ['value', 'value_one_right', 'value_two_right']]
            .agg(''.join, axis=1)
            .astype(int))
        )
    .part_number
    .sum()    
)

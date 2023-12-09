from pathlib import Path
import pandas as pd
import numpy as np
from collections import Counter

p = Path().cwd() / 'input.csv'
df = pd.read_csv(p, sep=' ', names=['hand', 'bid'])
replacements = {
    'T': '10',
    'J': '11',
    'Q': '12',
    'K': '13',
    'A': '14'
}
# Part 1
print(df
.assign(
     counts = df.hand.apply(list).apply(Counter),
     n_unique = lambda df_: df_.counts.apply(len),
     first = df.hand.str.extract(r'^(.).*').replace(replacements).astype(int),
     second = df.hand.str.extract(r'^.(.).*').replace(replacements).astype(int),
     third = df.hand.str.extract(r'^..(.).*').replace(replacements).astype(int),
     fourth = df.hand.str.extract(r'^...(.).*').replace(replacements).astype(int),
     fifth = df.hand.str.extract(r'^.*(.)$').replace(replacements).astype(int),
     high_hand = lambda df_: np.where(
         (df_.counts.apply(lambda x: x.most_common(1)[0][1] == 1)), 14, 0),
     one_pair = lambda df_: np.where(
         (df_.counts.apply(lambda x: x.most_common(1)[0][1] == 2)) &
         (df_.n_unique == 4), 15, 0),
     two_pairs = lambda df_: np.where(
         (df_.counts.apply(lambda x: x.most_common(1)[0][1] == 2)) &
         (df_.n_unique == 3), 16, 0),
     three_of_kind = lambda df_: np.where(
         (df_.counts.apply(lambda x: x.most_common(1)[0][1] == 3)) &
         (df_.n_unique == 3), 17, 0), 
     full_house = lambda df_: np.where(
         (df_.counts.apply(lambda x: x.most_common(1)[0][1] == 3)) &
         (df_.n_unique == 2), 18, 0),
     four_of_kind = lambda df_: np.where(
         (df_.counts.apply(lambda x: x.most_common(1)[0][1] == 4)) &
         (df_.n_unique == 2), 19, 0),   
     five_of_kind = lambda df_: np.where(
         (df_
          .counts
          .apply(lambda x: x.most_common(1)[0][1] == 5)), 20, 0),
     hand_val = lambda df_: (
         df_
         .loc[:,'high_hand':'five_of_kind']
         .max(axis='columns')))   
.sort_values(['hand_val', 'first', 'second', 'third', 'fourth', 'fifth'], ascending=False)
.assign(
    _rank = np.arange(start=df.shape[0], stop=0, step=-1),
    winnings = lambda df_: df_.bid.multiply(df_._rank))
.winnings
.sum()
)
# Part 2
replacements.update({'J': 1})
print(df
.assign(
     counts = df.hand.apply(list).apply(Counter),
     n_unique = lambda df_: df_.counts.apply(len),
     first = df.hand.str.extract(r'^(.).*').replace(replacements).astype(int),
     second = df.hand.str.extract(r'^.(.).*').replace(replacements).astype(int),
     third = df.hand.str.extract(r'^..(.).*').replace(replacements).astype(int),
     fourth = df.hand.str.extract(r'^...(.).*').replace(replacements).astype(int),
     fifth = df.hand.str.extract(r'^.*(.)$').replace(replacements).astype(int),
     joker = lambda df_: df_.counts.apply(lambda x: x.get('J', 0)),
     most_common = lambda df_ : df_.counts.apply(lambda x: x.most_common(1)[0][0]),
     most_common_cnt = lambda df_ : df_.counts.apply(lambda x: x.most_common(1)[0][1]),
     high_hand = lambda df_: np.where(
         (df_.most_common_cnt == 1), 14, 0),
     one_pair = lambda df_: np.where(
         ((df_.most_common_cnt == 2) &
         (df_.n_unique == 4))
          | 
         ((df_.high_hand == 14) & (df_.joker == 1)), 15, 0),
     two_pairs = lambda df_: np.where(
         ((df_.most_common_cnt == 2) &
         (df_.n_unique == 3)), 16, 0),
     three_of_kind = lambda df_: np.where(
         ((df_.most_common_cnt == 3) &
         (df_.n_unique == 3))
         | # puvodni one pair + joker
         (((df_.most_common_cnt == 2) &
         (df_.n_unique == 4))  
          & (df_.joker == 1) 
          & (df_.most_common != 'J'))
         | # pair of jokers
         ((df_.most_common_cnt == 2) 
         & (df_.joker == 2)), 17, 0),
     full_house = lambda df_: np.where(
         ((df_.most_common_cnt== 3) 
         & (df_.n_unique == 2))
         | # dva pary + joker
         ((df_.most_common_cnt == 2) 
         & (df_.n_unique == 3)
         & (df_.joker == 1))      
         , 18, 0),
     four_of_kind = lambda df_: np.where(
         ((df_.most_common_cnt == 4) &
         (df_.n_unique == 2))
         | # doplnim trojici na ctverici
         ((df_.most_common_cnt == 3) 
          & (df_.n_unique == 3)
          & (df_.joker == 1) 
          & (df_.most_common != 'J'))
         | # doplnim dve dvojice na ctverici
         ((df_.most_common_cnt == 2) 
          & (df_.n_unique == 3)
          & (df_.joker == 2))
         | # trojice jokeru ale ne full house
         ((df_.most_common_cnt == 3) 
           & (df_.n_unique == 3)
           & (df_.joker == 3)), 19, 0),
     five_of_kind = lambda df_: np.where(
         (df_.most_common_cnt == 5)
         | # ctyri + joker
         ((df_.most_common_cnt == 4) 
          & (df_.n_unique == 2)
          & (df_.joker == 1))
         | # tri + 2x joker
         ((df_.most_common_cnt == 3) 
          & (df_.n_unique == 2)
          & (df_.joker == 2))
         | # 2 + 3x joker
          ((df_.joker == 3) 
          & (df_.n_unique == 2))         
         | # 4 jokers
          ((df_.joker == 4) 
          & (df_.n_unique == 2))  
         | # 5 jokers       
         (df_.joker == 5), 20, 0),
     hand_val = lambda df_: (
         df_
         .loc[:,'high_hand':'five_of_kind']
         .max(axis='columns')))         
.sort_values(['hand_val', 'first', 'second', 'third', 'fourth', 'fifth'], ascending=False)
.assign(
    _rank = np.arange(start=df.shape[0], stop=0, step=-1),
    winnings = lambda df_: df_.bid.multiply(df_._rank))
.winnings
.sum()        
)
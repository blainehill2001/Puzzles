"""
Blaine Hill
September 2023
IBM Ponder This Puzzle

sequence size for n=5 for tenth occurrence: Sequence Size: 125

"""

import numba as nb
from numba_progress import ProgressBar

@nb.njit
def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

@nb.njit
def do_puzzle(n, a_1, progress_hook=None):
    count_5 = 0
    last_term = a_1

    diff_seq_size = 0
    
    for i in range(1, n):
        current_diff = gcd(i + 1, last_term)
        curr_term = last_term + current_diff
        if current_diff != 1:
            diff_seq_size+=1
            if current_diff == 5:
                count_5 += 1
        
        last_term = curr_term

        if count_5 == 200:
            break

        if progress_hook is not None:
            progress_hook.update(1)

    return diff_seq_size

a_1 = 531
n = 1000000000000000000

with ProgressBar(total=n, ncols=80) as progress:
    diff_seq_size = do_puzzle(n, a_1, progress)
    
    
# print(diff_seq_size)

from itertools import count, islice 
from math import gcd 
from sympy import isprime 
from tqdm import tqdm


def gen (a=531) :
    for n in count(2):
        if (b := gcd(a, n)) > 1:
            yield b
        a+=b
mylist = []
for k in tqdm( range(7, 10_000), desc='Processing', ncols=100):
    d = list(islice(gen (k), 58))
    for idx, n in enumerate(d):
        if not isprime(n):
            mylist.append(f"k: {k}, n: {(idx + 1)}, val: {n}")
            break
for ans in mylist:
    print(ans)


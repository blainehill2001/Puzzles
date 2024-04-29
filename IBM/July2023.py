"""
IBM July Puzzle
Blaine Hill



implement dfs with memo

as we go along, keep track of string answer, store states we have seen previously

write custom hash function

write custom checker function to ensure previous move was good


check current state to be good

check current state to be our answer

hash current state

run all possible moves





"""

from typing import Dict

import numba as nb
import numpy as np


@nb.njit
def dfs_with_memo(state, memo, cost, cur_move_str):
    hashed_state = hash_puzzle_board(state, equivalent_pieces)
    # check state

    # check set
    if hashed_state in memo:
        if memo[hashed_state] <= cost:
            return
        memo[hashed_state] = min(memo[hashed_state], cost)

    # check for answer
    if hashed_state == target_hash and cost < 100:
        print("Moves:", cur_move_str)
        return cur_move_str

    # Recurse on the neighbors
    for move, move_cost in get_feasible_moves(state):
        new_state = apply_move(state, move)
        new_move_str = cur_move_str + move
        dfs_with_memo(new_state, memo, cost + move_cost, new_move_str)


@nb.njit
def get_feasible_moves(state):
    feasible_moves = []
    nrows, ncols = state.shape

    for j in range(nrows):
        for i in range(ncols):
            if state[j, i] == 0:
                continue

            # Move up
            if j > 0 and (
                state[j - 1, i] == 0 or state[j - 1, i] == state[j, i]
            ):
                feasible_moves.append((f"U{j},{i}", 1))

            # Move down
            if j < nrows - 1 and (
                state[j + 1, i] == 0 or state[j + 1, i] == state[j, i]
            ):
                feasible_moves.append((f"D{j},{i}", 1))

            # Move left
            if i > 0 and (
                state[j, i - 1] == 0 or state[j, i - 1] == state[j, i]
            ):
                feasible_moves.append((f"L{j},{i}", 1))

            # Move right
            if i < ncols - 1 and (
                state[j, i + 1] == 0 or state[j, i + 1] == state[j, i]
            ):
                feasible_moves.append((f"R{j},{i}", 1))

    return feasible_moves


# Helper function to apply a move to the state
@nb.njit
def apply_move(state, move):
    move_type, pos = move.split(",")
    j, i = map(int, pos.split(","))
    new_state = state.copy()

    if move_type == "U":
        new_state[j - 1, i] = new_state[j, i]
        new_state[j, i] = 0
    elif move_type == "D":
        new_state[j + 1, i] = new_state[j, i]
        new_state[j, i] = 0
    elif move_type == "L":
        new_state[j, i - 1] = new_state[j, i]
        new_state[j, i] = 0
    elif move_type == "R":
        new_state[j, i + 1] = new_state[j, i]
        new_state[j, i] = 0

    return new_state


@nb.njit
def hash_puzzle_board(grid, equivalent_pieces):
    # Create a new grid where equivalent pieces are represented with the same values
    new_grid = np.array(
        [[equivalent_pieces[cell] for cell in row] for row in grid]
    )

    # Convert the 2D grid into a list of strings representation
    grid_list = [
        "".join([str(new_grid[j, i]) for i in range(5)]) for j in range(5)
    ]

    # Sort the pieces on the grid to ensure identical configurations get the same hash
    sorted_grid_string = "".join(sorted(grid_list))

    # Hash the sorted grid representation using the hash() function
    hash_value = custom_hash(sorted_grid_string)
    return hash_value


@nb.njit
def custom_hash(s):
    # A simple custom hashing function using prime numbers
    h = 0
    for c in s:
        h = (h * 31 + ord(c)) & 0xFFFFFFFFFFFFFFFF
    return h


equivalent_pieces = np.array(["X", "2", "3", "X", "Y", "Y", "Z", "8", "Z"])

grid = np.array(
    [
        [1, 2, 2, 3, 4],
        [1, 2, 3, 3, 4],
        [5, 6, 7, 7, 8],
        [9, 9, 8, 8, 8],
        [0, 0, 0, 0, 0],
    ]
)

memo: Dict[int, int] = {}
ans = np.array(
    [
        [7, 7, 0, 2, 2],
        [0, 0, 3, 2, 4],
        [0, 3, 3, 1, 4],
        [5, 9, 9, 1, 8],
        [0, 6, 8, 8, 8],
    ]
)
target_hash = hash_puzzle_board(ans, equivalent_pieces)

dfs_with_memo(grid, memo, 0, "")

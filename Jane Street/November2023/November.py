from collections import deque
from copy import deepcopy
from itertools import permutations
from typing import List, Tuple

import numpy as np

"""
soln:

Final time: 183
Final path: [(0, b1), (0, c1), (18, a2), (27, a1), (0, b1), (0, d1), (0, e1), (4, f1), (0, f3), (0, f4), (12, h3), (0, f4), (48, f2), (0, e2), (0, e1), (4, f3), (0, e1), (0, e3), (7, e4), (17, g5), (0, e4), (0, e2), (0, d4), (0, d5), (2, d7), (32, d5), (0, e3), (0, e2), (0, e4), (0, e5), (0, e6), (0, e7), (6, g8), (0, f8), (4, f7), (0, g7), (2, h7), (0, h8)]


"""


def get_possible_moves():
    # Define the elements and variations
    elements = (0, 1, 2)

    # Generate all permutations
    permutations_list = list(permutations(elements))

    moves = []
    # Print the permutations
    for perm in permutations_list:
        negOnePerm = tuple(-1 if value == 1 else value for value in perm)
        negTwoPerm = tuple(-2 if value == 2 else value for value in perm)
        moves.append(perm)
        moves.append(negOnePerm)
        moves.append(negTwoPerm)
    return moves


possible_moves = get_possible_moves()


def convert_to_lattice_point_notation(i, j):
    mapping = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return f"{i+1}{mapping[j]}"


def print_lattice_in_quandrant_one(lattice):
    reversed_lattice = lattice[::-1]
    for i in range(8):
        print(8 - i, end=" [")
        for elem in reversed_lattice[i][:7]:
            print("{:6.3f}".format(elem), end=" ")
        print("{:6.3f}]".format(reversed_lattice[i][7]))
    print("        ", end="")
    for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        print("{:6}".format(letter), end=" ")
    print()


lattice = np.array(
    [
        [0, 1, 0, 2, 4, 4, 7, 9],
        [2, 2, 3, 6, 10, 7, 9, 8],
        [4, 0, 1, 4, 7, 5, 11, 10],
        [3, 1, 4, 2, 9, 8, 9, 12],
        [5, 2, 2, 5, 6, 8, 10, 11],
        [6, 5, 7, 9, 8, 6, 12, 8],
        [2, 7, 10, 8, 7, 13, 14, 10],
        [4, 6, 7, 11, 9, 10, 12, 17],
    ],
    dtype=np.float64,
)


def simulate_waiting(i, j, time, lattice, max_time=180):
    time = min(max_time - time, max_time)
    # time = 5

    sinking_coords = [
        (x, y)
        for x, row in enumerate(lattice)
        for y, v in enumerate(row)
        if v == lattice[i, j]
    ]
    rising_coord = (abs(7 - i), abs(7 - j))
    if lattice[rising_coord[0], rising_coord[1]] == lattice[i, j]:
        rising_equals = True
        sinking_coords.remove(
            rising_coord
        )  # this works even if rising_coord wasn't in sinking_coords
    else:
        rising_equals = False
    for time_spent_waiting in range(
        0, 6 * len(sinking_coords), len(sinking_coords)
    ):
        timed_lattice = lattice.copy()

        for x, y in sinking_coords:
            timed_lattice[x, y] -= (
                time_spent_waiting * 1.0 / (len(sinking_coords))
            )
            # timed_lattice[x, y] -= 1

        if not rising_equals:
            x, y = rising_coord
            timed_lattice[x, y] += (
                time_spent_waiting * 1.0 / (len(sinking_coords))
            )
            # timed_lattice[x, y] += 1

        yield timed_lattice, time_spent_waiting


def find_max_time_iterative(
    start_i, start_j, start_time, start_lattice, start_visited, start_path
):
    queue = deque(
        [
            (
                start_i,
                start_j,
                start_time,
                start_lattice,
                start_visited,
                start_path,
            )
        ]
    )
    #   max_path, max_time = [], 0
    # prev_move_found = (0, 0, True)  # i,j, whether there was a move found last loop
    while queue:
        i, j, time, lattice, visited, path = queue.popleft()

        print(f"i: {i}, j: {j}, time: {time}")
        if i == 7 and j == 7:
            if time >= 180:
                print("got to final coords")
                print(path, time)
                return path, time
            else:
                print("Got to end but not without enough time")
                continue

        for di, dj, dz in possible_moves:
            ni, nj = i + di, j + dj

            if 0 <= ni <= 7 and 0 <= nj <= 7 and visited[ni][nj] < 3:
                continue_sinkining = True
                for timed_lattice, wait_time in simulate_waiting(
                    i, j, time, lattice
                ):
                    if not continue_sinkining:
                        break  # no point in going forward if sinking further doesn't matter
                    continue_sinkining = False
                    x, y = timed_lattice[i, j] + dz, timed_lattice[ni, nj]
                    if x > y:
                        continue_sinkining = True  # if the spot the knight with the change in height is on is still higher than where it is trying to go
                    if abs(x - y) > 1e-5:
                        continue

                    cur_visited = deepcopy(visited)
                    cur_visited[ni, nj] += 1
                    cur_path = deepcopy(path)
                    cur_path.append((wait_time, (ni, nj)))
                    queue.append(
                        (
                            ni,
                            nj,
                            time + wait_time,
                            timed_lattice,
                            cur_visited,
                            cur_path,
                        )
                    )

    print("nothing found, return None")


#   return max_path, max_time

visited = np.zeros((8, 8), dtype=int)
visited[0, 0] = 1
path: List[Tuple[int, str]] = []
# max_path, max_time = find_max_time(0, 0, 0, lattice, visited, path)
max_path, max_time = find_max_time_iterative(0, 0, 0, lattice, visited, path)
max_path = list(
    map(
        lambda x: (x[0], convert_to_lattice_point_notation(x[1][0], x[1][1])),
        max_path,
    )
)
print(f"Max time: {max_time}")
print(f"Max path: {max_path}")

import numpy as np
import os
from itertools import permutations


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
        combinedPerm = tuple(
            -1 if value == 1 else -2 if value == 2 else value for value in perm
        )
        moves.append(perm)
        moves.append(negOnePerm)
        moves.append(negTwoPerm)
        moves.append(combinedPerm)
    return moves


possible_moves = get_possible_moves()


def convert_to_lattice_point_notation(i, j):
    mapping = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return f"{mapping[j]}{i+1}"


def print_lattice_in_quandrant_one(lattice, knight_pos, good_moves):
    dim = len(lattice) - 1
    knight_pos = (dim - knight_pos[0], knight_pos[1])
    good_moves = list(map(lambda x: (dim - x[0], x[1]), good_moves))

    letter_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
    reversed_lattice = np.transpose(lattice)[::-1]

    print("\n\n")
    for i in range(dim + 1):
        print(dim + 1 - i, end=f" [")
        for j, elem in enumerate(reversed_lattice[i][:dim]):
            if (i, j) == knight_pos:
                print(
                    "\033[1;32m{:7.3f}\033[0m".format(elem), end=" "
                )  # Use ANSI escape codes for bold text
            elif (i, j) in good_moves:
                print(
                    "\033[1;31m{:7.3f}\033[0m".format(elem), end=" "
                )  # Use ANSI escape codes for bold text
            else:
                print("{:7.3f}".format(elem), end=" ")
        if (i, dim) == knight_pos:
            print(
                "\033[1;32m{:7.3f}]\033[0m".format(reversed_lattice[i][dim])
            )  # Use ANSI escape codes for bold text
        elif (i, dim) in good_moves:
            print(
                "\033[1;31m{:7.3f}]\033[0m".format(reversed_lattice[i][dim])
            )  # Use ANSI escape codes for bold text
        else:
            print("{:7.3f}]".format(reversed_lattice[i][dim]))

    print("        ", end="")
    for letter in letter_list[: dim + 1]:
        print("{:7}".format(letter), end=" ")


def print_lattice_in_quandrant_one_for_move_selection(
    lattice, knight_pos, good_moves, cur_move
):
    dim = len(lattice) - 1
    knight_pos = (dim - knight_pos[0], knight_pos[1])
    good_moves = list(map(lambda x: (dim - x[0], x[1]), good_moves))
    cur_move = (dim - cur_move[0], cur_move[1])

    letter_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
    reversed_lattice = np.transpose(lattice)[::-1]

    print("\n\n")
    for i in range(dim + 1):
        print(dim + 1 - i, end=f" [")
        for j, elem in enumerate(reversed_lattice[i][:dim]):
            if (i, j) == knight_pos:
                print(
                    "\033[1;32m{:7.3f}\033[0m".format(elem), end=" "
                )  # Use ANSI escape codes for bold text
            elif (i, j) == cur_move:
                print(
                    "\033[1;31m{:7.3f}\033[0m".format(elem), end=" "
                )  # Use ANSI escape codes for bold text
            elif (i, j) in good_moves:
                print(
                    "\033[2;31m{:7.3f}\033[0m".format(elem), end=" "
                )  # Use ANSI escape codes for bold text
            else:
                print("{:7.3f}".format(elem), end=" ")
        if (i, dim) == knight_pos:
            print(
                "\033[1;32m{:7.3f}]\033[0m".format(reversed_lattice[i][dim])
            )  # Use ANSI escape codes for bold text
        elif (i, dim) == cur_move:
            print(
                "\033[1;31m{:7.3f}\033[0m".format(reversed_lattice[i][dim])
            )  # Use ANSI escape codes for bold text
        elif (i, dim) in good_moves:
            print(
                "\033[2;31m{:7.3f}]\033[0m".format(reversed_lattice[i][dim])
            )  # Use ANSI escape codes for bold text
        else:
            print("{:7.3f}]".format(reversed_lattice[i][dim]))

    print("        ", end="")
    for letter in letter_list[: dim + 1]:
        print("{:7}".format(letter), end=" ")


class GameState:
    def __init__(self, lattice):
        self.lattice = lattice
        self.knight_pos = (0, 0)
        self.time = 0
        self.move_history = []
        self.dim = len(lattice) - 1
        self.visited = np.zeros((8, 8), dtype=int)
        self.visited[0, 0] = 1

    def make_move(self, lattice, wait, move):
        old_lattice = self.lattice
        old_knight_pos = self.knight_pos

        ni, nj = move
        self.visited[nj, ni] += 1  # due to printing weirdness
        self.lattice = lattice
        self.knight_pos = (ni, nj)
        self.time += wait
        self.move_history.append(
            (
                wait,
                convert_to_lattice_point_notation(ni, nj),
                ((old_knight_pos), old_lattice),
            )
        )

    def get_path(self):
        return list(map(lambda x: (x[0], x[1]), self.move_history))

    def undo_move(self):
        if len(self.move_history) > 0:
            cur_i, cur_j = self.knight_pos
            self.visited[cur_j, cur_i] -= 1
            last_wait, last_move_str, old_stuff = self.move_history.pop()
            last_i, last_j, old_lattice = old_stuff[0][0], old_stuff[0][1], old_stuff[1]

            self.lattice = old_lattice
            self.knight_pos = (last_i, last_j)
            self.time -= last_wait

    def find_moves_for_lat(self, lat):
        good_moves = []
        i, j = self.knight_pos
        i, j = j, i
        print(f"\ngood moves for {i, j}")
        for di, dj, dz in possible_moves:
            # di, dj = dj, di
            ni, nj = i + di, j + dj
            # nj, ni = ni, nj
            if 0 <= ni <= self.dim and 0 <= nj <= self.dim and self.visited[ni][nj] < 3:
                x, y = lat[i, j], lat[ni, nj] + dz
                print(convert_to_lattice_point_notation(nj, ni), x, y, di, dj, dz)
                if abs(x - y) < 1e-5:
                    print("Good move by altitude")
                    # print(convert_to_lattice_point_notation(nj,ni))
                    good_moves.append((nj, ni))  # due to printing weirdness
        return good_moves

    def simulate_waiting(self, wait=180):
        # this func will yield wait number of lattices that is changed by waiting at the knight_pos for 0-wait*len(sinking_coords) amount of seconds
        cur_i, cur_j = self.knight_pos
        cur_i, cur_j = cur_j, cur_i
        sinking_coords = [
            (x, y)
            for x, row in enumerate(self.lattice)
            for y, v in enumerate(row)
            if v == self.lattice[cur_i, cur_j]
        ]
        print(len(sinking_coords))
        rising_coord = (abs(self.dim - cur_i), abs(self.dim - cur_j))
        if self.lattice[rising_coord[0], rising_coord[1]] == self.lattice[cur_i, cur_j]:
            rising_equals = True
            sinking_coords.remove(
                rising_coord
            )  # this works even if rising_coord wasn't in sinking_coords
        else:
            rising_equals = False

        wait_times = [(self.lattice.copy(), 0)]
        timed_lattice = self.lattice.copy()
        for time_spent_waiting in range(
            len(sinking_coords), wait * len(sinking_coords), len(sinking_coords)
        ):
            for x, y in sinking_coords:
                timed_lattice[x, y] -= 1

            if not rising_equals:
                x, y = rising_coord
                timed_lattice[x, y] += 1

            wait_times.append((timed_lattice.copy(), time_spent_waiting))
        return wait_times

    def visualize(self):
        self.wait_times = self.simulate_waiting()
        cur_index = 0
        while True:
            cur_lat, cur_wait_time = (
                self.wait_times[cur_index][0],
                self.wait_times[cur_index][1],
            )
            # Clear the screen
            os.system("cls")
            good_moves = self.find_moves_for_lat(cur_lat)
            print_lattice_in_quandrant_one(
                np.array(cur_lat), self.knight_pos, good_moves
            )
            print("\n")
            print("Wait time is:", cur_wait_time)
            print("Knight path thus far is:", self.get_path())
            print("\n")
            # Get the user's input
            key = input("Type 'l' or 'r' to move, 's' to select: ")

            # Handle up arrow key
            if key == "r":
                if cur_index == len(self.wait_times) - 1:
                    cur_index = 0
                else:
                    cur_index += 1

            # Handle down arrow key
            elif key == "l":
                if cur_index == 0:
                    cur_index = len(self.wait_times) - 1
                else:
                    cur_index -= 1

            # Handle space bar key
            elif key == "s":
                final_lat = cur_lat
                final_wait_time = cur_wait_time
                break

        # now select the move
        move_index = 0
        while True:
            cur_lat, cur_wait_time = (
                self.wait_times[cur_index][0],
                self.wait_times[cur_index][1],
            )
            # Clear the screen
            os.system("cls")
            good_moves = self.find_moves_for_lat(cur_lat)
            if len(good_moves) == 0:
                # no available moves
                print("\n")
                print("You selected wait time:", cur_wait_time)
                print("Knight path thus far is:", self.get_path())
                print("\n")
                input(
                    "\033[1;31m{}\033[0m".format(
                        "No moves are available. Please press any key to continue"
                    )
                )
                return

            cur_move = good_moves[move_index]
            print_lattice_in_quandrant_one_for_move_selection(
                np.array(cur_lat), self.knight_pos, good_moves, cur_move
            )
            print("\n")
            print("You selected wait time:", cur_wait_time)
            print("Knight path thus far is:", self.get_path())
            print("\n")

            # Get the user's input
            key = input("Type 'l' or 'r' to move, 's' to select and exit: ")

            # Handle up arrow key and wraparound
            if key == "r":
                if move_index == len(good_moves) - 1:
                    move_index = 0
                else:
                    move_index += 1

            # Handle down arrow key and wraparound
            elif key == "l":
                if move_index == 0:
                    move_index = len(good_moves) - 1
                else:
                    move_index -= 1

            # Handle space bar key
            elif key == "s":
                final_move = cur_move
                break

        # apply move and go to home
        return final_lat, final_wait_time, final_move


class Game:
    def __init__(self, lattice):
        self.state = GameState(lattice)

    def play(self):
        self.render_lattice()

        while True:
            action = self.get_action()

            if action == "p":
                result = self.state.visualize()
                if not result:
                    continue  # continue if there are no legal moves
                lattice, wait_time, move = result
                # apply move
                self.state.make_move(lattice, wait_time, move)

            elif action == "u":
                self.state.undo_move()

            elif action == "e":
                break

            else:
                print("\n\n\nMake a valid selection")

        print("Final time:", self.state.time)
        print("Final path:", self.state.get_path())

    def get_action(self):
        print("\n\n\n")
        print("Knight path thus far is:", self.state.get_path())
        print("Possible actions:")
        print("- Play 'p'")
        print("- Undo last move 'u'")
        print("- End game 'e'")

        action = input("\nSelect action: ")
        return action

    def get_valid_moves(self):
        # Return list of valid moves
        return []

    def render_lattice(self):
        # Print lattice with knight position marked
        pass


practice_lattice = np.array(
    [[7, 10, 8, 11], [6, 4, 6, 10], [5, 3, 9, 11], [0, 1, 9, 14]]
)

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
    dtype=np.int8,
)

game = Game(lattice)
game.play()

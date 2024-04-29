import os
import pickle as pkl
from itertools import combinations

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy import Eq, I, solve, sqrt, symbols
from tqdm import tqdm

"""

check the region between x^2+y^2 = m^2 and x^2+y^2 = (m+1)^2 in the first quadrant

obtain all possible isometric gridpoints in the region.

the number of unique gridpoints not on either circle is the answer for f(m)

binary search for the answer since this is a monotonic function?

"""


def generate_isometric_grid_equations(m):
    equations = []

    for k in range(2 * m):

        def horizontal_equation_upwards(x, k=k):
            return k * sqrt(3) / 2

        # won't need for first quadrant analysis
        # def horizontal_equation_downwards(x, k=k):
        #     return -k * sqrt(3) / 2

        def positive_diagonal_equation_forwards(x, k=k):
            return sqrt(3) * x + k * sqrt(3)

        def positive_diagonal_equation_backwards(x, k=k):
            return sqrt(3) * x - k * sqrt(3)

        def negative_diagonal_equation_forwards(x, k=k):
            return -sqrt(3) * x + k * sqrt(3)

        # won't need for first quadrant analysis
        # def negative_diagonal_equation_backwards(x, k=k):
        #     return -sqrt(3) * x - k * sqrt(3)

        equations.extend(
            [
                horizontal_equation_upwards,
                positive_diagonal_equation_forwards,
                positive_diagonal_equation_backwards,
                negative_diagonal_equation_forwards,
            ]
        )

    return equations


def find_intersection_points(f, g):
    x = sp.Symbol("x")

    solutions = sp.solve([f(x) - g(x)], x, real=True)

    return [s[0] for s in solutions if not s[0].has(I) and s[0] >= 0]


def visualize_three_line_segments(segs):
    ((x1, y1), (x2, y2)), ((x3, y3), (x4, y4)), ((x5, y5), (x6, y6)) = segs
    x1, x2, x3, y1, y2, y3 = (
        [x1, x2],
        [x3, x4],
        [x5, x6],
        [y1, y2],
        [y3, y4],
        [y5, y6],
    )

    fig, ax = plt.subplots()

    ax.plot(x1, y1, color="red")
    ax.plot(x2, y2, color="green")
    ax.plot(x3, y3, color="blue")

    ax.autoscale()
    ax.set_title("Three Line Segments")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.show()


def check_parallel_lines(segs):
    def calculate_slope(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        if x1 == x2:
            # The line is vertical, and the slope is undefined
            return float("inf")
        else:
            return (y2 - y1) / (x2 - x1)

    slopes = [
        calculate_slope(segs[0][0], segs[0][1]),
        calculate_slope(segs[1][0], segs[1][1]),
        calculate_slope(segs[2][0], segs[2][1]),
    ]

    # Check if at least two slopes are equal
    return (
        slopes.count(slopes[0]) >= 2
        or slopes.count(slopes[1]) >= 2
        or slopes.count(slopes[2]) >= 2
    )


def find_line_seg_intersection_points(line_segments, m, log=True):
    dir_path = "./line seg intersection points"
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{m}.pkl")

    if not os.path.exists(file_path):
        if log:
            i, important_val = 0, -1
            with open("log.txt", "w") as file:
                pass  # The file is now empty

        intersection_points = []
        if len(line_segments) >= 3:
            triplets = list(combinations(line_segments, 3))
        else:
            return 0  # not enough line segments if there are only 3

        x, y = symbols("x y")
        # Iterate over all combinations of three line segments

        for (
            ((x1, y1), (x2, y2)),
            ((x3, y3), (x4, y4)),
            ((x5, y5), (x6, y6)),
        ) in tqdm(triplets, desc="Processing triplets"):
            # if check_parallel_lines((((x1, y1), (x2, y2)), ((x3, y3), (x4, y4)), ((x5, y5), (x6, y6)))): continue

            # Equations of lines
            line1 = sp.simplify(Eq(y - y1, (y2 - y1) / (x2 - x1) * (x - x1)))
            line2 = sp.simplify(Eq(y - y3, (y4 - y3) / (x4 - x3) * (x - x3)))
            line3 = sp.simplify(Eq(y - y5, (y6 - y5) / (x6 - x5) * (x - x5)))

            # # Extract slopes
            # slopes = [
            #     sp.simplify(line1.rhs.as_numer_denom()[0] / line1.rhs.as_numer_denom()[1]),
            #     sp.simplify(line2.rhs.as_numer_denom()[0] / line2.rhs.as_numer_denom()[1]),
            #     sp.simplify(line3.rhs.as_numer_denom()[0] / line3.rhs.as_numer_denom()[1])
            # ]
            # if slopes.count(slopes[0]) >= 2 or slopes.count(slopes[1]) >= 2 or slopes.count(slopes[2]) >= 2: continue
            # Solve the system of equations
            intersection_point = sp.solve((line1, line2, line3), (x, y))

            if intersection_point:
                print(intersection_point)
                print(
                    (
                        (x1, y1),
                        (x2, y2),
                        (x3, y3),
                        (x4, y4),
                        (x5, y5),
                        (x6, y6),
                    )
                )
            # Check if the intersection point is within the bounds of all three line segments
            if (
                intersection_point
                and (x1 < intersection_point[x] < x2)
                and (y1 < intersection_point[y] < y2)
                and (x3 < intersection_point[x] < x4)
                and (y3 < intersection_point[y] < y4)
                and (x5 < intersection_point[x] < x6)
                and (y5 < intersection_point[y] < y6)
            ):
                print("\n\n\n\n")
                print("GOT HERE!!!!!!!!!!")
                print(intersection_point)
                print(
                    (
                        (x1, y1),
                        (x2, y2),
                        (x3, y3),
                        (x4, y4),
                        (x5, y5),
                        (x6, y6),
                    )
                )
                intersection_points.append(
                    (intersection_point[x], intersection_point[y])
                )

            if log:
                i += 1
                with open("log.txt", "a") as f:
                    f.write(
                        str(
                            (
                                intersection_point,
                                ((x1, y1), (x2, y2)),
                                ((x3, y3), (x4, y4)),
                                ((x5, y5), (x6, y6)),
                            )
                        )
                    )
                    f.write("\n")
                if i == important_val:
                    visualize_three_line_segments(
                        (
                            ((x1, y1), (x2, y2)),
                            ((x3, y3), (x4, y4)),
                            ((x5, y5), (x6, y6)),
                        )
                    )

        # Filter out duplicate intersection points
        intersection_points = list(set(intersection_points))

        # Save the tuples to a file using pickle
        with open(file_path, "wb") as file:
            pkl.dump(intersection_points, file)

        return intersection_points

    else:
        with open(file_path, "rb") as f:
            intersection_points = pkl.load(f)

        # intersection_points = pkl.load(file_path)
        return intersection_points


def get_line_segments(m):
    line_segments = []
    # create file to output line segments to
    dir_path = "./line segments"
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{m}.pkl")
    if not os.path.exists(file_path):
        equations = generate_isometric_grid_equations(m)
        for equation in tqdm(equations, desc="Processing equations"):

            def small_circle_eqn(x):
                return sqrt(m**2 - x**2)

            def large_circle_eqn(x):
                return sqrt((m + 1) ** 2 - x**2)

            smaller_intersection_points = find_intersection_points(
                equation, small_circle_eqn
            )
            larger_intersection_points = find_intersection_points(
                equation, large_circle_eqn
            )

            # Display the intersection points
            for x_small, x_large in zip(
                smaller_intersection_points, larger_intersection_points
            ):
                line_segments.append(
                    (
                        (x_small, equation(x_small)),
                        (x_large, equation(x_large)),
                    )
                )

        # Save the tuples to a file using pickle
        with open(file_path, "wb") as file:
            pkl.dump(line_segments, file)

        return line_segments
    else:
        with open(file_path, "rb") as f:
            line_segments = pkl.load(f)

        # line_segments = pkl.load(file_path)
        return line_segments


def solve_puzzzle(m, graph=False):
    line_segments = get_line_segments(m)

    # once we get here we have our line segments
    intersection_points = find_line_seg_intersection_points(line_segments, m)

    def euclidean_distance_squared(point):
        return point[0] ** 2 + point[1] ** 2

    def count_and_get_coordinates(coordinates, m):
        unique_distances = set()
        unique_coordinates = {}

        for coord in coordinates:
            distance = euclidean_distance_squared(coord)

            # Check if the distance is within the specified range (m to m+1)
            if m**2 < distance < (m + 1) ** 2:
                unique_distances.add(distance)

                # Add the coordinate to the dictionary with the rounded distance as the key
                if distance not in unique_coordinates:
                    unique_coordinates[distance] = []
                unique_coordinates[distance].append(coord)

        return len(unique_distances), unique_coordinates

    count, unique_coordinates = count_and_get_coordinates(
        intersection_points, m
    )

    if graph:
        # Create figure and axes
        fig, ax = plt.subplots()

        for equation in generate_isometric_grid_equations(m):
            # Plot equation
            x = np.linspace(-m - 3, m + 3, 10000)
            y = np.zeros_like(x)
            for i, x_val in enumerate(x):
                y[i] = equation(x_val)
            ax.plot(x, y, label="Equation")

        small_circle = patches.Circle(
            (0, 0), radius=m, edgecolor="b", facecolor="none"
        )
        ax.add_patch(small_circle)
        ax.set_aspect("equal", adjustable="box")
        ax.add_artist(small_circle)

        large_circle = patches.Circle(
            (0, 0), radius=m + 1, edgecolor="b", facecolor="none"
        )
        ax.add_patch(large_circle)
        ax.set_aspect("equal", adjustable="box")
        ax.add_artist(large_circle)

        # Find and plot intersection point
        for x, y in unique_coordinates:
            ax.plot(x, y, "ro", label="Intersection")

        ax.grid()
        plt.show()

    print(f"unique intersection points: {unique_coordinates}")
    return count


def binary_search_for_puzzle_answer(start_interval, end_interval):
    while start_interval < end_interval:
        m = (start_interval + end_interval) // 2
        print("Checking {m}")
        cur_ans = solve(m)
        with open("answer.txt", "w") as f:
            f.write(
                f"The number of non integer radii circles between {m} and {m+1}: {cur_ans}"
            )
        if cur_ans == 1_000_000:
            with open("answer.txt", "w") as f:
                f.write(
                    f"The answer to this month's puzzle (the m that yields 1 million) is: {m}"
                )
            return m
        if solve(m) < 1_000_000:  # mid was too small
            start_interval = m + 1
        else:
            end_interval = m
        print("\n")
    return -1


# ans = binary_search_for_puzzle_answer(0, 100000)

print("ans: ", solve_puzzzle(11, graph=True))

import math

def is_grid_point(x, y):
    # Check if the given coordinates are grid points
    return x % 1 == 0 and y % 1 == 0

def count_circles(m_range):
    count = 0

    for x in range(1, m_range + 1):
        for y in range(0, x):
            for r in range(m_range * x, (m_range + 1) * x):
                # Equation of a circle: (x-a)^2 + (y-b)^2 = r^2
                # Since (0,0) is a grid point, the equation becomes x^2 + y^2 = r^2
                if is_grid_point(x, y) and x**2 + y**2 <= r**2:
                    count += 1

    return count

def find_m(target_count):
    m = 1
    count = 0

    while count < target_count:
        count = count_circles(m)
        print(f"f({m}) = {count}")
        m += 1

    return m - 1

target_count = 1000000
result = find_m(target_count)
print(f"The value of m such that f(m) = {target_count} is {result}.")

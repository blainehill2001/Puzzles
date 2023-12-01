import gmpy2


def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

def calculate_A(x, z, table):
    if z > x:
        return 0

    if table[x][z] is not None:
        return table[x][z]

    result = 0  # Default value

    if z <= x < 2 * z:
        if (x + z) % 2 == 0:
            result = 1
        else:
            result = 2
    elif x > 4 * z:
        if x % 2 == 0 and z % 2 == 0:
            result = 3
        elif x % 2 == 0 and z % 2 == 1:
            result = 4
        elif x % 2 == 1 and z % 2 == 1:
            result = 5
        else:
            result = 6

    table[x][z] = result
    return result

# Create a cache for a 1000x1000 table
table_size = 1000000
cache = [[-1 for _ in range(table_size)] for _ in range(table_size)]

# Fill the cache
for x in range(table_size):
    for z in range(table_size):
        calculate_A(x, z, cache)

# Example usage:
# x = 7
# z = 3
# result = cache[x][z]
# print(f'A({x}, {z}) = {result}')

def generate_strings(x):
    if x < 1:
        return

    def backtrack(current_string, ones_count):
        if len(current_string) == x:
            yield current_string
        else:
            if ones_count < 2:
                yield from backtrack(current_string + "1", ones_count + 1)
            yield from backtrack(current_string + "0", ones_count)

    yield from backtrack("", 0)

def generate_numbers_and_check(cache):
    for x in range(len(cache)):
        for z in range(len(cache[x])):
            A_xz = cache[x][z]
            if A_xz == 0:
                continue  # Skip zero entries

            len_extra_nines_and_zeroes = z - 1
            for x_string in generate_strings(x):
                the_num = "1" + x_string + "0" + "9"*len_extra_nines_and_zeroes + "9" + "0"*len_extra_nines_and_zeroes + "1" + x_string[::-1] + "1" # Generate the number R
                the_num = gmpy2.mpz(the_num)
                if the_num % 1201 == 845 and the_num % 3565 == 2256:
                    if is_palindrome(the_num**2):
                        print(f"Found R: {the_num}, A({x}, {z}) = {A_xz}")
                        return the_num

# Example usage:
# Assuming you have already filled the cache using the previous code
generate_numbers_and_check(cache)



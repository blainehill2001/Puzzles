import itertools


def generate_magic_squares():
    numbers = list(range(16))

    for perm in itertools.permutations(numbers):
        if (
            sum(perm[0:4])
            == sum(perm[4:8])
            == sum(perm[8:12])
            == sum(perm[12:16])
            == 30
            and sum(perm[0:16:4])
            == sum(perm[1:16:4])
            == sum(perm[2:16:4])
            == sum(perm[3:16:4])
            == 30
            and sum(perm[0:16:5]) == sum(perm[4:16:3]) == 30
        ):
            yield perm


def reverse_ans(x):
    return [int(s.strip()) if s else s.strip() for s in x.split("|")][::-1][
        1:-1
    ]


x = "|12|9|2|13|6|3|15|10|3|2|5| 14 | 13 | 5| 9| 15 | 10|4|8|7| 11 | 12 | 15 | 10 | 7 | 8|4|3|2|6|5| 9| 10 | 11 | 12 |"
x = reverse_ans(x)

print(x)

# from numba import jit
# import math 
# import tqdm
# #test all pairs a, b such that a^b = n^n
# """
# find a number that has 2023 pairs of a,b such that a^b = number^number

# row's value = size(set(a,b)) s.t. a^b = row_idx^row_idx
# """


# def factors(n):
#     result = []
#     for i in range(1, int(n**(n/2) + 1)):
#         if n % i == 0:
#             result.append(i)
#             if i != n // i:
#                 result.append(n // i)
#     return sorted(result)
     
# def get_smallest_bigger_factor(n, factors):
#     for i in factors[:len(factors)-1]:
#         if i > n:
#             if i**0.5 == n: return n
#             return i
#     return n
            

# if __name__ == "__main__":
#     for n in tqdm.tqdm(range(1, 100000)):
#         factors_of_n_squared = factors(n)
#         p = get_smallest_bigger_factor(n, factors_of_n_squared)
#         factors_of_smallest_bigger = factors(p)
#         res = sum(2 if x % 2 == 0 else 1 for x in factors_of_smallest_bigger)
#         if res == 2023:
#             print("found answer")
#             print(n)
#             break
    

# import numba
# from numba import jit
# import tqdm

# @jit(nopython=True)
# def factors(n):
#     result = []
#     for i in range(1, int(n**(n/2)) + 1):
#         if n % i == 0:
#             result.append(i)
#             if i != n // i:
#                 result.append(n // i)
#     return sorted(result)

# @jit(nopython=True)
# def get_smallest_bigger_factor(n, factors):
#     for i in factors[:len(factors)-1]:
#         if i > n:
#             if i**0.5 == n:
#                 return n
#             return i
#     return n

# if __name__ == "__main__":
#     for n in range(1, 100000):
#         factors_of_n_squared = factors(n**2)
#         p = get_smallest_bigger_factor(n, factors_of_n_squared)
#         factors_of_smallest_bigger = factors(p)
#         res = sum(2 if x % 2 == 0 else 1 for x in factors_of_smallest_bigger)
#         if res == 2023:
#             print("found answer") 
#             print(n)
#             break

#         print(n)


def sm_factor(n):
  result = []
  for i in range(2, int(n**0.5) + 1):
      if n % i == 0:
          result.append(i)
          if i != n // i:
              result.append(n // i)
  result.append(n)
  return sorted(result)

def factors(n):
    result = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            result.append(i)
            if i != n // i:
                result.append(n // i)
    return sum([2 if num%2==0 else 1 for num in result])

def func(n):
    
    numbers=sm_factor(n)
    for num in sorted(numbers):
        if num == 1:
            continue
        power = 1
        while num ** power <= n:
            if num ** power == n:
                return factors(power * n)
            power += 1
    return None

def main():
    m = 0
    with open('temp.txt', 'w') as f:
        for n in range(68_000_000,10_000_000_000):
            val = func(n)
            m = max(m, val)
            if n%100000==0:
                f.write(f'{n} {m}\n')
                print(f'{n} {m}\n')
            if m == 2023:
                f.write(f'Solved!: m is {m} at n = {n}')


if __name__ == "__main__":
    main()
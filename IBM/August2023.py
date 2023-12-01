from mpmath import mp, log10, sqrt

# Set precision to a large value, for example, 1000 decimal places
mp.dps = 1000

# Define the expression
numerator = 10 ** 100 + log10(32)
denominator = 2 * log10(3 + 2 * sqrt(2))
x = numerator / denominator

# Print the result
print(x)
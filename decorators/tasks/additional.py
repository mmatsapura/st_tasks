# Task 1
# @time_it
def slow_operation():
    total = 0
    for i in range(10_000_000):
        total += i
    return total

result = slow_operation()
print("Result:", result)

# Task 2
# @cache
def slow_add(a, b):
    print("Computing...")
    return a + b

print(slow_add(2, 3))
print(slow_add(2, 3))
print(slow_add(4, 5))
print(slow_add(2, 3))


# Task 3
functions = []

for n in range(1, 6):
    functions.append(lambda: n * n)

for func in functions:
    print(func())
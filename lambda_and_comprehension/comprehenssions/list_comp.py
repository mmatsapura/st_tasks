#[new_item for item in iterable if condition]


squares = [x**2 for x in range(5)]
#--------------------------------------
evens = [x for x in range(10) if x % 2 == 0]
#--------------------------------------
import math

roots = [math.sqrt(x) for x in range(1, 11)]
#--------------------------------------

matrix = [
    [1, 15, 2],
    [5, 30, 9],
    [12, 3, 99],
]

flat = [num
        for row in matrix
        for num in row
        if num > 10]

# for i in matrix:
#     for j in i:
#         print(j, end=" ")
#----------------------------------------
labels = ["even" if x % 2 == 0 else "odd" for x in range(10)]
#----------------------------------------
#Task: print list of tuples with (student, grade). Print only grades > 10
# expected result
# [
#     ('Ann', 10),
#     ('Ann', 12),
#     ('Bob', 12),
#     ('Bob', 11),
#     ('Kate', 10),
#     ('Kate', 10),
#     ('Max', 12)
# ]





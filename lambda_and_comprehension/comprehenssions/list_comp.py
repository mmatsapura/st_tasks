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
grades = {
    "Ann": [7, 10, 12],
    "Bob": [12, 5, 11],
    "Kate": [8, 10, 10],
    "Max": [4, 12, 6],
}


result = [ (name, grade) 
          for name, marks in grades.items() 
          for grade in marks if grade > 10]

print(result)





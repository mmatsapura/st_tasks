#{key_expr: value_expr for item in iterable if condition}

numbers = [1, 2, 3]
squares = {n: n*n for n in numbers}
#----------------------------------
even_squares = {n: n*n for n in range(10) if n % 2 == 0}

#----------------------------------
def normalize(name: str) -> str:
    return name.strip().title()

names = ["  ivan", "PETRO  ", "olENA"]
clean = {name: normalize(name) for name in names}

#----------------------------------

nums = range(1, 8)

status = {
    n: ("even" if n % 2 == 0 else "odd")
    for n in nums
}

#Task: create a dict with every student good marks (>10)
#Expected result
# {
#     'Ann': [10, 12],
#     'Bob': [12, 11],
#     'Kate': [10, 10],
#     'Max': [12]
# }

grades = {
    "Ann": [7, 10, 12],
    "Bob": [12, 5, 11],
    "Kate": [8, 10, 10],
    "Max": [4, 12, 6],
}

result = {name: [mark for mark in scores if mark > 10]
          for name, scores in grades.items()}

print(result)
#{expression for item in iterable if condition}

s = {x*x for x in range(10)}
#------------------------------------------------------
evens = {x for x in range(20) if x % 2 == 0}
#------------------------------------------------------
unique_letters = {char for char in "banana"}
#------------------------------------------------------

def normalize(word):
    return word.lower().strip()

words = ["Apple", " apple ", "BANANA", "Banana", "Kiwi"]
normalized = {normalize(w) for w in words}

#--------------------------------------------------------
A = {1, 2, 3}
B = {3, 4}

pairs = {(a, b) for a in A for b in B if a != b}

#Task:
# Get marks which are bigger than 10
grades = [
    [5, 12, 11],
    [7, 10, 14],
    [9, 16, 8]
]

# Expected result
# {10, 11, 12, 14, 16}

result = {mark for row in grades for mark in row if mark > 10}
print(result)
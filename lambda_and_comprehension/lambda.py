# lambda arguments: expression
# map() applies a specific function to every item in an iterable and returns the results.
# Syntax: map(function, iterable)
# filter() constructs an iterator from elements of an iterable for which a function returns True.
# Syntax: filter(function, iterable)
square = lambda x: x * x
print(square(5))


f = lambda x: x + 1
f1 = lambda x, y: x + y
f2 = lambda a, b, c: a + b + c

sorted([5, 2, 9], key=lambda x: -x)
nums = [1, 2, 3, 4]
even = list(filter(lambda x: x % 2 == 0, nums))

hosts = ["app01", "db01", "cache01"]
new = list(map(lambda h: f"{h}.company.local", hosts))


from functools import partial
# macros or alias
log = lambda msg: print("[LOG]", msg)
info = partial(log, "[INFO]")

#sort by second argument
items = [(1, 5), (3, 1), (4, 9)]
sorted_items = sorted(items, key=lambda x: x[1])

# map
nums = [1, 2, 3]
doubled = list(map(lambda x: x * 2, nums))

# filter
nums = [1, 2, 3, 4]
even = list(filter(lambda x: x % 2 == 0, nums))

#i f example
even_odd = list(filter(lambda x: "even" if x % 2 == 0 else "odd", even))


# bad example
process = lambda x: (x ** 2 + 1) / 3 if x % 2 else x * 10
# Solutions: comprehensions_tasks

# Task 1
nums = [3, -1, 0, 7, -5, -10, 12]
print([x for x in nums if x > 0])


# Task 2
nums = [3, -1, 0, 7, -5, -10, 12]
print([x**2 if x < 0 else x for x in nums])


# Task 3
users = [
    {"name": "Anna", "age": 22},
    {"name": "Oleg", "age": 17},
    {"name": "Ivan", "age": 30},
    {"name": "Olga", "age": 19},
]
print([u["name"] for u in users if u["age"] > 18])


# Task 4
grades = {
    "Ann": [7, 10, 12],
    "Bob": [12, 5, 11],
    "Kate": [8, 10, 10],
}
print([g for marks in grades.values() for g in marks if g > 10])


# Task 5
users = [
    {"name": "Anna", "age": 22},
    {"name": "Oleg", "age": 17},
    {"name": "Ivan", "age": 30},
]
print({u["name"]: u["age"] for u in users if u["age"] >= 18})


# Task 6
words = ["apple", "hi", "banana", "ok"]
print({w: len(w) for w in words})


# Task 7
categories = ["Food", "drink", "FOOD", "Snack", "Drink"]
print({c.lower() for c in categories})


# Task 8
marks = [
    [5, 12, 11],
    [7, 10, 12],
    [9, 10, 8],
]
print({m for row in marks for m in row if m >= 10})


# Task 9
nums = [1, 2, 3, 4, 5, 6]
print(list(x ** 2 for x in nums if x % 2 == 0))


# Task 10
def errors(lines):
    for line in lines:
        if "ERROR" in line:
            yield line


lines = [
    "INFO started",
    "ERROR disk full",
    "INFO ok",
    "ERROR timeout",
]
for line in errors(lines):
    print(line)


# Task 11
orders = [
    {"user": "Ann", "total": 120, "paid": True},
    {"user": "Bob", "total": 40, "paid": False},
    {"user": "Ann", "total": 80, "paid": True},
    {"user": "Kate", "total": 15, "paid": True},
    {"user": "Bob", "total": 10, "paid": False},
]
print({
    user: sum(o["total"] for o in orders if o["user"] == user and o["paid"])
    for user in {o["user"] for o in orders if o["paid"]}
})


# Task 12
matrix = [
    [1, 15, 2],
    [5, 30, 9],
    [12, 3, 99],
]
print([
    (row, col, value)
    for row, values in enumerate(matrix)
    for col, value in enumerate(values)
    if value > 10
])


# Task 13
articles = [
    {"title": "a", "tags": ["python", "oop"]},
    {"title": "b", "tags": ["python", "sql"]},
    {"title": "c", "tags": ["git", "sql", "python"]},
]
print({
    tag
    for article in articles
    for tag in article["tags"]
    if sum(tag in other["tags"] for other in articles) >= 2
})


# Task 14
logs = [
    "ERROR:disk full",
    "INFO:started",
    "ERROR:timeout",
    "INFO:ok",
    "WARNING:slow",
]
print({
    level: [line.split(":", 1)[1] for line in logs if line.startswith(level + ":")]
    for level in {line.split(":", 1)[0] for line in logs}
})


# Task 15
def out_of_stock(shops):
    for shop, products in shops.items():
        for product in products:
            if product["qty"] == 0:
                yield shop, product["name"]


shops = {
    "center": [
        {"name": "apple", "qty": 0},
        {"name": "milk", "qty": 3},
    ],
    "west": [
        {"name": "bread", "qty": 0},
        {"name": "milk", "qty": 1},
    ],
}
for item in out_of_stock(shops):
    print(item)

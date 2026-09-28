# Solutions: lambda_tasks


# Task 1 (first.py)
# Find negative numbers and replace them with zero
nums = [3, -1, 0, 7, -5, -10, 12]
print(list(map(lambda x: 0 if x < 0 else x, nums)))
# [3, 0, 0, 7, 0, 0, 12]


# Task 2 (second.py)
# Found users older than 18 and name starts with "O"
users = [
    {"name": "Anna", "age": 22},
    {"name": "Oleg", "age": 17},
    {"name": "Ivan", "age": 30},
    {"name": "Olga", "age": 19},
]
print(list(filter(
    lambda u: u["age"] > 18 and u["name"].startswith("O"),
    users,
)))
# [{'name': 'Olga', 'age': 19}]


# Task 3 (third.py)
# Sort users by age in reverse order
users = [
    {"name": "Anna", "age": 22},
    {"name": "Oleg", "age": 17},
    {"name": "Ivan", "age": 30},
]
print(sorted(users, key=lambda u: u["age"], reverse=True))
# Ivan 30, Anna 22, Oleg 17


# Task 4 (fourth.py)
# price <= 10 без змін, price > 10 збільшити на 50%
products = [
    {"name": "apple", "price": 10},
    {"name": "banana", "price": 5},
    {"name": "cherry", "price": 20},
]
print(list(map(
    lambda p: {**p, "price": p["price"] * 1.5 if p["price"] > 10 else p["price"]},
    products,
)))
# apple 10, banana 5, cherry 30.0

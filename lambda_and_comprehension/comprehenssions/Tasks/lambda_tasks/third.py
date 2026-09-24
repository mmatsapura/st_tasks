# Sort users by age in reverse order
users = [
    {"name": "Anna", "age": 22},
    {"name": "Oleg", "age": 17},
    {"name": "Ivan", "age": 30}
]

result = sorted(users, key=lambda user: user['age'], reverse=True)
print(result)
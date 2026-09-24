# Found users older than 18 and name starts with "O"
users = [
    {"name": "Anna", "age": 22},
    {"name": "Oleg", "age": 17},
    {"name": "Ivan", "age": 30},
    {"name": "Olga", "age": 19}
]

result = list(filter(lambda user: user['age'] > 18 and user['name'].startswith('O'), users))
print(result)
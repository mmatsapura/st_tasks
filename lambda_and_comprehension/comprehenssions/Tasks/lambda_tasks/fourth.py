#Create list of products where price that is below 10 stay the same it and if bigger than 10 increase price by 50 percents
products = [
    {"name": "apple", "price": 10},
    {"name": "banana", "price": 5},
    {"name": "cherry", "price": 20}
]

result = list(map(lambda user: {'name': user['name'], 'price': user['price'] * 1.5 if user['price'] > 10 else user['price']}, products))
print(result)
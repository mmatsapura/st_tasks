'''Создай два декоратора:
to_json - возвращает результат функции в виде JSON-строки.
from_json - преобразует JSON-строку в объект Python и передаёт его в функцию.'''


# @to_json
def get_data():
    return {"name": "John", "age": 25}

# @from_json
def print_data(data):
    print(data["name"], data["age"])

json_str = get_data()
print_data(json_str)

#Expected result
# {"name": "John", "age": 25}
# John 25
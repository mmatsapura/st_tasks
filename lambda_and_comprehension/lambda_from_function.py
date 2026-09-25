def select_operation(choice):
    if choice == 1:
        return lambda a, b: a + b
    elif choice == 2:
        return lambda a, b: a - b
    else:
        return lambda a, b: a * b


operation = select_operation(1)
print(operation(10, 6))

operation = select_operation(2)
print(operation(10, 6))

operation = select_operation(3)
print(operation(10, 6))
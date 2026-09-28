def do_operation(a, b, operation):
    result = operation(a, b)
    print(f"result = {result}")


do_operation(5, 4, lambda a, b: a + b)
do_operation(5, 4, lambda a, b: a * b)
def do_twice(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        return value
    return wrapper


@do_twice
def return_greeting(name):
     print("Creating greeting")
     return f"Hi {name}"

print(return_greeting("Alex"))
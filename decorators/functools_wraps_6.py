import functools

# Useful for metadata
def do_twice(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice


@do_twice
def say_whee():
    print("Whee!")

help(say_whee)
print(f"Function name: {say_whee.__name__}")
print(f"Documentation: {say_whee.__doc__}")

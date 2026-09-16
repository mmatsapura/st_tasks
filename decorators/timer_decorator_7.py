import functools
import time

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__}() in {run_time:.4f} secs")
        return value
    print(id(wrapper_timer))
    return wrapper_timer


@timer
def function_to_wait():
    time.sleep(1)
    print("function_to_wait")

@timer
def say_my_name(name):
    print("say_my_name")
    return name

say_my_name = timer(say_my_name)


def say_my_name_in_normal_way(name="bob"):
    print("say_my_name_in_normal_way")
    return name


say_my_name_in_normal_way = timer(say_my_name_in_normal_way)
print(id(say_my_name_in_normal_way))

# print(function_to_wait())
# print(say_my_name("Maksym"))
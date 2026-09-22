import time
import functools


def repeat(nums_to_repeat=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(nums_to_repeat):
                value = func(*args, **kwargs)
            return value
        return wrapper
    return decorator



@repeat(nums_to_repeat=2)
def function_to_repeat(api_url):
    print("Repeat function")
    time.sleep(1)
    return api_url

@repeat
def function_to_repeat_1(api_url):
    print("Repeat function")
    time.sleep(1)
    return api_url

function_to_repeat_1(api_url="https://google.com")
function_to_repeat(api_url="https://google.com")
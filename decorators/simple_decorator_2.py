def decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper


def say_whee():
    print("Whee!")

say_whee = decorator(say_whee)
say_whee()

#--------------------------------------------
from datetime import datetime

def not_during_the_night(func):
    def wrapper_skdfjnhskfhsdf():
        if 7 <= datetime.now().hour < 22:
            func()
        else:
            pass  # Hush, the neighbors are asleep
    return wrapper_skdfjnhskfhsdf

def say_whee_day():
    print("Whee day!")

say_whee_dt = not_during_the_night(say_whee_day)

say_whee_dt()
class Timer:
    def __init__(self, func=None, *, repeat=1):
        self.repeat = repeat
        self.func = func
        self.is_wrapped = func is not None

    def __call__(self, *args, **kwargs):
        if not self.is_wrapped:
            func = args[0]
            return Timer(func, repeat=self.repeat)
        else:
            # without parentheses
            for _ in range(self.repeat):
                self.func(*args, **kwargs)



# @Timer
# def say_hello():
#     print("Hello!")

@Timer(repeat=3)
def say_hi():
    print("Hi!")

# say_hello()
say_hi()

# greet = Timer(repeat=3)(greet)
#greet = Timer(greet)


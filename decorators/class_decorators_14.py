class Repeat:
    def __init__(self, func, times=1):
        self.times = times
        self.func = func

    def __call__(self, *args, **kwargs):
        for _ in range(self.times):
            self.func(*args, **kwargs)


@Repeat
def greet(name):
    print(f"Hi, {name}!")

greet("John")

# repeat_instance = Repeat(times=3)     # __init__
# greet = repeat_instance.__call__(greet)

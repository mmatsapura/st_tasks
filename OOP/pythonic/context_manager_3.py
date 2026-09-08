# Демо 3. Контекстный менеджер: __enter__ / __exit__
#
# with сам вызовет вход и выход. Даже если внутри ошибка,
# __exit__ всё равно выполнится — это главное зачем он нужен.
#
# __exit__ получает тип ошибки, сам объект и traceback.
# return False (или None) — ошибка летит дальше.
# return True — ошибку проглотили (так почти никогда не делают).


import time


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, traceback):
        elapsed = time.perf_counter() - self.start
        print(f"заняло {elapsed:.4f} с")
        if exc_type is not None:
            print(f"внутри была ошибка: {exc}")
        return False


class Log:
    def __init__(self, path):
        self.path = path
        self.file = None

    def __enter__(self):
        self.file = open(self.path, "w", encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc, traceback):
        if self.file is not None:
            self.file.close()
        return False


with Timer():
    sum(range(100_000))

with Log("timer_demo.txt") as file:
    file.write("session ok\n")

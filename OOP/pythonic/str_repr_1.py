# Демо 1. __str__ и __repr__
#
# __repr__ — для разработчика: однозначный снимок объекта
# (удобно в консоли, логах, списке объектов).
# __str__ — для человека: короткая фраза в print().
# Если __str__ нет, print берёт __repr__.
# Если нет обоих — дефолт: <__main__.Book object at 0x...>


class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __repr__(self):
        return f"Book({self.title!r}, {self.pages})"

    def __str__(self):
        return f"{self.title} ({self.pages} стр.)"


book = Book("Python", 400)
print(book)                    # Python (400 стр.)   <- __str__
print(repr(book))              # Book('Python', 400) <- __repr__

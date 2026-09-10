# Демо 4b. __post_init__ у датакласса
#
# @dataclass сам пишет __init__ и сразу после него вызывает __post_init__.
# Сюда ставят проверки: пустая строка, цена <= 0.
# Без этого Product("", -10) спокойно создастся.


from dataclasses import dataclass


@dataclass
class Product:
    title: str
    price: float

    def __post_init__(self):
        if not self.title:
            raise ValueError("title is empty")
        if self.price <= 0:
            raise ValueError("price must be greater than 0")


@dataclass(frozen=True)
class Plate:
    number: str

    def __post_init__(self):
        # frozen: поля уже стоят, менять их нельзя — только проверить.
        if not self.number:
            raise ValueError("number is empty")


book = Product("Python", 400)
print(book)

try:
    Product("", 400)
except ValueError as error:
    print(error)

try:
    Product("Python", 0)
except ValueError as error:
    print(error)

print(Plate("AA1234"))
# Plate("")  # ValueError

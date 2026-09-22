from dataclasses import dataclass, field


@dataclass(frozen=True)
class Book:
    title: str
    author: str
    year: int
    pages: int = field(default=100)

    def __post_init__(self):
        if self.year < 0:
            raise ValueError('Год не может быть отрицательным числом')



book1 = Book('Learn Python', 'John Smith', 2023)
book2 = Book('Harry Potter', 'Vanilla', 2010, 565)
book3 = Book('Harry Potter', 'Vanilla', 2010, 565)
# book4 = Book('Harry', 'Malina', -2010)

print(book1)
print(book2)

print(book1 == book2)
print(book3 == book2)


# Создай dataclass Book, который будет хранить информацию о книге.
# Требования:
# Класс должен содержать следующие поля:
# title (строка) — название книги
# author (строка) — автор книги
# year (целое число) — год издания
# pages (целое число) — количество страниц
# Используйте значение по умолчанию для поля pages — пусть по умолчанию будет 100.
# Сделайте класс неизменяемым (frozen=True).
# Создайте два экземпляра книги и выведите их на экран.
# Сравните эти книги с помощью оператора == и выведите результат.
# Используйте __post_init__, чтобы проверять, что year не отрицательный.
# The duck-typing contract is only a convention.
# If one class uses a different method name, the common loop breaks.


import math


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square:
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def half_of_perimeter(self):
        return (self.a + self.b + self.c) / 2

    def area_for_triangle(self):
        # Different name: this is NOT area(), so the loop below cannot see it.
        p = self.half_of_perimeter()
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))


shapes = [
    Rectangle(4, 5),
    Square(6),
    Triangle(3, 4, 5),
]

for shape in shapes:
    try:
        print(shape.area())
    except AttributeError as error:
        print(f"{type(shape).__name__}: {error}")
# 20
# 36
# Triangle: 'Triangle' object has no attribute 'area'

# hasattr() can skip the bad object, but it does not force anyone to implement area().
# print(hasattr(Triangle(3, 4, 5), "area"))  # False

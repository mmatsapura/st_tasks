# Duck typing: "if it has area(), we can use it as a shape".
# There is no common parent. The loop only needs the same method name.


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

    def area(self):
        # Same method name as Rectangle and Square — that is enough for the loop.
        p = self.half_of_perimeter()
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))


shapes = [
    Rectangle(4, 5),
    Square(6),
    Triangle(3, 4, 5),
]

for shape in shapes:
    print(shape.area())
# 20
# 36
# 6.0

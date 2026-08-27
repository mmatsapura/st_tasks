# Same shapes as in duck_typing / missing_method, but now Shape is an ABC.
# Python checks the area() contract when you create an object, not later
# in the loop. That answers: "how to be sure about implementation?"


import math
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def half_of_perimeter(self):
        return (self.a + self.b + self.c) / 2

    def area(self):
        # Must be named area() — otherwise Triangle is still abstract.
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

# class Circle(Shape):
#     def __init__(self, radius):
#         self.radius = radius
#     # no area() here
#
# Circle(3)  # TypeError: Can't instantiate abstract class Circle
#            # with abstract method area
#
# Contrast with inheritance_polymorphism_3.py:
# there Circle(3) succeeded and failed only on .area().

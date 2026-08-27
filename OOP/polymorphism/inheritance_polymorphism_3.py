# Inheritance polymorphism: one parent type, many child implementations.
# The loop calls shape.area() on a Shape, but the child version runs.
# This is still not a hard guarantee — a child can forget to override area().


import math


class Shape:
    def area(self):
        raise NotImplementedError("Subclass must implement area().")


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

    def area(self):
        p = (self.a + self.b + self.c) / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))


def print_area(shape: Shape):
    # Callers depend on the parent type. The real method comes from the child.
    print(shape.area())


shapes = [
    Rectangle(4, 5),
    Square(6),
    Triangle(3, 4, 5),
]

for shape in shapes:
    print_area(shape)
# 20
# 36
# 6.0

print(isinstance(Square(6), Shape))  # True

# A child that forgets area() is still a Shape. The error appears only when
# area() is called, not when the object is created:
#
# class Circle(Shape):
#     def __init__(self, radius):
#         self.radius = radius
#
# Circle(3)          # OK — object is created
# Circle(3).area()   # NotImplementedError

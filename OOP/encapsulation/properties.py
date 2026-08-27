# @property turns a method into an attribute-like interface.
# Callers write obj.age instead of obj.get_age(), while you still
# keep validation and a private backing field.


class Person:
    def __init__(self, name, age):
        self.name = name
        # The real data lives in a private attribute.
        # The public API is the "age" property below.
        self.__age = None
        self.age = age  # goes through the setter

    @property
    def age(self):
        # Getter: runs when you read person.age
        return self.__age

    @age.setter
    def age(self, value):
        # Setter: runs when you assign person.age = ...
        if not isinstance(value, int):
            raise TypeError("Age must be an integer.")
        if value < 0 or value > 130:
            raise ValueError("Age must be between 0 and 130.")
        self.__age = value

    @age.deleter
    def age(self):
        # Deleter: runs when you call del person.age
        print("Age was deleted.")
        self.__age = None

    @property
    def is_adult(self):
        # Read-only property: no setter, so it cannot be assigned from outside.
        return self.__age is not None and self.__age >= 18


person = Person("Oleg", 20)

print(person.age)          # 20  — looks like an attribute, calls the getter
print(person.is_adult)     # True

person.age = 17            # calls the setter
print(person.age)          # 17
print(person.is_adult)     # False

# person.age = -5          # ValueError from the setter
# person.is_adult = True   # AttributeError: read-only property

del person.age             # calls the deleter
print(person.age)          # None

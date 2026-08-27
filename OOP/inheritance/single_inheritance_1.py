# Single inheritance: one child, one parent.
# The child reuses the parent and may override methods or add new ones.


class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def info(self):
        # Uses self.speak(), so a child override is picked up automatically.
        return f"{self.name}: {self.speak()}"


class Dog(Animal):
    def speak(self):
        # Override: replace the parent version for this class.
        return "Woof!"

    def fetch(self):
        # Extra behavior that exists only on the child.
        return f"{self.name} brings the ball."


dog = Dog("Rex")

print(dog.info())              # Rex: Woof!  — info() from Animal, speak() from Dog
print(dog.fetch())
print(isinstance(dog, Dog))    # True
print(isinstance(dog, Animal)) # True
print(Dog.__bases__)           # (<class '__main__.Animal'>,)

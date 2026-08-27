# Hierarchical inheritance: several children share one parent.
# Each child gets the common API and then specializes it.


class Employee:
    def __init__(self, name, salary):
        self.name = name
        self._salary = salary  # protected: meant for subclasses, not for outside code

    def info(self):
        return f"{self.name}, salary {self._salary}"


class Developer(Employee):
    def __init__(self, name, salary, language):
        super().__init__(name, salary)
        self.language = language

    def work(self):
        return f"{self.name} writes {self.language} code."


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def work(self):
        return f"{self.name} leads a team of {self.team_size}."


dev = Developer("Oleg", 3000, "Python")
boss = Manager("Anna", 5000, 8)

print(dev.info())
print(dev.work())
print(boss.info())
print(boss.work())

# Both children are Employees, but they are not related to each other.
print(isinstance(dev, Employee))   # True
print(isinstance(boss, Employee))  # True
print(isinstance(dev, Manager))    # False

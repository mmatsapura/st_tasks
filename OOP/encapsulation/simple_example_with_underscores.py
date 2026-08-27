# Public, protected, and private attributes in Python are a naming convention,
# not a hard language restriction. Underscores signal how an attribute should be used.


class Employee:
    def __init__(self, name, salary, password):
        # Public: intended for free access from anywhere.
        self.name = name

        # Protected: a single leading underscore. Other code may still read
        # or write it, but the name means "for internal / subclass use only".
        self._salary = salary

        # Private: a double leading underscore. Python name-mangles it to
        # _Employee__password, which makes accidental access from outside harder.
        self.__password = password

    def show_info(self):
        # Inside the class, all three access levels are available.
        print(f"Name: {self.name}")
        print(f"Salary: {self._salary}")
        print(f"Password: {self.__password}")


# ---------------------------------------------------------------------------
# Public
# ---------------------------------------------------------------------------

worker = Employee("Anna", 2500, "secret123")

print(worker.name)          # OK: public attribute
worker.name = "Maria"       # OK: public attribute can be changed freely
print(worker.name)


# ---------------------------------------------------------------------------
# Protected
# ---------------------------------------------------------------------------

# This works, but by convention you should not touch _salary from outside.
print(worker._salary)
worker._salary = 3000
print(worker._salary)


# ---------------------------------------------------------------------------
# Private
# ---------------------------------------------------------------------------

# Direct access by the original name fails: AttributeError.
# print(worker.__password)

# Name mangling still lets you reach it (not recommended):
print(worker._Employee__password)

worker.show_info()

# Encapsulation + inheritance.
# Protected (_name) is the level meant for subclasses.
# Private (__name) is mangled per class, so a child does not see it
# under the original name — even though it still inherits the object.


class Employee:
    def __init__(self, name, salary, password):
        self.name = name
        self._salary = salary          # protected: subclasses may use this
        self.__password = password     # private: stored as _Employee__password

    def _monthly_bonus(self):
        # Protected method: helpers for this class and its children.
        return round(self._salary * 0.1, 2)

    def __secret_token(self):
        # Private method: name-mangled to _Employee__secret_token.
        return f"token-{self.__password}"

    def payroll_line(self):
        return f"{self.name}: {self._salary} + bonus {self._monthly_bonus()}"


class Manager(Employee):
    def give_raise(self, amount):
        # OK: a subclass is allowed to touch protected data.
        self._salary += amount

    def bonus_report(self):
        # OK: protected methods are part of the inherited internal API.
        return f"Bonus for {self.name}: {self._monthly_bonus()}"

    def try_private_attr(self):
        # Looks for _Manager__password — it does not exist.
        # The real field is _Employee__password.
        try:
            return self.__password
        except AttributeError as error:
            return f"Cannot read __password in Manager: {error}"

    def try_private_method(self):
        try:
            return self.__secret_token()
        except AttributeError as error:
            return f"Cannot call __secret_token in Manager: {error}"

    def force_private_access(self):
        # Works, but breaks encapsulation. Do not do this in real code.
        return self._Employee__password


class TeamLead(Manager):
    # Multilevel: protected members stay available down the chain.
    def cut_salary(self, amount):
        self._salary -= amount
        return self._salary


boss = Manager("Anna", 5000, "qwerty")

print(boss.payroll_line())
boss.give_raise(500)
print(boss.bonus_report())
print(boss.try_private_attr())
print(boss.try_private_method())
print("Forced access:", boss.force_private_access())  # qwerty — possible, not allowed by design

lead = TeamLead("Oleg", 6000, "secret")
print("After cut:", lead.cut_salary(200))
print(lead.payroll_line())

# Outside code can still read _salary (Python does not forbid it),
# but the underscore means "do not touch this from here".
print("Outside read of protected:", boss._salary)

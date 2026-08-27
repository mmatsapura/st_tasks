# Getters and setters hide internal data behind methods.
# That lets you validate values, log changes, or change storage later
# without rewriting every place that uses the class.


class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        # Keep the real balance private. Callers should use get/set methods.
        self.__balance = 0
        self.set_balance(balance)

    def get_balance(self):
        # Getter: controlled read access to the hidden value.
        return self.__balance

    def set_balance(self, amount):
        # Setter: controlled write access. Reject invalid data here.
        if not isinstance(amount, (int, float)):
            raise TypeError("Balance must be a number.")
        if amount < 0:
            raise ValueError("Balance cannot be negative.")
        self.__balance = amount

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive.")
        self.set_balance(self.get_balance() + amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive.")
        if amount > self.get_balance():
            raise ValueError("Not enough money on the account.")
        self.set_balance(self.get_balance() - amount)


account = BankAccount("Ivan", 100)

print(account.get_balance())   # 100

account.set_balance(250)
print(account.get_balance())   # 250

account.deposit(50)
account.withdraw(80)
print(account.get_balance())   # 220

# Direct access to the private field is not the intended API:
# print(account.__balance)     # AttributeError

# Invalid updates are blocked by the setter:
# account.set_balance(-10)     # ValueError

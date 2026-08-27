# ABC (Abstract Base Class) makes the interface mandatory.
# A subclass that does not implement pay() cannot even be created.


from abc import ABC, abstractmethod


class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        # No body on purpose: every child must provide its own version.
        pass


class CreditCardPayment(Payment):
    def pay(self, amount):
        print(f"Payed {amount} usd by card")


class PayPalPayment(Payment):
    def pay(self, amount):
        print(f"Payed {amount} usd by PayPal")


def process_payment(payment: Payment, amount: float):
    # payment can be any concrete Payment subclass.
    payment.pay(amount)


process_payment(CreditCardPayment(), 100)
process_payment(PayPalPayment(), 250)

# The abstract class itself cannot be instantiated:
# Payment()  # TypeError: Can't instantiate abstract class Payment

# A child that forgets pay() also cannot be instantiated:
# class BankTransfer(Payment):
#     pass
#
# BankTransfer()  # TypeError: Can't instantiate abstract class BankTransfer
#                 # with abstract method pay

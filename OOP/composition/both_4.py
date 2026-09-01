# Демо 4. Оба отношения в одном объекте — так чаще бывает в жизни.
#
# Заказ в кафе:
#   клиент пришёл с улицы и уйдёт с чеком — агрегация;
#   строки "2 латте" родились вместе с заказом и без него бессмысленны —
#   композиция.
#
# Проверка на понимание:
#   тот же Customer в двух заказах — норма (агрегация, `is`);
#   ту же Line не перекладывают в чужой заказ (композиция).
#   class Order(Customer) было бы снова is-a вместо has-a.


class Customer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Customer({self.name})"


class Line:
    def __init__(self, title, qty):
        self.title = title
        self.qty = qty

    def __str__(self):
        return f"{self.qty} x {self.title}"


class Order:
    def __init__(self, customer):
        # Агрегация: клиента создали снаружи и передали.
        self.customer = customer
        # Композиция: список строк пустой, заполним сами.
        self.lines = []

    def add(self, title, qty):
        self.lines.append(Line(title, qty))

    def __str__(self):
        items = ", ".join(str(line) for line in self.lines)
        return f"Order for {self.customer.name}: {items}"


olya = Customer("Olya")

morning = Order(olya)
morning.add("Latte", 2)
morning.add("Croissant", 1)

evening = Order(olya)
evening.add("Tea", 1)

print(morning)                           # Order for Olya: 2 x Latte, 1 x Croissant
print(morning.customer is olya)          # True
print(evening.customer is olya)          # True — один человек, два заказа
print(olya)                              # Customer(Olya) — жив без заказа
print(morning.lines[0])                  # 2 x Latte — строка живёт в заказе

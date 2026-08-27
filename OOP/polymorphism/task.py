# Задание: Полиморфизм
#
# Сделай абстрактный канал уведомлений и несколько реализаций.
# Общий код должен вызывать один и тот же метод send(), не зная,
# email это, sms или push. Контракт обязан быть обязательным (ABC).
#
# Требования:
#
# 1. Класс Notifier(ABC)
#    - абстрактный метод channel() — возвращает строку с названием канала
#    - абстрактный метод send(message) — возвращает строку с результатом отправки
#    - сам Notifier создавать нельзя
#
# 2. send(message):
#    - message должен быть непустой строкой
#    - иначе TypeError или ValueError
#
# 3. Класс EmailNotifier(Notifier)
#    Конструктор: EmailNotifier(email)
#    - email — публичный атрибут, в строке должен быть символ "@"
#    - иначе ValueError
#    - channel() возвращает "email"
#    - send(message) возвращает: "Email to {email}: {message}"
#
# 4. Класс SmsNotifier(Notifier)
#    Конструктор: SmsNotifier(phone)
#    - phone — публичный атрибут
#    - channel() возвращает "sms"
#    - send(message) возвращает: "SMS to {phone}: {message}"
#
# 5. Класс PushNotifier(Notifier)
#    Конструктор: PushNotifier(device_id)
#    - device_id — публичный атрибут
#    - channel() возвращает "push"
#    - send(message) возвращает: "Push to {device_id}: {message}"
#
# 6. Функция notify_all(notifiers, message)
#    - принимает список Notifier и текст
#    - вызывает send(message) у каждого элемента
#    - возвращает список строк
#
# 7. __str__ для каждого канала:
#    EmailNotifier("anna@mail.com") -> EmailNotifier(anna@mail.com)
#    SmsNotifier("+380991112233")   -> SmsNotifier(+380991112233)
#    PushNotifier("device-7")       -> PushNotifier(device-7)
#
# Пример:
#     email = EmailNotifier("anna@mail.com")
#     sms = SmsNotifier("+380991112233")
#     push = PushNotifier("device-7")
#
#     print(email.channel())            # email
#     print(sms.send("Hello"))          # SMS to +380991112233: Hello
#     print(email)                      # EmailNotifier(anna@mail.com)
#
#     print(notify_all([email, sms, push], "Exam tomorrow"))
#     # ['Email to anna@mail.com: Exam tomorrow',
#     #  'SMS to +380991112233: Exam tomorrow',
#     #  'Push to device-7: Exam tomorrow']
#
#     print(isinstance(email, Notifier))  # True
#
# Некорректные случаи (должны выбрасывать исключение):
#     Notifier()                           # TypeError
#     EmailNotifier("anna.mail.com")       # ValueError
#     email.send("")                       # ValueError
#     email.send(123)                      # TypeError
#
#     class BadNotifier(Notifier):
#         pass
#     BadNotifier()                        # TypeError (нет send и channel)

# Задание: Композиция и агрегация
#
# Сделай капсулу времени.
# Композиция: часть создаётся внутри целого и без него не нужна.
# Агрегация: целое хранит уже существующий объект, он живёт своей жизнью.
#
# Записка рождается в капсуле — композиция.
# Свидетель приходит снаружи и может быть в другой капсуле — агрегация.
#
# Требования:
#
# 1. Класс Person(name)
#    - name — публичный атрибут, непустая строка, иначе ValueError
#    - __str__: Person(Ira)
#
# 2. Класс Note(text)
#    - text — публичный атрибут
#    - снаружи Note(...) в рабочем коде не вызываем: записку создаёт Capsule
#    - __str__: Note(We passed the exam)
#
# 3. Класс Capsule(title)
#    - title — публичный атрибут, непустая строка, иначе ValueError
#    - witnesses — список людей, сначала пустой
#    - notes — список записок, сначала пустой
#    - капсула сначала открыта
#
# 4. add_witness(person) — агрегация
#    - person должен быть Person, иначе TypeError
#    - одного человека дважды нельзя — ValueError
#    - после seal() добавлять нельзя — ValueError
#    - в список кладётся тот же объект, который передали
#
# 5. add_witnesses(*people)
#    - принимает несколько людей сразу
#    - если не передали никого — ValueError
#    - для каждого вызывает add_witness
#
# 6. write(text) — композиция
#    - text — непустая строка, иначе TypeError или ValueError
#    - создаёт Note(text) внутри метода и кладёт в notes
#    - после seal() писать нельзя — ValueError
#
# 7. write_from_file(path)
#    - открыть файл через with open(path, encoding="utf-8")
#    - каждая непустая строка — новая записка через write()
#    - пустые строки и строки, которые начинаются с #, пропустить
#    - у строки убрать пробелы по краям (strip)
#    - если после этого записок не осталось — ValueError
#    - после seal() читать файл в капсулу нельзя — ValueError
#    - файл notes_2026.txt лежит рядом с этим заданием
#
# 8. find_note(fragment)
#    - вернуть первую записку, в чьём text есть fragment (оператор in)
#    - поиск напиши циклом for ... else:
#      нашли — return внутри цикла
#      не нашли — ValueError в else у for (else относится к циклу, не к if)
#    - fragment — непустая строка, иначе ValueError
#
# 9. preview()
#    - вернуть список строк с номерами через enumerate(..., start=1)
#    - ["1. We passed the exam", "2. Hello future"]
#
# 10. dump(path)
#     - записать тексты записок в файл, по одной на строку
#     - with open(path, "w", encoding="utf-8")
#     - после seal() дамп разрешён: капсулу уже не меняем, только читаем
#
# 11. seal()
#     - закрывает капсулу
#     - повторный seal() — ValueError
#
# 12. __str__ для Capsule:
#     Capsule(2026): 2 witnesses, 3 notes, open
#     Capsule(2026): 2 witnesses, 3 notes, sealed
#
# 13. Функция capsules_of(person, capsules)
#     - возвращает список title капсул, где этот человек есть в witnesses
#     - сравнение людей — тот же объект, не совпадение имени
#
# Пример:
#     ira = Person("Ira")
#     oleg = Person("Oleg")
#     maxim = Person("Max")
#     box = Capsule("2026")
#
#     box.add_witness(ira)
#     box.add_witnesses(oleg, maxim)
#     box.write_from_file("notes_2026.txt")
#
#     print(box.witnesses[0] is ira)       # True
#     print(box.witnesses[2] is maxim)     # True
#     print(len(box.notes))                # 3
#     print(box.find_note("exam"))         # Note(We passed the exam)
#     print(box.preview())
#     # ['1. We passed the exam', '2. Hello future', '3. До встречи в 2030']
#     print(box)                           # Capsule(2026): 3 witnesses, 3 notes, open
#
#     box.seal()
#     box.dump("capsule_out.txt")          # файл с тремя строками
#     print(box)                           # Capsule(2026): 3 witnesses, 3 notes, sealed
#
#     later = Capsule("2030")
#     later.add_witness(ira)
#     print(capsules_of(ira, [box, later]))  # ['2026', '2030']
#
# Некорректные случаи (должны выбрасывать исключение):
#     Person("")                           # ValueError
#     Capsule("")                          # ValueError
#
#     pack = Capsule("test")
#     pack.add_witness("Ira")              # TypeError
#     pack.add_witnesses()                 # ValueError
#     pack.add_witness(ira)
#     pack.add_witness(ira)                # ValueError (уже есть)
#     pack.write("")                       # ValueError
#     pack.write(123)                      # TypeError
#     pack.find_note("exam")               # ValueError (записок ещё нет)
#     pack.seal()
#     pack.seal()                          # ValueError
#     pack.write("too late")               # ValueError
#     pack.write_from_file("notes_2026.txt")  # ValueError
#     pack.add_witness(oleg)               # ValueError

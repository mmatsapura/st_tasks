# Задание: Композиция и агрегация



class Person:

    def __init__(self, name):
        if not name:
            raise ValueError
        if not isinstance(name, str):
            raise TypeError
        self.name = name

    def __str__(self):
        return f'{self.__class__.__name__}({self.name})'


class Note:

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f'{self.__class__.__name__}({self.text})'


class Capsule:

    def __init__(self, title):
        if not title:
            raise ValueError
        if not isinstance(title, str):
            raise TypeError
        self.title = title
        self.witnesses = []
        self.notes = []
        self.is_open = True

    def add_witness(self, person):
        if not self.is_open:
            raise ValueError
        if not isinstance(person, Person):
            raise TypeError
        if person in self.witnesses:
            raise ValueError
        self.witnesses.append(person)

    def add_witnesses(self, *people):
        if not people:
            raise ValueError
        for person in people:
            self.add_witness(person)

    def write(self, text):
        if not self.is_open:
            raise ValueError
        if not text:
            raise ValueError
        if not isinstance(text, str):
            raise TypeError
        self.notes.append(Note(text))

    def write_from_file(self, path):
        if not self.is_open:
            raise ValueError
        added_count = 0
        with open(path, encoding='utf-8') as file:
            for line in file:
                clean_line = line.strip()
                if not clean_line:
                    continue
                if clean_line[0] == '#':
                    continue
                self.write(clean_line)
                added_count += 1
        if added_count == 0:
            raise ValueError

    def find_note(self, fragment):
        if not fragment:
            raise ValueError
        if not isinstance(fragment, str):
            raise TypeError
        for note in self.notes:
            if fragment in note.text:
                return note
        else:
            raise ValueError

    def preview(self):
        return [f'{i}. {note.text}' for i, note in enumerate(self.notes, start=1)]

    def dump(self, path):
        with open(path, "w", encoding="utf-8") as file:
            for note in self.notes:
                new_note = note.text + '\n'
                file.write(new_note)

    def seal(self):
        if not self.is_open:
            raise ValueError
        self.is_open = False

    def __str__(self):
        if self.is_open:
            status = 'open'
        else:
            status = 'sealed'
        return f'{self.__class__.__name__}({self.title}): {len(self.witnesses)} witnesses, {len(self.notes)} notes, {status}'


def capsules_of(person, capsules):
    results = []
    for capsule in capsules:
        if person in capsule.witnesses:
            results.append(capsule.title)
    return results






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

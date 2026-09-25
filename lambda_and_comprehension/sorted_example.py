participant_list = [
    ('Alison', 50, 18),
    ('Terence', 75, 22),
    ('David', 75, 20),
    ('Jimmy', 90, 22),
    ('John', 45, 22)
]


def sorter(item):
    error = 100 - item[1]
    age = item[2]
    return (error, age)


sorted_list = sorted(participant_list, key=sorter)
print(sorted_list)
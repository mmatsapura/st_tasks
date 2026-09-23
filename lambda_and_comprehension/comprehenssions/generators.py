# gen = (x**2 for x in range(5))
# print(next(gen))
# print(next(gen))
# print(next(gen))
# #-----------------------------------------
#
# gen = (x for x in range(10) if x % 2 == 0)
# for _ in range(3):
#     print(next(gen))
#
# #-----------------------------------------
# def square(x):
#     return x*x
#
# gen = (square(x) for x in range(5))
# print(next(gen))  # 0
# print(next(gen))  # 1
#
#
# # tuple comprehension
# result = tuple(x for x in range(5))
# print(result)
# #-----------------------------------------
# def count_up_to(n):
#     i = 1
#     while i <= n:
#         yield i
#         i += 1
#
# gen = count_up_to(5)
# print(next(gen))
# print(next(gen))




# real example

def read_logs(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if "ERROR" in line:
                yield line.strip()

error_logs = read_logs("server.log")

for log in error_logs:
    print(log)

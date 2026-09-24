# Find negative numbers and replace them with zero
nums = [3, -1, 0, 7, -5, -10, 12]

results = list(map(lambda number: number if number > 0 else 0, nums))
print(results)
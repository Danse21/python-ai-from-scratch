def sum_list(numbers):
  total = 0
  for number in numbers:
    total += number
  return total
result = sum_list([1, 2, 3, 4])
print(result)
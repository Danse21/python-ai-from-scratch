    #Original code
# def has_duplicate(numbers):
#     for i in range(len(numbers)):
#         for j in range(len(numbers)):
#             if i != j and numbers[i] == numbers[j]:
#                 return True
#     return False

# Optimized to O(n)
def has_duplicate(numbers):
  seen_numbers = set()
  for number in numbers:
    if number in seen_numbers:
      return number
    else:
      seen_numbers.add(number)
  return False

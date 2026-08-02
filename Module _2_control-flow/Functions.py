# Ett återanvändbart kodblock
def is_even(number):
  return number % 2 == 0
result = is_even(3)
print(result)

# Complexity = O(1) (constant number of operations): This is because the function takes only one items (element) and checks if it's 
# an even number. That will always perform the same number of operations no matter how big or small the element is
# as what matters is the number of operations to be performed, which will always be the same. 
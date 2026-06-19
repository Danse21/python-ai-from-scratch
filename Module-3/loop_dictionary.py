#
prices = {"bread": 25, "milk": 15, "egg": 40, "butter": 55}
total = 0
for key, value in prices.items():
  print(f"{key}: {value}")
  total += value
print(total)



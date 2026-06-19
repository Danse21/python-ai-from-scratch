age = input("What is your age? ")
try:
  print(int(age))
except ValueError:
  print("Det är inte ett glitigt tal!")
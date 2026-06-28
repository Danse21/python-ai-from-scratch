# Skriv dina tre favoritmaträtter (från Modul 3) 
# till en fil my_foods.txt, en per rad. 
# Läs sedan filen och skriv ut varje rad utan \n.

my_foods = ["Rice", "Pizza", "Soup", "Potato"]
with open("my_foods.txt", "w") as f:
  for food in my_foods:
    f.write(food + "\n")

with open("my_foods.txt", "r") as f:
  reader = f.read()
  print(reader.strip())
  
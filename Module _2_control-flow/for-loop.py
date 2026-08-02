# Loopa igenom siffrorna 1 - 10 med range() och skriv ut bara de jämna talen.
for i in range(1, 11):
  if i%2 == 0 and i>0:
    print(i)
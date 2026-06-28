import csv
try:
  with open("does_not_exist.csv", "r") as f:
    print(f.read())
except FileNotFoundError:
  print("Filen finnades inte!")

with open("students.csv", "r") as f:
  reader = csv.reader(f)
  skipped = next(reader)
  counter = 0
  total = 0
  for row in reader:
    score = row[1]
    counter += 1
    total += int(score)
  print("Total score: ", total)
  print("Count: ", counter)
  avg_score = total / counter
  print(avg_score)
import csv
with open("students.csv", "w", newline="") as f:
  student_list = csv.writer(f)
  student_list.writerow(["name", "score"])
  student_list.writerow(["Anna", 85])
  student_list.writerow(["Bo", 62])
  student_list.writerow(["Cleo", 91])
  student_list.writerow(["Dan", 45])

with open("students.csv", "r") as f:
  text_score = f.read()
  print(text_score)
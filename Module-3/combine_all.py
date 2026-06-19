#
students = [
  {"name": "Anna", "score": 85},
  {"name": "Bo", "score": 62},
  {"name": "Cleo", "score": 91},
  {"name": "Dan", "score": 45}
]
def passing_students(students):
  threshold = 60
  passing_names = []
  for i in students:
    if i["score"] >= threshold:
      passing_names.append(i["name"])
  return passing_names
students_list = passing_students(students)
print(students_list)

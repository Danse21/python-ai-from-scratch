# Create a dictionary of items of about_myself in a key: value fprmat
# Display all content of the dictionary using an f-string

about_myself = {
  "name": "Damasus",
  "age": 35,
  "city": "Gothenburg",
  "hobby": "cooking"
}
print(f"{about_myself['name']}, {about_myself['age']} years, lives in {about_myself['city']}, likes {about_myself['hobby']}.")

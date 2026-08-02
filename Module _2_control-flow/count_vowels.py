# Pseudocode
# Define a function that accepts a text
# write a for-loop that will go through the text and store each character in a variable called letter
# make a list of vowels and assign it to a variable called vowels
# check if items in the list of vowels exit in the letter
# return vowels
def count_vowels(text):
  counter = 0
  vowels = ["a", "e", "i", "o", "u"]
  for letter in text:
    if letter in vowels:
      counter += 1
  return counter
result = count_vowels("Damasus")
print(result)
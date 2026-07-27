# pseudocode first, plain language, before any Python. Sketch the steps for: 
# loop 1 to 20, check divisibility by 3 and/or 5, print accordingly.
# Pseudocode
# Write a for loop that goes through the numbers ranging from 1 to 21.
# write an if statement that checks if a number gives 0 when divided by both 3 and 5, for each number divisible both 3 and 5, print "FizzBuzz"
# write an elif statement that checks if a number gives 0 when divided by 3, for each number divisible by 3, print "Fizz"
# write an elif statement that checks if a number gives 0 when divided by 5, for each number divisible by 5, print "Buzz"
# write an else statement for number that did not return 0 when divided by both 3 and 5.


for i in range(1, 21):
  if i % 3 == 0 and i % 5 == 0:
    print("FizzBuzz")
  elif i % 3 == 0:
    print("Fizz")
  elif i % 5 == 0:
    print("Buzz")
  else:
    print(i)
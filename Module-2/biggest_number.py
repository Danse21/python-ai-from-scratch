# Pseudocode
# Define a function, find_max(numbers)
# assign or initiate a variable named, biggest_so_far, to number on the first index in the "numbers"
# write a for-loop the goes through the "numbers" and store it "number" variable
# check if each of the "number" is greater than value of biggest_so_far
# Reassign biggest_so_far to the "number"
# Move out of the loo and return biggest_so_far
# Assign the function call to a variable "result", while adding a list of numbers
# Print the function call variable 

def find_max(numbers):
  biggest_so_far = numbers[0]
  for number in numbers:
    if number > biggest_so_far:
      biggest_so_far = number
  return biggest_so_far
result = find_max([50, 24, 72, 99])
print(result)

# Complexity = O(n) (linear time): This is because the time it takes to run the code increases
# as the number of iimes (n elements) to loop through increases.
# Pseudocode
# write a for-loop that goes over a range of numbers (1 - 5) - row 
# inside the first loop, write another for-loop that goes through a range of number (1 - 5) -collumn
# 

for i in range(1, 6):
  for j in range(1, 6):
    total = i * j
    print(f"{i} * {j} = {total}")

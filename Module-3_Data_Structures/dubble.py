#
numbers = [1, 3, 5, 3, 2, 1, 5, 7, 2]
remove_duplicates = set(numbers)
convert_to_list = list(sorted(remove_duplicates))
print(convert_to_list)
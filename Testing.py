# file_paths = list(filedialog.askopenfilenames(title="Select Signal Data Files"))
#
# print(file_paths)
#
# file_paths.pop(0)
#
# for file_path in file_paths:
#     print(file_path)
#     with open(file_path, 'r') as file:
#         for line in file:
#             print(line)
#     print("= " * 30)


original_array = [1, 2, 3, 4, 5]
new_array = [sum(original_array[:i+1]) for i in range(len(original_array))]
print(new_array)

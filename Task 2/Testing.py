import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import numpy as np
from comparesignals import SignalSamplesAreEqual
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter


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


# Your original array of 5 values
original_array = [1, 2, 3, 4, 5]

# Define the desired length of the extended array
desired_length = 5

# Create a new array with the desired length filled with 0s
extended_array = original_array + [0] * (desired_length - len(original_array))

# Print the extended array
print(extended_array)

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

file_path = "signal1.txt"
x = []
y = []

with open(file_path, 'r') as file:
    line_count = 0
    for line in file:
        line_count += 1
        if line_count <= 3:
            continue
        values = line.split()  # Assuming the values are separated by whitespace
        x.append(float(values[0]))  # Assuming x values are in the first column
        y.append(float(values[1]))  # Assuming y values are in the second column

# Plot the frequency domain
plt.stem(x, y)
plt.plot(x, y)
plt.xlabel('X')
plt.ylabel('Amplitude')
plt.title('Time Domain Plot')
plt.show()

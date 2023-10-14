import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

file_path = "signal1.txt"
x = []
y = []
z = []
domain = 0

with open(file_path, 'r') as file:
    line_count = 0
    domain = 0
    for line in file:
        line_count += 1
        if line_count == 1:
            # [0] Time Domain (x= time_in_secs, y= Amplitude)
            # [1] Freq Domain (x= bin_num, y= Amplitude, z= phase_shift)
            if line == 1:
                domain = 1
            continue
        elif line_count == 2:
            # [0] Aperiodic
            # [1] Periodic
            continue
        elif line_count == 3:
            # N samples (pointless)
            continue
        values = line.split()       # Separate by whitespace
        x.append(float(values[0]))  # [T] Sample Index      [F] Frequency
        y.append(float(values[1]))  # [T] Sample Amplitude  [F] Amplitude
        if domain == 1:
            y.append(float(values[1]))  # [T] Shift = 0     [F] Phase Shift


# Plot the frequency domain with different colors
plt.stem(x, y)
# plt.plot(x, y, color='green')
plt.xlabel('X')
plt.ylabel('Amplitude')
plt.title('Time Domain Plot')
plt.show()

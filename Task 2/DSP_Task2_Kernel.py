import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

# file_path = "signal1_T_AP_13.txt"
# x = []
# y = []
# z = []
# domain = 0
# signal_details = []
# x_label = 'f'
#
# with open(file_path, 'r') as file:
#     line_count = 0
#     for line in file:
#         line_count += 1
#         if line_count <= 3:
#             # [0] Domain
#             # if == 0 -> Time Domain (x= time_in_secs, y= Amplitude)
#             # if == 1 -> Freq Domain (x= bin_num, y= Amplitude, z= phase_shift)
#             # [1] Period
#             # if == 0 -> Aperiodic
#             # if == 1 -> Periodic
#             # [2] N samples
#             signal_details.append(int(line))
#             continue
#         values = line.split()  # Separate by whitespace
#         x.append(float(values[0]))  # [T] Sample Index      [F] Frequency
#         y.append(float(values[1]))  # [T] Sample Amplitude  [F] Amplitude
#         if signal_details[0] == 1:  # [2] Domain
#             x_label = 't'
#             z.append(float(values[2]))  # [T] Shift = 0         [F] Phase Shift
#     if signal_details[1] == 1:  # [1] Period
#         start_of_cycle = 0
#         end_of_cycle = signal_details[2] + 1
#         temp_y = y
#         for i in range(1, 3):
#             start_of_cycle += signal_details[2] + 1
#             end_of_cycle += signal_details[2] + 1
#             x.extend(range(start_of_cycle, end_of_cycle))
#             y = y + temp_y
#
# # Plot the frequency domain with different colors
# plt.stem(x, y)
# # plt.plot(x, y, color='green')
# plt.xlabel(x_label)
# plt.ylabel('Amplitude')
# plt.title('Time Domain Plot')
# plt.show()





# Read the contents of the first text file
with open('signal1.txt', 'r') as file1:
    lines = file1.readlines()
    signal1_time = []
    signal1_value = []
    for line in lines:
        parts = line.split()
        signal1_time.append(float(parts[0]))
        signal1_value.append(float(parts[1]))


    Square = np.array(signal1_value) * np.array(signal1_value)
    print(Square)
    plt.stem(signal1_time, Square)
    plt.xlabel("signal_time")
    plt.ylabel('Amplitude')
    plt.title('ِِSquaring')
    plt.show()







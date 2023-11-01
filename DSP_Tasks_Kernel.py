import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler

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


# # Read the contents of the first text file
# with open('Task 2/signal1.txt', 'r') as file1:
#     lines = file1.readlines()
#     signal1_time = []
#     signal1_value = []
#     for line in lines:
#         parts = line.split()
#         signal1_time.append(float(parts[0]))
#         signal1_value.append(float(parts[1]))
#
# # Read the contents of the second text file
# with open('Task 2/signal2.txt', 'r') as file2:
#     lines = file2.readlines()
#     signal2_time = []
#     signal2_value = []
#     for line in lines:
#         parts = line.split()
#         signal2_time.append(float(parts[0]))
#         signal2_value.append(float(parts[1]))
#
# # Check the sizes of the signals
# signal1_size = len(signal1_value)
# signal2_size = len(signal2_value)
#
# # Check if the sizes match
# if signal1_size != signal2_size:
#     print("Error: The signals have different sizes.")
# else:
#     result_value = np.array(signal1_value) + np.array(signal2_value)
#     print(type(result_value))
#     plt.stem(signal2_time, result_value)
#     # plt.plot(x, y, color='green')
#     plt.xlabel("signal2_time")
#     plt.ylabel('Amplitude')
#     plt.title('ِِAdding')
#     plt.show()

# Normalization
# def normalization():
#
#     with open('Task 2/signal1.txt', 'r') as file1:
#         lines = file1.readlines()
#         signal1_time = []
#         signal1_value = []
#         for line in lines:
#             parts = line.split()
#             signal1_time.append(float(parts[0]))
#             signal1_value.append(float(parts[1]))
#
#
#     signal1_value = np.reshape(signal1_value, (-1, 1))
#     scaler_value = int(input("1- press one for (0:1)\n2- for (-1:1)\n"))
#     scaler = MinMaxScaler(feature_range=(0,1))
#     if scaler_value == 1:
#         scaler = MinMaxScaler(feature_range=(0,1))
#     else:
#         scaler = MinMaxScaler(feature_range=(-1,1))
#
#     normalized_signal = scaler.fit_transform(np.array(signal1_value))
#     normalized_result = normalized_signal.flatten()
#     print(normalized_result)
#     plt.stem(signal1_time, normalized_result)
#     # plt.plot(x, y, color='green')
#     plt.xlabel("signal1_time")
#     plt.ylabel('Amplitude')
#     plt.title('ِِAdding')
#     plt.show()
#
#
# normalization()

import cmath
import math


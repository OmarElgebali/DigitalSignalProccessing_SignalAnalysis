# # file_paths = list(filedialog.askopenfilenames(title="Select Signal Data Files"))
# #
# # print(file_paths)
# #
# # file_paths.pop(0)
# #
# # for file_path in file_paths:
# #     print(file_path)
# #     with open(file_path, 'r') as file:
# #         for line in file:
# #             print(line)
# #     print("= " * 30)
# import cmath
# import math
# # #
# # c = -2 + 2j
# # print(c)
# # print(type(c))
# # print(cmath.phase(c))
# # print(math.degrees(cmath.phase(c)))
#
#
# """
# import cmath
# import math
#
# # c = (real) + (img)j           -> complex (real, imaginary)
# # c.conjugate()                 -> (3 + 3j) : (3 - 3j)
# # abs(c)                        -> Amplitude
# # cmath.phase()                 -> Phase Shift in Radian
# # math.degrees(cmath.phase())   -> Phase Shift in Degree
# """
#
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Step 1: Discretize the Signal (Example signal)
# signal = [7, 15, 26, 88]
#
# # Step 2: Compute the Discrete Fourier Transform (DFT)
# dft_result = np.fft.fft(signal)
#
# print(dft_result)
# # Step 3: Compute Magnitude and Phase (Optional)
# magnitude = np.abs(dft_result)
# phase = np.angle(dft_result)
# print(magnitude)
# phase_d = [math.degrees(cmath.phase(c)) for c in dft_result]
# print(phase)
# print(phase_d)
#
# # Step 4: Plot the Frequency Spectrum
# plt.figure(figsize=(8, 6))
# plt.subplot(2, 1, 1)
# plt.stem(magnitude)
# plt.title('Magnitude Spectrum')
# plt.xlabel('Frequency Index')
# plt.ylabel('Magnitude')
#
# plt.subplot(2, 1, 2)
# plt.stem(phase_d)
# plt.title('Phase Spectrum')
# plt.xlabel('Frequency Index')
# plt.ylabel('Phase (radians)')
#
# plt.tight_layout()
# plt.show()
import math

import numpy as np
from matplotlib import pyplot as plt

# import math
# print(math.radians(45))


# arr = [10.4628, 7.324, 7.8834, 11.3679, 12.962, 10.4628, 7.324, 7.8834, 11.3679,  12.962, 11.3679, 12.962, 10.4628, 7.324, 7.8834, 12.962]
# avg = sum(arr) / len(arr)
# print(sum(arr))
# print(len(arr))
# print(avg)
# new_arr = [val - avg for val in arr]
# print(new_arr)
# new_arr = [round(val, 3) for val in new_arr]
# print(new_arr)


# time = [1, 2, 3, 4, 5]
# values = [10, 20, 30, 40, 50]
#
# # Reverse the signal
#
# # Shift the reversed signal to align with the original signal
# folded = [(-1*x) for x in time]
# # Print the original and folded signals
# print("Original Signal (Time, Values):", list(zip(time, values)))
# print("Folded Signal (Time, Values):", list(zip(folded, values)))
from TaskFunctions import Task_8_CompareSignal


def sort_2_lists(list_1, list_2):
    combined_lists = list(zip(list_1, list_2))
    combined_lists.sort(key=lambda l: l[0])
    x, y = zip(*combined_lists)
    x = list(x)
    y = list(y)
    return x, y


def read_signal_periodicity(signal_file_path):
    with open(signal_file_path, 'r') as file:
        file.readline()
        periodicity = int(float(file.readline()))
        file.readline()
        lines = file.readlines()
        signal_time = []
        signal_value = []
        for line in lines:
            parts = line.split()
            signal_time.append(float(parts[0]))
            signal_value.append(float(parts[1]))
    return signal_time, signal_value, periodicity


def read_only_signal(signal_file_path):
    with open(signal_file_path, 'r') as file:
        file.readline()
        file.readline()
        file.readline()
        lines = file.readlines()
        signal_time = []
        signal_value = []
        for line in lines:
            parts = line.split()
            signal_time.append(float(parts[0]))
            signal_value.append(float(parts[1]))
    return signal_time, signal_value


def direct_correlation_2_signals(signal_value_1, signal_value_2, periodicity):
    def shift_left_signal(signal_v, is_periodic):
        prev_first_element = signal_v.pop(0)
        signal_v.append(prev_first_element if is_periodic else 0)
        return signal_v

    summation_square_of_list = lambda signal: sum([x1 * x1 for x1 in signal])
    calc_normalization_term = lambda signal_1, signal_2, length: math.sqrt(
        summation_square_of_list(signal_1) * summation_square_of_list(signal_2)) / length

    N = len(signal_value_1)
    print("=" * 200)
    print(f"Length (N)                  : {N}")
    normalization_term = calc_normalization_term(signal_value_1, signal_value_2, N)
    print(f"Normalization Term          : {normalization_term}")
    normalized_correlated_signal = []
    for i in range(N):
        r_12 = np.sum([a * b for a, b in zip(signal_value_1, signal_value_2)]) / N
        if periodicity:
            norm_12 = normalization_term
        else:
            norm_12 = calc_normalization_term(signal_value_1, signal_value_2, N)
        normalized_correlated_signal.append(r_12 / norm_12)
        signal_value_2 = shift_left_signal(signal_value_2, periodicity)
    print(f"Normalized Correlated Signal: {normalized_correlated_signal}")
    return normalized_correlated_signal


def task_8_correlation_fast():
    signal_file_path_1 = "Task 8/Correlation/Corr_input signal1.txt"
    signal_file_path_2 = "Task 8/Correlation/Corr_input signal2.txt"
    output_file_path = "Task 8/Correlation/CorrOutput.txt"

    signal_time_1, signal_value_1, signal_periodicity_1 = read_signal_periodicity(signal_file_path_1)
    signal_time_1, signal_value_1 = sort_2_lists(signal_time_1, signal_value_1)

    signal_time_2, signal_value_2, signal_periodicity_2 = read_signal_periodicity(signal_file_path_2)
    signal_time_2, signal_value_2 = sort_2_lists(signal_time_2, signal_value_2)

    normalized_correlated_signal = direct_correlation_2_signals(signal_value_1, signal_value_2, signal_periodicity_2)

    Task_8_CompareSignal.Compare_Signals(output_file_path, signal_time_1, normalized_correlated_signal)

    plt.plot(signal_time_1, signal_value_1, color='green', label='Signal 1')
    plt.plot(signal_time_2, signal_value_2, color='orange', label='Signal 2')
    plt.plot(signal_time_1, normalized_correlated_signal, color='red', label='Correlated Signal')
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel('Amplitude')
    plt.title('Task 8.1 - Correlation Signal')
    plt.show()


task_8_correlation_fast()
# s1 = [2, 1, 0, 0, 3]
# s2 = [3, 2, 1, 1, 5]
# fast_correlation_2_signals(s1, s2, 1)

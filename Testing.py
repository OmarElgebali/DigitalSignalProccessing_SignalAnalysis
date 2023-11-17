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

print(math.radians(45))

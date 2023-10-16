import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

def sort_2_lists(list_1, list_2):
    combined_lists = list(zip(list_1, list_2))
    combined_lists.sort(key=lambda l: l[0])
    x, y = zip(*combined_lists)
    x = list(x)
    y = list(y)
    return x, y

def shift():
    with open('signal1.txt', 'r') as file1:
        lines = file1.readlines()
        signal_time = []
        signal_value = []
        for line in lines:
            parts = line.split()
            signal_time.append(float(parts[0]))
            signal_value.append(float(parts[1]))

    shift_value = float(input("enter shift value : \n"))
    shifted_signal = np.array(signal_time) + shift_value
    shifted_signal , signal_value = sort_2_lists(shifted_signal,signal_value)
    plt.plot(shifted_signal, signal_value)
    plt.stem(shifted_signal,signal_value)
    plt.xlabel("Shifted Time")
    plt.ylabel('Amplitude')
    plt.title('ِِShift')
    plt.show()

shift()





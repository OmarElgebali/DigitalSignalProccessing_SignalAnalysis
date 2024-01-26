# Libraries
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk
import numpy as np
import math
import cmath
import os
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import log2

# Tasks Imports
from TaskFunctions import Task_9_ConvTest, Task_6_Shift_Fold_Signal, Task_5_comparesignal2, Task_7_ConvTest, \
    Task_6_DerivativeSignal, Task_8_CompareSignal, Task_9_CompareSignal, Task_4_signalcompare
from TaskFunctions.Task_1_comparesignals import SignalSamplesAreEqual
from TaskFunctions.Task_3_QuanTest1 import QuantizationTest1
from TaskFunctions.Task_3_QuanTest2 import QuantizationTest2
from TaskFunctions.Task_4_signalcompare import SignalCompare

import HelperResources
from FourierTransform import dft, idft, fourier_transform
from Correlation import direct_correlation_2_signals, fast_correlation_2_signals


TestCases = True


class GUI:
    def __init__(self):

        self.root = tk.Tk()

        self.Ys_cos_sample = None
        self.Ys_cos_analog = None
        self.Ys_sin_sample = None
        self.Ys_sin_analog = None
        self.Xs_SinCos = None
        self.Xs_ContDisc = []
        self.Ys_ContDisc = []

        self.root.title("DSP Tasks - CS6")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        self.menubar = tk.Menu(self.root)
        self.task_1_menu = tk.Menu(self.menubar, tearoff=0)
        self.task_1_menu.add_separator()
        self.task_1_menu.add_command(label="(1.1) Generate Cont. & Disc. Signals", command=self.task_1_1)
        self.task_1_menu.add_separator()
        self.task_1_menu.add_command(label="(1.1-TEST) Generate Cont. & Disc. Signals", command=self.task_1_1_TEST)
        self.task_1_menu.add_separator()
        self.task_1_menu.add_command(label="(1.2) Generate Sin/Cos Signal", command=self.task_1_2)
        self.task_1_menu.add_separator()
        self.task_1_menu.add_command(label="(1.2-TEST) Generate Sin/Cos Signal", command=self.task_1_2_TEST)
        self.menubar.add_cascade(menu=self.task_1_menu, label="Task 1")

        self.task_2_menu = tk.Menu(self.menubar, tearoff=1)
        self.task_2_menu.add_command(label="(2.1) Addition [∑ S's]", command=self.task_2_1_addition)
        self.task_2_menu.add_separator()
        self.task_2_menu.add_command(label="(2.2) Subtraction [S1 - S2]", command=self.task_2_2_subtraction)
        self.task_2_menu.add_separator()
        self.task_2_menu.add_command(label="(2.3) Multiplication [S * C]", command=self.task_2_3_multiplication)
        self.task_2_menu.add_separator()
        self.task_2_menu.add_command(label="(2.4) Squaring [S * S]", command=self.task_2_4_squaring)
        self.task_2_menu.add_separator()
        self.task_2_menu.add_command(label="(2.5) Shifting [Ø +- C]", command=self.task_2_5_shifting)
        self.task_2_menu.add_separator()
        self.task_2_menu.add_command(label="(2.6) Normalization [-1, 1 | 0, 1]", command=self.task_2_6_normalization)
        self.task_2_menu.add_separator()
        self.task_2_menu.add_command(label="(2.7) Accumulation [∑ x(k)] ", command=self.task_2_7_accumulation)
        self.menubar.add_cascade(menu=self.task_2_menu, label="Task 2")

        self.task_3_menu = tk.Menu(self.menubar, tearoff=2)
        self.task_3_menu.add_command(label="(3) Quantize Signal", command=self.task_3_quantize)
        self.menubar.add_cascade(menu=self.task_3_menu, label="Task 3")

        self.task_4_menu = tk.Menu(self.menubar, tearoff=2)
        self.task_4_menu.add_command(label="(4.1) Fourier Transform [DFT]", command=self.task_4_dft)
        self.task_4_menu.add_separator()
        self.task_4_menu.add_command(label="(4.2) Inverse Fourier Transform [IDFT]", command=self.task_4_idft)
        self.menubar.add_cascade(menu=self.task_4_menu, label="Task 4")

        self.task_5_menu = tk.Menu(self.menubar, tearoff=2)
        self.task_5_menu.add_command(label="(5.1) Compute DCT", command=self.task_5_dct)
        self.task_5_menu.add_separator()
        self.task_5_menu.add_command(label="(5.2.1) Remove DC using Average", command=self.task_5_remove_dc_using_avg)
        self.task_5_menu.add_command(label="(5.2.2) Remove DC using Harmonics",
                                     command=self.task_5_remove_dc_using_harmonics)
        self.menubar.add_cascade(menu=self.task_5_menu, label="Task 5")

        self.task_6_menu = tk.Menu(self.menubar, tearoff=2)
        self.task_6_menu.add_command(label="(6.1) Smoothing", command=self.task_6_smoothing)
        self.task_6_menu.add_separator()
        self.task_6_menu.add_command(label="(6.2) Sharpening", command=self.task_6_sharpening)
        self.task_6_menu.add_separator()
        self.task_6_menu.add_command(label="(6.3) Delaying / Advancing", command=self.task_6_delay_advance_signal)
        self.task_6_menu.add_separator()
        self.task_6_menu.add_command(label="(6.4) Folding", command=self.task_6_folding)
        self.task_6_menu.add_separator()
        self.task_6_menu.add_command(label="(6.5) Delaying / Advancing a Folded Signal",
                                     command=self.task_6_delay_advance_folded_signal)
        self.task_6_menu.add_separator()
        self.task_6_menu.add_command(label="(6.6) Remove DC in Frequency Domain",
                                     command=self.task_6_remove_dc_in_freqdomain)
        self.menubar.add_cascade(menu=self.task_6_menu, label="Task 6")

        self.task_7_menu = tk.Menu(self.menubar, tearoff=2)
        self.task_7_menu.add_command(label="(7) Convolution Signal [TD]", command=self.task_7_convolution_time_domain)
        self.menubar.add_cascade(menu=self.task_7_menu, label="Task 7")

        self.task_8_menu = tk.Menu(self.menubar, tearoff=2)
        self.task_8_menu.add_command(label="(8.1) Correlation [TD]", command=self.task_8_direct_correlation)
        self.task_8_menu.add_separator()
        self.task_8_menu.add_command(label="(8.2+) Time Analysis", command=self.task_8_time_analysis_BONUS)
        self.task_8_menu.add_separator()
        self.task_8_menu.add_command(label="(8.3+) Template Matching", command=self.task_8_template_matching_BONUS)
        self.menubar.add_cascade(menu=self.task_8_menu, label="Task 8")

        self.task_9_menu = tk.Menu(self.menubar, tearoff=2)
        self.task_9_menu.add_command(label="(9.1) Fast Convolution Signal [FD]",
                                     command=self.task_9_fast_convolution)
        self.task_9_menu.add_separator()
        self.task_9_menu.add_command(label="(9.2) Fast Convolution Signal [FD]",
                                     command=self.task_9_fast_correlation)
        self.menubar.add_cascade(menu=self.task_9_menu, label="Task 9")

        self.color_green_1 = '#092635'
        self.color_green_2 = '#1B4242'
        self.color_green_3 = '#5C8374'
        self.color_green_4 = '#9EC8B9'
        self.plots_bg_color = self.color_green_4

        # Customize menu appearance
        menu_bg_color = self.color_green_3  # Menu background color
        menu_fg_color = 'white'  # Menu foreground color
        menu_font = ('serif', 10, 'italic')

        self.menubar.config(bg=menu_bg_color)

        # Apply styles to menus
        menus = [self.task_1_menu, self.task_2_menu, self.task_3_menu,
                 self.task_4_menu, self.task_5_menu, self.task_6_menu,
                 self.task_7_menu, self.task_8_menu, self.task_9_menu]
        for menu in menus:
            menu.config(bg=menu_bg_color, fg=menu_fg_color, font=menu_font)

        self.root.config(menu=self.menubar, bg=self.plots_bg_color)

        self.plots_frame = tk.Frame(self.root)
        self.plots_frame.grid(row=0, column=0)

        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def task_1_1(self):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))
        fig.patch.set_facecolor(self.plots_bg_color)

        file_path = filedialog.askopenfilename(title="Select a Signal Data File")
        if not file_path:
            messagebox.showerror(title="Error", message="Signal Data File Not Found!")
            return

        x = []
        y = []
        signal_details = []
        x_label = 't'
        domain = 'Time'
        periodic = 'Aperiodic'

        with open(file_path, 'r') as file:
            line_count = 0
            for line in file:
                line_count += 1
                if line_count <= 3:
                    # [0] Domain
                    # if == 0 -> Time Domain (x= time_in_secs, y= Amplitude)
                    # if == 1 -> Freq Domain (x= bin_num, y= Amplitude, z= phase_shift)
                    # [1] Period
                    # if == 0 -> Aperiodic
                    # if == 1 -> Periodic
                    # [2] N samples
                    # [3] Phase Shift
                    signal_details.append(int(line))
                    continue
                elif signal_details[0] == 1 and (line_count - 3) == (signal_details[2] + 1):
                    signal_details.append(int(line))
                    continue
                values = line.split()  # Separate by whitespace
                x.append(float(values[0]))  # [T] Sample Index      [F] Frequency
                y.append(float(values[1]))  # [T] Sample Amplitude  [F] Amplitude

            x, y = HelperResources.sort_2_lists(x, y)

            if signal_details[1] == 1:  # [1] Period
                periodic = 'Periodic'
                start_of_cycle = 0
                end_of_cycle = signal_details[2]
                temp_y = y
                for i in range(1, 3):
                    start_of_cycle += signal_details[2]
                    end_of_cycle += signal_details[2]
                    x.extend(range(start_of_cycle, end_of_cycle))
                    y = y + temp_y

            if signal_details[0] == 1:  # [0] Frequency Domain
                x_label = 'f'
                domain = 'Frequency'

            title = f'{periodic} {domain} Domain with {signal_details[2]} Samples'
            if signal_details[0] == 1 and signal_details[3]:  # [3] Phase Shift
                title = f'{periodic} {domain} Domain with {signal_details[2]} Samples and {signal_details[3]} Phase Shift'
                plt.xlim(1, max(x) + abs(signal_details[3]))
                x = [value + signal_details[3] for value in x]

        self.Xs_ContDisc = x
        self.Ys_ContDisc = y

        plt.plot(self.Xs_ContDisc, self.Ys_ContDisc, color='orange')
        plt.scatter(self.Xs_ContDisc, self.Ys_ContDisc)
        plt.xlabel(x_label)
        plt.ylabel('Amplitude')
        plt.title(title)
        plt.grid(True)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def task_1_2(self):
        wave_type = simpledialog.askinteger("Wave Type", "Enter Type of Signal:\n1- Sin\n2- Cosine")
        amplitude = simpledialog.askfloat("Amplitude", "Enter Amplitude:")
        analog_frequency = simpledialog.askinteger("Analog Frequency", "Enter Analog Frequency:")
        sampling_frequency = simpledialog.askinteger("Sampling Frequency", "Enter Sampling Frequency:")
        phase_shift = simpledialog.askfloat("Phase Shift", "Enter Phase Shift:")

        # if not amplitude or not sampling_frequency or not phase_shift or not analog_frequency or not wave_type:
        #     messagebox.showerror(title="Error", message="One of the values is Null")
        #     return

        if wave_type != 1 and wave_type != 2:
            messagebox.showerror(title="Error", message="Wave Type is not either a Sin (1) or Cosine (2) signal type")
            return

        # if sampling_frequency < 2 * analog_frequency:
        #     messagebox.showerror(title="Error", message="Sampling Frequency MUST BE Greater Than 2*Analog Frequency")
        #     return

        if sampling_frequency == 0:
            x_values = np.linspace(0, 10, analog_frequency)
            self.Xs_SinCos = x_values
            self.Ys_sin_analog = amplitude * np.sin(2 * np.pi * analog_frequency * x_values + phase_shift)
            self.Ys_cos_analog = amplitude * np.cos(2 * np.pi * analog_frequency * x_values + phase_shift)
            if wave_type == 1:
                name = "Sin"
                y_axis = self.Ys_sin_analog
            else:
                name = "Cosine"
                y_axis = self.Ys_cos_analog
        else:
            x_values = np.linspace(0, 10, sampling_frequency)
            self.Xs_SinCos = x_values

            # num_cycles_sample = sampling_frequency/360
            # num_cycles_analog = analog_frequency/360

            # Equation -> y = amplitude * np.sin(2 * np.pi * x + phase_shift)
            self.Ys_sin_analog = amplitude * np.sin(2 * np.pi * analog_frequency * x_values + phase_shift)
            self.Ys_sin_sample = amplitude * np.sin(2 * np.pi * sampling_frequency * x_values + phase_shift)

            # Equation -> y = amplitude * np.cos(2 * np.pi * x + phase_shift)
            self.Ys_cos_analog = amplitude * np.cos(2 * np.pi * analog_frequency * x_values + phase_shift)
            self.Ys_cos_sample = amplitude * np.cos(2 * np.pi * sampling_frequency * x_values + phase_shift)

            # else :
            if wave_type == 1:
                name = "Sin"
                y_axis = self.Ys_sin_sample

            else:
                name = "Cosine"
                y_axis = self.Ys_cos_sample

        title = f"""{name} Wave Plot
        Form: Y = A * {name.lower()}( W * X + Theta ) 
        Equation: Y = ({amplitude}) * {name.lower()}( ({analog_frequency}) * X + ({phase_shift}) )
        Sampling Frequency: {sampling_frequency}
        Fs >= 2 * Fmax : ({sampling_frequency}) >= (2 * {analog_frequency})"""

        self.window_1_plots([self.Xs_SinCos],
                            [y_axis],
                            [f'{name} Wave Plot'],
                            'Time',
                            'Amplitude',
                            title)

    def task_1_1_TEST(self):
        file_path = filedialog.askopenfilename(title="Select a Signal Data File")
        if not file_path:
            messagebox.showerror(title="Error", message="Signal Data File Not Found!")
            return

        x = []
        y = []
        signal_details = []
        x_label = 't'
        domain = 'Time'
        periodic = 'Aperiodic'

        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))
        fig.patch.set_facecolor(self.plots_bg_color)

        with open(file_path, 'r') as file:
            line_count = 0
            for line in file:
                line_count += 1
                if line_count <= 3:
                    # [0] Domain
                    # if == 0 -> Time Domain (x= time_in_secs, y= Amplitude)
                    # if == 1 -> Freq Domain (x= bin_num, y= Amplitude, z= phase_shift)
                    # [1] Period
                    # if == 0 -> Aperiodic
                    # if == 1 -> Periodic
                    # [2] N samples
                    # [3] Phase Shift
                    signal_details.append(int(line))
                    continue
                elif signal_details[0] == 1 and (line_count - 3) == (signal_details[2] + 1):
                    signal_details.append(int(line))
                    continue
                values = line.split()  # Separate by whitespace
                x.append(float(values[0]))  # [T] Sample Index      [F] Frequency
                y.append(float(values[1]))  # [T] Sample Amplitude  [F] Amplitude

            x, y = self.sort_2_lists(x, y)

            if signal_details[1] == 1:  # [1] Period
                periodic = 'Periodic'
                start_of_cycle = 0
                end_of_cycle = signal_details[2]
                temp_y = y
                for i in range(1, 3):
                    start_of_cycle += signal_details[2]
                    end_of_cycle += signal_details[2]
                    x.extend(range(start_of_cycle, end_of_cycle))
                    y = y + temp_y

            if signal_details[0] == 1:  # [0] Frequency Domain
                x_label = 'f'
                domain = 'Frequency'

            title = f'{periodic} {domain} Domain with {signal_details[2]} Samples'
            if signal_details[0] == 1 and signal_details[3]:  # [3] Phase Shift
                title = f'{periodic} {domain} Domain with {signal_details[2]} Samples and {signal_details[3]} Phase Shift'
                plt.xlim(1, max(x) + abs(signal_details[3]))
                x = [value + signal_details[3] for value in x]

        self.Xs_ContDisc = x
        self.Ys_ContDisc = y
        plt.plot(self.Xs_ContDisc, self.Ys_ContDisc, color='orange')
        plt.scatter(self.Xs_ContDisc, self.Ys_ContDisc)
        plt.xlabel(x_label)
        plt.ylabel('Amplitude')
        plt.title(title)
        plt.grid(True)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def task_1_2_TEST(self):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))
        fig.patch.set_facecolor(self.plots_bg_color)

        output_path = "Task 1/CosOutput.txt"
        name = "Cosine"
        wave_type = 2
        amplitude = 3
        analog_frequency = 200
        sampling_frequency = 500
        phase_shift = 2.35619449019235
        if messagebox.askyesno(title="Test Signal", message="Yes -> Sine Test\nNo  -> Cosine Test"):
            output_path = "Task 1/SinOutput.txt"
            name = "Sin"
            wave_type = 1
            analog_frequency = 360
            sampling_frequency = 720
            phase_shift = 1.96349540849362

        x_values = np.arange(0, 1, 1 / sampling_frequency)
        self.Xs_SinCos = x_values

        # Equation -> y = amplitude * np.sin(2 * np.pi * x + phase_shift)
        self.Ys_sin_analog = amplitude * np.sin(2 * np.pi * analog_frequency * x_values + phase_shift)
        self.Ys_sin_sample = amplitude * np.sin(2 * np.pi * sampling_frequency * x_values + phase_shift)

        # Equation -> y = amplitude * np.cos(2 * np.pi * x + phase_shift)
        self.Ys_cos_analog = amplitude * np.cos(2 * np.pi * analog_frequency * x_values + phase_shift)
        self.Ys_cos_sample = amplitude * np.cos(2 * np.pi * sampling_frequency * x_values + phase_shift)

        if wave_type == 1:
            plt.plot(self.Xs_SinCos, self.Ys_sin_sample, color='orange')
            plt.scatter(self.Xs_SinCos, self.Ys_sin_sample)
            SignalSamplesAreEqual(output_path, sampling_frequency, self.Ys_sin_analog)
        else:
            plt.plot(self.Xs_SinCos, self.Ys_cos_sample, color='orange')
            plt.scatter(self.Xs_SinCos, self.Ys_cos_sample)
            SignalSamplesAreEqual(output_path, sampling_frequency, self.Ys_cos_analog)

        title = f"""{name} Wave Plot
        Form: Y = A * {name.lower()}( W * X + Theta ) 
        Equation: Y = ({amplitude}) * {name.lower()}( ({analog_frequency}) * X + ({phase_shift}) )
        Sampling Frequency: {sampling_frequency}
        Fs >= 2 * Fmax : ({sampling_frequency}) >= (2 * {analog_frequency})"""

        plt.title(title)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.grid(True)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def task_2_1_addition(self):
        if TestCases:
            output_path = "Task 2/output_signals/signal1+signal3.txt"
            signal_2_file_path = "Task 2/input_signals/signal3.txt"
            if messagebox.askyesno(title="Test Signal", message="Yes -> Signal 2 (S1 + S2)\nNo  -> Signal 3 (S1 + S3)"):
                output_path = "Task 2/output_signals/Signal1+signal2.txt"
                signal_2_file_path = "Task 2/input_signals/Signal2.txt"

            signal_1_file_path = "Task 2/input_signals/Signal1.txt"
            file_paths = [signal_1_file_path, signal_2_file_path]
        else:
            # Select Multiple Files
            """
            file_paths = [filedialog.askopenfilename(title="Select a Signal Data File")]
            if not file_paths[0]:
                messagebox.showwarning(title="Warning", message="Signal Data File Not Found!")
                return
    
            while messagebox.askyesno(title="File Upload", message="Select another file (Signal)?"):
                file_paths.append(filedialog.askopenfilename(title="Select a Signal Data File"))
            """
            file_paths = list(filedialog.askopenfilenames(title="Select Signal Data Files"))
            if not file_paths[0]:
                messagebox.showerror(title="Error", message="There is a Signal Data File Not Found!")
                return

        signal_number = 0
        lengths_equal = 1
        signal_times = []
        signal_values = []
        """
        signal_times & signal_values -> List Description
        [
            [], Signal #1
            [], Signal #2
            [], Signal #3
            .
            .
            .
            []  Signal #N
        ]
        """

        signal_time_temp, signal_value_temp = HelperResources.read_only_signal(file_paths[0])
        signal_times.append(signal_time_temp)
        signal_values.append(signal_value_temp)
        file_paths.pop(0)

        for file_path in file_paths:
            signal_number += 1
            signal_time_temp, signal_value_temp = HelperResources.read_only_signal(file_path)
            signal_times.append(signal_time_temp)
            signal_values.append(signal_value_temp)
            if len(signal_times[0]) != len(signal_times[signal_number]):
                lengths_equal = 0
            signal_times[signal_number], signal_values[signal_number] = HelperResources.sort_2_lists(
                signal_times[signal_number],
                signal_values[signal_number])

        # Not Equal Length Check
        """
        signal_lengths = [len(signal) for signal in signal_times]
        if len(set(signal_lengths)) != 1:
        """
        if not lengths_equal:
            """
            current_signal = 0
            while current_signal <= signal_number:
                signal_values[current_signal] = signal_values[current_signal] + [0] * (len(signal_values[max_signal_len_number]) - len(signal_values[current_signal]))
                signal_times[current_signal].extend(range(len(signal_times[current_signal]), len(signal_values[max_signal_len_number])))
                current_signal += 1
            """
            signal_times, signal_values = HelperResources.extend_signals(signal_times, signal_values)
            messagebox.showwarning(title="Warning", message="Signal Lengths are not Equal!")

        # Add Signals
        """
        result_addition_signal = np.array(signal_values[0])
        current_signal = 0
        while current_signal <= (signal_number-1):
            result_addition_signal = result_addition_signal + np.array(signal_values[current_signal + 1])
            current_signal += 1
        """
        result_addition_signal = np.sum(signal_values, axis=0)

        if TestCases:
            SignalSamplesAreEqual(output_path, None, result_addition_signal)

        self.window_1_plots([signal_times[0]],
                            [result_addition_signal],
                            ['Addition Signal'],
                            "Time",
                            'Amplitude',
                            'Task 2.1 - Addition Signal')

    def task_2_2_subtraction(self):
        if TestCases:
            output_path = "Task 2/output_signals/signal1-signal3.txt"
            signal_2_file_path = "Task 2/input_signals/signal3.txt"
            if messagebox.askyesno(title="Test Signal", message="Yes -> Signal 2 (S1 - S2)\nNo  -> Signal 3 (S1 - S3)"):
                output_path = "Task 2/output_signals/signal1-signal2.txt"
                signal_2_file_path = "Task 2/input_signals/Signal2.txt"

            signal_1_file_path = "Task 2/input_signals/Signal1.txt"
        else:
            signal_1_file_path = filedialog.askopenfilename(title="Select Signal Data File (S1)")
            if not signal_1_file_path:
                messagebox.showerror(title="Error", message="Signal Data File (S1) Not Found!")
                return

            signal_2_file_path = filedialog.askopenfilename(title="Select Signal Data File (S2)")
            if not signal_2_file_path:
                messagebox.showerror(title="Error", message="Signal Data File (S2) Not Found!")
                return

        signal_1_time, signal_1_value = HelperResources.read_only_signal(signal_1_file_path)
        signal_2_time, signal_2_value = HelperResources.read_only_signal(signal_2_file_path)

        signal_1_time, signal_1_value = HelperResources.sort_2_lists(signal_1_time, signal_1_value)
        signal_2_time, signal_2_value = HelperResources.sort_2_lists(signal_2_time, signal_2_value)

        # Not Equal Length Check
        if len(signal_1_time) < len(signal_2_time):
            signal_1_time, signal_1_value = HelperResources.extend_signal_calculation(signal_1_time, signal_1_value,
                                                                                      len(signal_2_value))
            messagebox.showwarning(title="Warning", message="Signal Lengths are not Equal!")
        elif len(signal_1_time) > len(signal_2_time):
            signal_2_time, signal_2_value = HelperResources.extend_signal_calculation(signal_2_time, signal_2_value,
                                                                                      len(signal_1_value))
            messagebox.showwarning(title="Warning", message="Signal Lengths are not Equal!")

        # Subtract Signals
        """
        signal_1_value = np.array(signal_1_value)
        signal_2_value = np.array(signal_2_value)
        result_subtraction_signal_ = signal_1_value - signal_2_value
        """
        result_subtraction_signal = np.subtract(signal_2_value, signal_1_value)

        if TestCases:
            SignalSamplesAreEqual(output_path, None, result_subtraction_signal)

        self.window_1_plots([signal_1_time],
                            [result_subtraction_signal],
                            ['Subtraction Signal'],
                            "Time",
                            'Amplitude',
                            'Task 2.2 - Subtraction Signal')

    def task_2_3_multiplication(self):
        if TestCases:
            output_path = "Task 2/output_signals/MultiplySignalByConstant-signal2 - by 10.txt"
            signal_file_path = "Task 2/input_signals/Signal2.txt"
            factor = 10
            if messagebox.askyesno(title="Test Signal",
                                   message="Yes -> Signal 1 (Factor = 5)\nNo  -> Signal 2 (Factor = 10)"):
                output_path = "Task 2/output_signals/MultiplySignalByConstant-Signal1 - by 5.txt"
                signal_file_path = "Task 2/input_signals/Signal1.txt"
                factor = 5

        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File (S1)")
            if not signal_file_path:
                messagebox.showwarning(title="Warning", message="Signal Data File (S1) Not Found!")
                return

            factor = simpledialog.askinteger("Factor", "Enter Factor:")

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)

        signal_value_multiplied = np.array(signal_value) * np.array(factor)
        signal_time, signal_value_multiplied = HelperResources.sort_2_lists(signal_time, signal_value_multiplied)

        if TestCases:
            SignalSamplesAreEqual(output_path, None, signal_value_multiplied)

        self.window_1_plots([signal_time],
                            [signal_value_multiplied],
                            ['Multiplication Signal'],
                            "Time",
                            'Amplitude',
                            f'Task 2.3 - Multiplication Signal by Factor = {factor}')

    def task_2_4_squaring(self):
        if TestCases:
            signal_file_path = "Task 2/input_signals/Signal1.txt"
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        square_signal = np.array(signal_value) * np.array(signal_value)

        if TestCases:
            SignalSamplesAreEqual("Task 2/output_signals/Output squaring signal 1.txt", None, square_signal)

        self.window_1_plots([signal_time],
                            [square_signal],
                            ['Squared Signal'],
                            "Time",
                            'Amplitude',
                            'Task 2.4 - Squared Signal')

    def task_2_5_shifting(self):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))
        fig.patch.set_facecolor(self.plots_bg_color)

        if TestCases:
            signal_file_path = "Task 2/input_signals/Input Shifting.txt"
            shift_value = -500
            output_path = "Task 2/output_signals/output shifting by minus 500.txt"
            if messagebox.askyesno(title="Shifting Value", message="Yes -> +500\nNo  -> -500"):
                shift_value = 500
                output_path = "Task 2/output_signals/output shifting by add 500.txt"
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return
            shift_value = simpledialog.askfloat("Shifting Value", "Enter Shift Value (+ve or -ve):")

        signal_time, signal_value = (HelperResources.read_only_signal(signal_file_path))
        old_min_time = min(signal_time)
        old_max_time = max(signal_time)
        shifted_signal = np.array(signal_time) + shift_value
        shifted_signal, signal_value = HelperResources.sort_2_lists(shifted_signal, signal_value)
        new_min_time = min(shifted_signal)
        new_max_time = max(shifted_signal)
        if TestCases:
            SignalSamplesAreEqual(output_path, None, signal_value)

        plt.xlim(min(old_min_time, new_min_time) - 1, max(old_max_time, new_max_time) + 1)
        # plt.plot(shifted_signal, signal_value, color='orange')
        plt.scatter(shifted_signal, signal_value)
        plt.xlabel("Shifted Time")
        plt.ylabel('Amplitude')
        plt.title(f'Task 2.5 - Shifted Signal by ({shift_value})')
        plt.grid(True)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def task_2_6_normalization(self):
        if TestCases:
            signal_file_path = "Task 2/input_signals/Signal2.txt"
            output_path = "Task 2/output_signals/normlize signal 2 -- output.txt"
            scaler_value = 1
            if messagebox.askyesno(title="Test Signal", message="Yes -> Signal 1 (-1 , 1)\nNo  -> Signal 2 (0 , 1)"):
                output_path = "Task 2/output_signals/normalize of signal 1 -- output.txt"
                signal_file_path = "Task 2/input_signals/Signal1.txt"
                scaler_value = 2
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return
            scaler_value = simpledialog.askfloat("Normalizing Range", "Press Desired Range\n1. [0, 1]\n2. [-1, 1]")

            if scaler_value != 1 and scaler_value != 2:
                messagebox.showerror(title="Error",
                                     message="Normalizing Value is not either:\n[0, 1] -> (Number 1.) or\n [-1, 1] -> (Number 2.)")
                return

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)

        signal_value = np.reshape(signal_value, (-1, 1))
        scaler = MinMaxScaler(feature_range=(0, 1))
        if scaler_value == 2:
            scaler = MinMaxScaler(feature_range=(-1, 1))

        normalized_signal = scaler.fit_transform(np.array(signal_value))
        normalized_result = normalized_signal.flatten()

        if TestCases:
            SignalSamplesAreEqual(output_path, None, normalized_result)

        self.window_1_plots([signal_time],
                            [normalized_result],
                            ['Normalized Signal'],
                            "Time",
                            'Amplitude',
                            'Task 2.6 - Normalized Signal')

    def task_2_7_accumulation(self):
        if TestCases:
            signal_file_path = "Task 2/input_signals/Signal1.txt"
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        accumulate_signal = [sum(signal_value[:i + 1]) for i in range(len(signal_value))]

        if TestCases:
            SignalSamplesAreEqual("Task 2/output_signals/output accumulation for signal1.txt", None, accumulate_signal)

        self.window_1_plots([signal_time],
                            [accumulate_signal],
                            ['Accumulated Signal'],
                            "Time",
                            'Amplitude',
                            'Task 2.7 - Accumulated Signal')

    def task_3_quantize(self):
        if TestCases:
            signal_file_path = "Task 3/Test 2/Quan2_input.txt"
            bits = 2
            L = 4
            is_test_1 = messagebox.askyesno(title="Test Signal", message="Yes -> Signal 1\nNo  -> Signal 2")
            if is_test_1:
                signal_file_path = "Task 3/Test 1/Quan1_input.txt"
                bits = 3
                L = 8
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return
            if messagebox.askyesno(title="Levels or Bits used for Quantization",
                                   message="Yes -> # of Levels\nNo  -> # of Bits"):
                L = simpledialog.askinteger("Number of Levels", "Enter a +ve value:")
                if L < 0:
                    messagebox.showerror(title="Error", message="#ofLevels are -ve")
                    return
                bits = int(log2(L))
            else:
                bits = simpledialog.askinteger("Number of Bits", "Enter a +ve value:")
                if bits < 0:
                    messagebox.showerror(title="Error", message="#ofBits are -ve")
                    return
                L = pow(2, bits)

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        signal_time, signal_value = HelperResources.sort_2_lists(signal_time, signal_value)

        rounding_parameter = 3
        minimum = min(signal_value)
        maximum = max(signal_value)
        delta = round((maximum - minimum) * 1.00 / L, rounding_parameter)
        intervals = [(minimum, minimum + delta)]
        for i in range(L - 1):
            intervals.append((intervals[-1][1], intervals[-1][1] + delta))
        rounded_intervals = [(round(start, rounding_parameter), round(end, rounding_parameter)) for start, end in
                             intervals]

        mid_points = [(interval[0] + interval[1]) / 2.00 for interval in rounded_intervals]
        rounded_mid_points = [round(mid, rounding_parameter) for mid in mid_points]

        quantized_signal = []
        interval_index = []
        error_square = []
        errors = []

        for s_value in signal_value:
            for index, interval in enumerate(rounded_intervals):
                if interval[0] <= s_value <= interval[1]:
                    quantized_signal.append(rounded_mid_points[index])
                    interval_index.append(index + 1)
                    errors.append(round((quantized_signal[-1] - s_value), rounding_parameter))
                    error_square.append(round(((quantized_signal[-1] - s_value) ** 2), rounding_parameter))
                    break

        number_of_samples = len(signal_value)
        mse = (np.sum(error_square) * 1.00) / number_of_samples

        binary_values = [bin(index - 1)[2:] for index in interval_index]
        encoded_signal = []
        for bin_value in binary_values:
            if len(bin_value) < bits:
                bin_value = '0' * (bits - len(bin_value)) + bin_value
            encoded_signal.append(bin_value)

        popup = tk.Toplevel()
        popup.title("Quantization & Encoding Table")
        tree = ttk.Treeview(popup, columns=(
            "N", "Signal_Values", "Interval_Indices", "Quantized_Values", "Power_Errors", "Encoded_Signal"))
        tree.heading("#1", text="N")
        tree.heading("#2", text="Signal Values")
        tree.heading("#3", text="Interval Indices")
        tree.heading("#4", text="Quantized Values")
        tree.heading("#5", text="Power Errors")
        tree.heading("#6", text="Encoded Signal")

        for i in range(number_of_samples):
            tree.insert("", i, values=(
                i, signal_value[i], interval_index[i], quantized_signal[i], error_square[i],
                encoded_signal[i]))

        tree.pack()
        if TestCases:
            if is_test_1:
                output_path = "Task 3/Test 1/Quan1_Out.txt"
                QuantizationTest1(output_path, encoded_signal, quantized_signal)
            else:
                output_path = "Task 3/Test 2/Quan2_Out.txt"
                QuantizationTest2(output_path, interval_index, encoded_signal, quantized_signal, errors)

        self.window_2_plots([signal_time, signal_time],
                            [signal_value, quantized_signal],
                            ['Original Signal', 'Quantized Signal'],
                            "Time",
                            'Amplitude',
                            'Original Signal',
                            f'Task 3 - Quantized Signal with # of Levels = {L} & MSE = {mse}')

    def task_4_dft(self):
        if TestCases:
            signal_file_path = 'Task 4/DFT/input_Signal_DFT.txt'
            sampling_frequency = 4
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return
            sampling_frequency = simpledialog.askinteger("Sampling Frequency",
                                                         "Enter a +ve Sampling Frequency in (Hz):")
            if sampling_frequency < 0:
                messagebox.showerror(title="Error", message="Sampling Frequency must be non-negative")
                return

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        signal_time, signal_value = HelperResources.sort_2_lists(signal_time, signal_value)

        rounding_parameter = 3
        N = len(signal_value)

        harmonics = dft(signal_value)

        amplitudes = [abs(x_k_n) for x_k_n in harmonics]
        phase_shifts = [cmath.phase(x_k_n) for x_k_n in harmonics]
        print(f"Amplitudes         A: {amplitudes}")
        print(f"Phase Shifts       Ø: {phase_shifts}")
        print("=" * 200)

        if TestCases:
            output_file_path = 'Task 4/DFT/Output_Signal_DFT_A,Phase.txt'
            polar_form = HelperResources.read_polar_signal(output_file_path)
            output_amplitudes = []
            output_phase_shifts = []
            for a, ps in polar_form:
                output_amplitudes.append(a)
                output_phase_shifts.append(ps)
            Task_4_signalcompare.SignalCompare(amplitudes, output_amplitudes, phase_shifts, output_phase_shifts)

        fundamental_frequency = round((2 * math.pi * sampling_frequency) / N, rounding_parameter)
        print(f"Fundamental Frequency : {fundamental_frequency}")
        print("=" * 200)

        x_axis = [fundamental_frequency]
        for i in range(N - 1):
            x_axis.append(x_axis[-1] + fundamental_frequency)

        print(f"X-axis : {x_axis}")
        print("=" * 200)

        self.window_2_plots_freq_domain(x_axis, amplitudes, phase_shifts)

        popup = tk.Toplevel()
        popup.title("Modification of Frequency Domain Signal")
        modification_frame = tk.Frame(popup)
        modification_frame.columnconfigure(0, weight=1)
        modification_frame.columnconfigure(1, weight=1)
        lbl_freq_index = tk.Label(modification_frame, text="Frequency Index (0, N-1)", font=('Arial', 16))
        lbl_freq_index.grid(row=0, column=0, sticky=tk.W + tk.E)
        txt_freq_index = tk.Entry(modification_frame)
        txt_freq_index.grid(row=0, column=1, sticky=tk.W + tk.E)
        lbl_amplitude = tk.Label(modification_frame, text="Amplitude (A)", font=('Arial', 16))
        lbl_amplitude.grid(row=1, column=0, sticky=tk.W + tk.E)
        txt_amplitude = tk.Entry(modification_frame)
        txt_amplitude.grid(row=1, column=1, sticky=tk.W + tk.E)
        lbl_phase_shift = tk.Label(modification_frame, text="Phase Shift (Ø)", font=('Arial', 16))
        lbl_phase_shift.grid(row=2, column=0, sticky=tk.W + tk.E)
        txt_phase_shift = tk.Entry(modification_frame)
        txt_phase_shift.grid(row=2, column=1, sticky=tk.W + tk.E)

        def apply_modification():
            amplitudes[int(txt_freq_index.get())] = float(txt_amplitude.get())
            phase_shifts[int(txt_freq_index.get())] = float(txt_phase_shift.get())

            self.window_2_plots_freq_domain(x_axis, amplitudes, phase_shifts)

            messagebox.showinfo(title="Successful", message="Amplitude & Phase Shift Updated Successfully")

        btn_apply_mod = tk.Button(modification_frame, text="Apply Modifications", font=('Arial', 14),
                                  command=apply_modification)
        btn_apply_mod.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E)

        lbl_file_name = tk.Label(modification_frame, text="File Name", font=('Arial', 16))
        lbl_file_name.grid(row=4, column=0, sticky=tk.W + tk.E)
        txt_file_name = tk.Entry(modification_frame)
        txt_file_name.grid(row=4, column=1, sticky=tk.W + tk.E)

        def save_modified_signal():
            if not txt_file_name.get():
                messagebox.showerror(title="Error", message="Signal File Name is Empty!")
                return
            with open(txt_file_name.get(), 'w') as file:
                file.write(f"0\n")
                file.write(f"0\n")
                file.write(f"{len(amplitudes)}\n")
                for row in range(len(amplitudes)):
                    file.write(f'{amplitudes[row]} {phase_shifts[row]}\n')
            messagebox.showinfo(title="Successful", message="Signal Saved Successfully")

        btn_save_signal = tk.Button(modification_frame, text="Save Frequency Signal", font=('Arial', 14),
                                    command=save_modified_signal)
        btn_save_signal.grid(row=5, column=0, columnspan=2, sticky=tk.W + tk.E)
        modification_frame.pack(fill='x')

    def task_4_idft(self):
        if TestCases:
            signal_file_path = 'Task 4/IDFT/Input_Signal_IDFT_A,Phase.txt'
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        polar = HelperResources.read_polar_signal(signal_file_path)
        signal_time_domain = idft(polar)
        x_indices = [i for i in range(1, len(signal_time_domain) + 1)]

        if TestCases:
            # save_file_path = 'Task 4/idft_out.txt'
            # HelperResources.save_time_domain_signal(signal_time_domain, save_file_path)
            output_file_path = 'Task 4/IDFT/Output_Signal_IDFT.txt'
            _, s_v = HelperResources.read_only_signal(output_file_path)
            SignalSamplesAreEqual(output_file_path, x_indices, signal_time_domain)

        self.window_1_plots([x_indices],
                            [signal_time_domain],
                            ['IDFT Signal'],
                            "Time",
                            'Amplitude',
                            'Task 4.2 - IDFT')

    def task_5_dct(self):
        if TestCases:
            signal_file_path = 'Task 5/DCT/DCT_input.txt'
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        signal_time, signal_value = HelperResources.sort_2_lists(signal_time, signal_value)

        # sampling_frequency = 4000
        length = len(signal_value)

        if TestCases:
            co_number = 6
        else:
            co_number = simpledialog.askinteger("Number of Coefficient", "enter number of coefficient")
            if co_number <= 0:
                messagebox.showerror(title="Error", message="number of coefficient must be +ve")
                return
            if co_number > length:
                messagebox.showerror(title="Error", message="number of coefficient must be less than length")
                return

        dct = []
        K_array = list(range(0, co_number))
        term1 = math.sqrt((2 / length))
        for k in K_array:
            summation = 0.0
            for n, y_n in zip(signal_time, signal_value):
                summation += y_n * math.cos((math.pi / (4 * length)) * float(2 * n - 1) * float(2 * k - 1))
            dct.append(term1 * summation)
        print(f'dct {dct}')
        signal_time = [int(x) for x in signal_time]
        print(f'signal time  {signal_time}')
        combined_values = list(zip(signal_time, dct))
        file_path = "Task 5 Output - compute_dct.txt"
        with open(file_path, 'w') as file:
            file.write("0\n")
            file.write("1\n")
            file.write(f'{co_number}\n')
            for x, y in combined_values:
                file.write(f"{x}\t{y}\n")

        if TestCases:
            output_file_path = 'Task 5/DCT/DCT_output.txt'
            Task_5_comparesignal2.SignalSamplesAreEqual(output_file_path, dct)

    def task_5_remove_dc_using_avg(self):
        if TestCases:
            signal_file_path = 'Task 5/Remove DC component/DC_component_input.txt'
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        signal_time, signal_value = HelperResources.sort_2_lists(signal_time, signal_value)

        average = sum(signal_value) / len(signal_value)
        signal_value_without_dc = [round(value - average, 3) for value in signal_value]

        HelperResources.save_time_domain_signal(signal_value_without_dc, 'Task 5 Output - remove_dc_using_avg.txt')

        if TestCases:
            output_file_path = 'Task 5/Remove DC component/DC_component_output.txt'
            Task_5_comparesignal2.SignalSamplesAreEqual(output_file_path, signal_value_without_dc)

        self.window_1_plots([signal_time, signal_time],
                            [signal_value, signal_value_without_dc],
                            ['Original Signal', 'Removed DC Signal'],
                            "Time",
                            'Amplitude',
                            'Task 5.2 - Signal After Removing DC Component (using Average)')

    def task_5_remove_dc_using_harmonics(self):
        if TestCases:
            signal_file_path = 'Task 5/Remove DC component/DC_component_input.txt'
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        signal_time, signal_value = HelperResources.sort_2_lists(signal_time, signal_value)

        harmonics = dft(signal_value)
        harmonics[0] = complex(0, 0)
        amplitudes = [abs(x_k_n) for x_k_n in harmonics]
        phase_shifts = [cmath.phase(x_k_n) for x_k_n in harmonics]
        polar = list(zip(amplitudes, phase_shifts))
        signal_value_without_dc = idft(polar)

        HelperResources.save_time_domain_signal(signal_value_without_dc,
                                                'Task 5 Output - remove_dc_using_harmonics.txt')

        if TestCases:
            output_file_path = 'Task 5/Remove DC component/DC_component_output.txt'
            Task_5_comparesignal2.SignalSamplesAreEqual(output_file_path, signal_value_without_dc)

        self.window_1_plots([signal_time, signal_time],
                            [signal_value, signal_value_without_dc],
                            ['Original Signal', 'Removed DC Signal'],
                            "Time",
                            'Amplitude',
                            'Task 5.2 - Signal After Removing DC Component (using Harmonics)')

    # def task_6_smoothing(self): # >>>>>>>>>>>>>>>>> WITH PADDING <<<<<<<<<<<<<<<<<<<<<<<<<<
    #     # Clear the previous plot
    #     for widget in self.plots_frame.winfo_children():
    #         widget.destroy()
    #
    #     fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))
    #
    #     signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
    #     if not signal_file_path:
    #         messagebox.showerror(title="Error", message="Signal Data File Not Found!")
    #         return
    #
    #     signal_time, signal_value = self.read_only_signal(signal_file_path)
    #     signal_time, signal_value = self.sort_2_lists(signal_time, signal_value)
    #
    #     filter_size = simpledialog.askinteger("enter filter size", "enter filter size")
    #     if filter_size <= 0:
    #         messagebox.showerror(title="Error", message="filter size must be +ve")
    #         return
    #     avg_value=[]
    #     time_for_avg = []
    #     # calculate padding *2 in case we add at the end of the values array
    #     padding = (filter_size-1)
    #     #for adding zero padding to values
    #     for i in range(1,int(padding)+1):
    #         signal_value.append(0)
    #
    #     for t, v in zip(signal_time,signal_value):
    #         index = signal_value.index(v)
    #         sum = 0
    #         for index in range(index , index + filter_size):
    #             sum += signal_value[index]
    #         sum = sum / filter_size
    #         avg_value.append(sum)
    #         time_for_avg.append(t)
    #
    #     combined_values = list(zip(time_for_avg,avg_value))
    #     # print(combined_values)
    #     print(f'length : {len(avg_value)}')
    #     print(f' average values : \n{avg_value}')
    #     # Embed the Matplotlib plot in the Tkinter window
    #     canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
    #     canvas.get_tk_widget().pack()

    def task_6_smoothing(self):  ## >>>>>>>>>>>>>>>>> WITHOUT PADDING <<<<<<<<<<<<<<<<<<<<<<<
        if TestCases:
            signal_file_path = 'Task 6/Moving Average/MovAvgTest2.txt'
            filter_size = 5
            if messagebox.askyesno(title="Test Signal",
                                   message="Yes -> Test Case 1 with Filter Size = 3\nNo  -> Test Case 2 with Filter Size = 5"):
                signal_file_path = 'Task 6/Moving Average/MovAvgTest1.txt'
                filter_size = 3
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

            filter_size = simpledialog.askinteger("enter filter size", "enter filter size")
            if filter_size <= 0:
                messagebox.showerror(title="Error", message="filter size must be +ve")
                return

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        signal_time, signal_value = HelperResources.sort_2_lists(signal_time, signal_value)

        avg_value = []
        time_for_avg = []
        for index, (t, v) in enumerate(zip(signal_time, signal_value)):
            if index > (len(signal_value) - filter_size):
                break
            sum = 0
            for index in range(index, index + filter_size):
                sum += signal_value[index]
            avg_value.append((sum / filter_size))
            time_for_avg.append(t)

        time_for_avg = [int(x) for x in time_for_avg]
        signal_with_time = list(zip(time_for_avg, avg_value))
        print(f'Moving Average Signal: {signal_with_time}')

        self.window_2_plots([signal_time, time_for_avg],
                            [signal_value, avg_value],
                            ['Original Signal', 'Average Signal'],
                            "Time",
                            'Amplitude',
                            'Task 6.1 - Moving Average Signal',
                            'Task 6.1 - Moving Average Signal')

    def task_6_sharpening(self):
        if TestCases:
            signal_value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                            25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
                            47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68,
                            69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
                            91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

            signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
            signal_time, signal_value = HelperResources.sort_2_lists(signal_time, signal_value)

        first_derivative = [current_value - (signal_value[i - 1] if i != 0 else 0) for i, current_value in
                            enumerate(signal_value)][1:]
        second_derivative = [(signal_value[i + 1] if i < len(signal_value) - 1 else 0) + (
            signal_value[i - 1] if i != 0 else 0) - 2 * current_value for i, current_value in
                             enumerate(signal_value)][:(len(signal_value) - 1)]
        print(f"Signal Value  : {signal_value}")
        print(f"1st-Derivative: {first_derivative}")
        print(f"2nd-Derivative: {second_derivative}")
        print(f"Signal Value (Len)  : {len(signal_value)}")
        print(f"1st-Derivative (Len): {len(first_derivative)}")
        print(f"2nd-Derivative (Len): {len(second_derivative)}")
        if TestCases:
            Task_6_DerivativeSignal.DerivativeSignal(first_derivative, second_derivative)
        self.window_2_plots([],
                            [first_derivative, second_derivative, signal_value],
                            ['1st Derivative', '2nd Derivative', 'Original Signal'],
                            "Time",
                            'Amplitude',
                            'Task 6.2 - 1st & 2nd Derivatives',
                            'Task 6.2 - 1st & 2nd Derivatives')

    def task_6_delay_advance_signal(self):
        if TestCases:
            signal_file_path = 'Task 6/Shifting and Folding/input_fold.txt'
            k_steps = 2

        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return
            k_steps = simpledialog.askinteger("Delaying/Advancing Steps", "# of Steps to Delay (+ve) or Advance (-ve)")

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        signal_time, signal_value = HelperResources.sort_2_lists(signal_time, signal_value)

        new_label = "Delay" if k_steps > 0 else "Advanc"
        new_signal_time = [t + k_steps for t in signal_time]
        print(f"Signal Time    : {signal_time}")
        print(f"New Signal Time: {new_signal_time}")

        self.window_1_plots([signal_time, new_signal_time],
                            [signal_value, signal_value],
                            ['Original Signal', f'{new_label}ed Signal'],
                            "Time",
                            'Amplitude',
                            f'Task 6.3 - {new_label}ing Signal with Steps(K)={k_steps}')

    def task_6_folding(self):
        if TestCases:
            signal_file_path = 'Task 6/Shifting and Folding/input_fold.txt'
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        signal_time, signal_value = HelperResources.sort_2_lists(signal_time, signal_value)

        new_signal_time = [(-1 * x) for x in signal_time]
        new_signal_time, new_signal_value = HelperResources.sort_2_lists(new_signal_time, signal_value)

        if TestCases:
            output_file_path = 'Task 6/Shifting and Folding/Output_fold.txt'
            Task_6_Shift_Fold_Signal.Shift_Fold_Signal(output_file_path, new_signal_time, new_signal_value)

        self.window_1_plots([signal_time, new_signal_time],
                            [signal_value, new_signal_value],
                            ['Original Signal', 'Folded Signal'],
                            "Time",
                            'Amplitude',
                            f'Task 6.4 - Folding Signal')

    def task_6_delay_advance_folded_signal(self):
        if TestCases:
            signal_file_path = "Task 6/Shifting and Folding/input_fold.txt"
            output_file_path = "Task 6/Shifting and Folding/Output_ShiftFoldedby-500.txt"
            k_steps = -500
            is_test_500 = messagebox.askyesno(title="Test Signal",
                                              message="Yes -> Delay with 500\nNo  -> Advance with -500")
            if is_test_500:
                output_file_path = "Task 6/Shifting and Folding/Output_ShifFoldedby500.txt"
                k_steps = 500
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return
            k_steps = simpledialog.askinteger("Delaying/Advancing Steps", "# of Steps to Delay (+ve) or Advance (-ve)")

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        signal_time, signal_value = HelperResources.sort_2_lists(signal_time, signal_value)

        # Folding
        folded_signal_time = [(-1 * x) for x in signal_time]
        folded_signal_time, folded_signal_value = HelperResources.sort_2_lists(folded_signal_time, signal_value)

        # Delaying / Advancing
        new_label = "Delay" if k_steps > 0 else "Advanc"
        delayed_folded_signal_time = [t + k_steps for t in folded_signal_time]
        print(f"Signal Time    : {signal_time}")
        print(f"New Signal Time: {delayed_folded_signal_time}")

        if TestCases:
            Task_6_Shift_Fold_Signal.Shift_Fold_Signal(output_file_path, delayed_folded_signal_time,
                                                       folded_signal_value)

        self.window_1_plots([signal_time, delayed_folded_signal_time],
                            [signal_value, folded_signal_value],
                            ['Original Signal', f'{new_label}ed Folded Signal'],
                            "Time",
                            'Amplitude',
                            f'Task 6.5 - {new_label}ing a Folded Signal with Steps(K)={k_steps}')

    def task_6_remove_dc_in_freqdomain(self):
        if TestCases:
            signal_file_path = 'Task 5/Remove DC component/DC_component_input.txt'
        else:
            signal_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        signal_time, signal_value = HelperResources.read_only_signal(signal_file_path)
        signal_time, signal_value = HelperResources.sort_2_lists(signal_time, signal_value)

        harmonics = dft(signal_value)
        harmonics[0] = complex(0, 0)
        amplitudes = [abs(x_k_n) for x_k_n in harmonics]
        phase_shifts = [cmath.phase(x_k_n) for x_k_n in harmonics]
        polar = list(zip(amplitudes, phase_shifts))
        signal_value_without_dc = idft(polar)

        HelperResources.save_time_domain_signal(signal_value_without_dc,
                                                'Task 6 Output - remove_dc_using_harmonics.txt')

        if TestCases:
            output_file_path = 'Task 5/Remove DC component/DC_component_output.txt'
            Task_5_comparesignal2.SignalSamplesAreEqual(output_file_path, signal_value_without_dc)

        self.window_1_plots([signal_time, signal_time],
                            [signal_value, signal_value_without_dc],
                            ['Original Signal', 'Removed DC Signal'],
                            "Time",
                            'Amplitude',
                            'Task 6.6 - Signal After Removing DC Component in Frequency Domain')

    def task_7_convolution_time_domain(self):
        # out_of_range = lambda signal_v, signal_t, index: signal_v[signal_t.index(index)] if index in signal_t else 0
        def out_of_range(signal_v, signal_t, index):
            return signal_v[signal_t.index(index)] if index in signal_t else 0

        if TestCases:
            signal_file_path_1 = "Task 7/Convolution/Input_conv_Sig1.txt"
            signal_file_path_2 = "Task 7/Convolution/Input_conv_Sig2.txt"
        else:
            signal_file_path_1 = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path_1:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

            signal_file_path_2 = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path_2:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        signal_time_1, signal_value_1 = HelperResources.read_only_signal(signal_file_path_1)
        signal_time_1, signal_value_1 = HelperResources.sort_2_lists(signal_time_1, signal_value_1)

        signal_time_2, signal_value_2 = HelperResources.read_only_signal(signal_file_path_2)
        signal_time_2, signal_value_2 = HelperResources.sort_2_lists(signal_time_2, signal_value_2)

        min_i = int(signal_time_1[0] + signal_time_2[0])
        max_i = int(signal_time_1[-1] + signal_time_2[-1])
        convoluted_signal_time = list(range(min_i, max_i + 1, 1))

        convoluted_signal_value = []
        for n in convoluted_signal_time:
            y_n = 0
            # print(f"K: {n} -> Value[1]: {out_of_range(signal_value_1, signal_time_1, n)}")
            # print(f"K: {n} -> Value[2]: {out_of_range(signal_value_2, signal_time_2, n)}")
            for k in convoluted_signal_time:
                y_n += out_of_range(signal_value_1, signal_time_1, k) * out_of_range(signal_value_2, signal_time_2,
                                                                                     n - k)
            convoluted_signal_value.append(y_n)

        print(f"Convoluted Signal Time  : {convoluted_signal_time}")
        print(f"Convoluted Signal Value : {convoluted_signal_value}")

        if TestCases:
            Task_7_ConvTest.ConvTest(convoluted_signal_time, convoluted_signal_value)

        self.window_2_plots([signal_time_1, signal_time_2, convoluted_signal_time],
                            [signal_value_1, signal_value_2, convoluted_signal_value],
                            ['Signal 1 - X(K)', 'Signal 2 - H(K)', 'Convoluted Signal'],
                            "Time",
                            'Amplitude',
                            f'Task 7 - Convolution (Time Domain) [Signals]',
                            f'Task 7 - Convolution (Time Domain) [Value]')

    def task_8_direct_correlation(self):
        if TestCases:
            signal_file_path_1 = "Task 8/Correlation/Corr_input signal1.txt"
            signal_file_path_2 = "Task 8/Correlation/Corr_input signal2.txt"
        else:
            signal_file_path_1 = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path_1:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

            signal_file_path_2 = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path_2:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        signal_time_1, signal_value_1, signal_periodicity_1 = HelperResources.read_signal_periodicity(
            signal_file_path_1)
        signal_time_1, signal_value_1 = HelperResources.sort_2_lists(signal_time_1, signal_value_1)

        signal_time_2, signal_value_2, signal_periodicity_2 = HelperResources.read_signal_periodicity(
            signal_file_path_2)
        signal_time_2, signal_value_2 = HelperResources.sort_2_lists(signal_time_2, signal_value_2)

        normalized_correlated_signal = direct_correlation_2_signals(signal_value_1, signal_value_2,
                                                                    signal_periodicity_2)

        if TestCases:
            output_file_path = "Task 8/Correlation/CorrOutput.txt"
            Task_8_CompareSignal.Compare_Signals(output_file_path, signal_time_1, normalized_correlated_signal)

        self.window_2_plots([signal_time_1, signal_time_2, signal_time_1],
                            [signal_value_1, signal_value_2, normalized_correlated_signal],
                            ['Signal 1', 'Signal 2', 'Normalized Correlation'],
                            "Time",
                            'Amplitude',
                            f'Task 8.1 - Correlation (Time Domain) [Signals]',
                            'Task 8.1 - Correlation (Time Domain) [Value]')

    def task_8_time_analysis_BONUS(self):
        """
        perform time delay analysis,
        given two periodic signals and the sampling period,
        find approximately the delay between them.
        """

        if TestCases:
            signal_file_path_1 = "Task 8/Time analysis/TD_input signal1.txt"
            signal_file_path_2 = "Task 8/Time analysis/TD_input signal2.txt"
            sampling_frequency = 100
        else:
            signal_file_path_1 = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path_1:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

            signal_file_path_2 = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path_2:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

            sampling_frequency = simpledialog.askinteger("Sampling Frequency",
                                                         "Enter a +ve Sampling Frequency in (Hz):")
            if sampling_frequency <= 0:
                messagebox.showerror(title="Error", message="Sampling Frequency must be non-negative")
                return

        signal_time_1, signal_value_1 = HelperResources.read_only_signal(signal_file_path_1)
        signal_time_1, signal_value_1 = HelperResources.sort_2_lists(signal_time_1, signal_value_1)

        signal_time_2, signal_value_2 = HelperResources.read_only_signal(signal_file_path_2)
        signal_time_2, signal_value_2 = HelperResources.sort_2_lists(signal_time_2, signal_value_2)

        normalized_correlated_signal = fast_correlation_2_signals(signal_value_1, signal_value_2)

        print("=" * 200)
        print(f"Sampling Frequency                  : {sampling_frequency}")

        absolute_normalized_correlated_signal = [abs(corr) for corr in normalized_correlated_signal]
        maximum_absolute_correlation = max(absolute_normalized_correlated_signal)
        index_maximum_absolute_correlation = absolute_normalized_correlated_signal.index(maximum_absolute_correlation)
        print(f"Maximum Absolute Correlation        : {maximum_absolute_correlation}")
        print(f"Index Maximum Absolute Correlation  : {index_maximum_absolute_correlation}")

        time_delay = index_maximum_absolute_correlation / sampling_frequency
        print(f"Time Delay (Time-Analysis)          : {time_delay}")
        print("=" * 200)

        self.window_2_plots([signal_time_1, signal_time_2, signal_time_1],
                            [signal_value_1, signal_value_2, normalized_correlated_signal],
                            ['Signal 1', 'Signal 2', 'Normalized Correlation'],
                            "Time",
                            'Amplitude',
                            f'Task 8.2 - Time Analysis [Signals]',
                            f'Task 8.2 - Time Analysis [Correlation]\nTime Delayed = {time_delay}s, FS = {sampling_frequency}Hz, and Index Maximum Absolute Correlation = {index_maximum_absolute_correlation}')

    def task_8_template_matching_BONUS(self):
        """
        the user will give the paths for two folders of two classes and a test folder,
        using template matching the application will give labels for all signals in test folder
        """

        def print_class_lists(list_of_lists, its_name):
            num_of_lists = len(list_of_lists)
            labeled_lists = {}
            for i in range(num_of_lists):
                label = f'Signal {i + 1}'
                labeled_lists[label] = list_of_lists[i]
            print("=" * 400)
            print(f'Number of Signals ({its_name}): {num_of_lists}')
            for label, lst in labeled_lists.items():
                print(f'{its_name} - {label} (N: {len(lst)}): {lst}')

        def template_matching_read_file(signal_file_path):
            with open(signal_file_path, 'r') as file:
                lines = file.readlines()
                signal_value = []
                for line in lines:
                    signal_value.append(float(line))
            return signal_value

        def template_matching_read_folder(signals_folder_path):
            class_signals = []
            for filename in os.listdir(signals_folder_path):
                file_path = os.path.join(signals_folder_path, filename)
                class_signals.append(template_matching_read_file(file_path))
            return class_signals

        if TestCases:
            folder_path_1 = 'Task 8/Template Matching/Class 1'
            folder_path_2 = 'Task 8/Template Matching/Class 2'
        else:
            folder_path_1 = filedialog.askdirectory(title="Select Signals Folder (Class-1)")
            if not folder_path_1:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

            folder_path_2 = filedialog.askdirectory(title="Select Signals Folder (Class-2)")
            if not folder_path_2:
                messagebox.showerror(title="Error", message="Signal Data Folder Not Found!")
                return

        class_1_signals = template_matching_read_folder(folder_path_1)
        class_2_signals = template_matching_read_folder(folder_path_2)
        # print_class_lists(class_1_signals, "Down")
        # print_class_lists(class_2_signals, "UP")

        class_1_length = len(class_1_signals)
        class_2_length = len(class_2_signals)

        class_1_average = [sum(items) / class_1_length for items in zip(*class_1_signals)]
        class_2_average = [sum(items) / class_2_length for items in zip(*class_2_signals)]

        print("=" * 200)
        print(f"Class 1 - Average       : {class_1_average}")
        print(f"Class 2 - Average       : {class_2_average}")

        if TestCases:
            test_file_path = 'Task 8/Template Matching/Test Signals/Test2.txt'
            if messagebox.askyesno(title="Test Case", message="Yes -> Test Case 1\nNo  -> Test Case 2"):
                test_file_path = 'Task 8/Template Matching/Test Signals/Test1.txt'
        else:
            test_file_path = filedialog.askopenfilename(title="Select Signal Data File")
            if not test_file_path:
                messagebox.showerror(title="Error", message="Signal Data FileNot Found!")
                return

        test_signal = template_matching_read_file(test_file_path)

        normalized_correlated_class_1 = fast_correlation_2_signals(class_1_average, test_signal)
        absolute_normalized_correlated_class_1 = [abs(corr) for corr in normalized_correlated_class_1]
        maximum_absolute_correlation_class_1 = max(absolute_normalized_correlated_class_1)

        normalized_correlated_class_2 = fast_correlation_2_signals(class_2_average, test_signal)
        absolute_normalized_correlated_class_2 = [abs(corr) for corr in normalized_correlated_class_2]
        maximum_absolute_correlation_class_2 = max(absolute_normalized_correlated_class_2)

        print(f"Class 1 (DOWN) - Max Correlation    : {maximum_absolute_correlation_class_1}")
        print(f"Class 2 ( UP ) - Max Correlation    : {maximum_absolute_correlation_class_2}")

        if maximum_absolute_correlation_class_1 > maximum_absolute_correlation_class_2:
            best_match_label = "DOWN Class"
            best_match_class_average = class_1_average
            best_match_class_normalized_correlation = normalized_correlated_class_1
        else:
            best_match_label = "UP Class"
            best_match_class_average = class_2_average
            best_match_class_normalized_correlation = normalized_correlated_class_2

        print(f"Best Match - Class                  : {best_match_label}")
        print(f"Best Match - Average                : {best_match_class_average}")
        print(f"Best Match - Normalized_Correlation : {best_match_class_normalized_correlation}")
        print("=" * 200)

        self.window_2_plots([],
                            [best_match_class_average, best_match_class_normalized_correlation],
                            ['Average Signal', 'Normalized Correlation'],
                            "Time",
                            'Amplitude',
                            f'Task 8.3 - Template Matching with Tested File and best match {best_match_label}',
                            f'Task 8.3 - Template Matching with Tested File and best match {best_match_label}')

    def task_9_fast_convolution(self):
        if TestCases:
            signal_file_path_1 = "Task 9/Fast Convolution/Input_conv_Sig1.txt"
            signal_file_path_2 = "Task 9/Fast Convolution/Input_conv_Sig2.txt"
        else:
            signal_file_path_1 = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path_1:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

            signal_file_path_2 = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path_2:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        # signal_file_path_1 = "Task 7/Convolution/Input_conv_Sig1.txt"
        signal_time1, signal_value1 = HelperResources.read_only_signal(signal_file_path_1)
        signal_time1, signal_value1 = HelperResources.sort_2_lists(signal_time1, signal_value1)

        # signal_file_path_2 = "Task 7/Convolution/Input_conv_Sig2.txt"
        signal_time2, signal_value2 = HelperResources.read_only_signal(signal_file_path_2)
        signal_time2, signal_value2 = HelperResources.sort_2_lists(signal_time2, signal_value2)

        min_index = signal_time1[0] + signal_time2[0]
        max_index = signal_time1[-1] + signal_time2[-1]

        output_time = list(range(int(min_index), int(max_index) + 1))
        number_of_elements = len(output_time)

        signal_value1 = np.pad(signal_value1, (0, number_of_elements - len(signal_value1)))
        signal_value2 = np.pad(signal_value2, (0, number_of_elements - len(signal_value2)))

        signal1_freq_domain = dft(signal_value1)
        signal2_freq_domain = dft(signal_value2)

        output = [a * b for a, b in zip(signal1_freq_domain, signal2_freq_domain)]

        amplitude = [abs(x) for x in output]
        phase_shift = [cmath.phase(angle) for angle in output]

        polar1 = list(zip(amplitude, phase_shift))
        convoluted_signal_value = idft(polar1)
        print(f'convoluted_signal_value : {convoluted_signal_value}')

        if TestCases:
            Task_9_ConvTest.ConvTest(output_time, convoluted_signal_value)

        self.window_1_plots([output_time],
                            [convoluted_signal_value],
                            ['Convoluted Signal'],
                            "Time",
                            'Amplitude',
                            'Task 9.1 - Convolution (Frequency Domain)')

    def task_9_fast_correlation(self):
        if TestCases:
            signal_file_path_1 = "Task 9/Fast Correlation/Corr_input signal1.txt"
            signal_file_path_2 = "Task 9/Fast Correlation/Corr_input signal2.txt"
        else:
            signal_file_path_1 = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path_1:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

            signal_file_path_2 = filedialog.askopenfilename(title="Select Signal Data File")
            if not signal_file_path_2:
                messagebox.showerror(title="Error", message="Signal Data File Not Found!")
                return

        signal_time1, signal_value1 = HelperResources.read_only_signal(signal_file_path_1)
        signal_time1, signal_value1 = HelperResources.sort_2_lists(signal_time1, signal_value1)

        signal_time2, signal_value2 = HelperResources.read_only_signal(signal_file_path_2)
        signal_time2, signal_value2 = HelperResources.sort_2_lists(signal_time2, signal_value2)

        signal1_freq_domain = dft(signal_value1)
        signal2_freq_domain = dft(signal_value2)

        output = [a * b for a, b in zip(np.conj(signal1_freq_domain), signal2_freq_domain)]
        print(f'conj :   {np.conj(signal1_freq_domain)}')
        amplitude = [abs(x) for x in output]
        phase_shift = [cmath.phase(angle) for angle in output]

        polar1 = list(zip(amplitude, phase_shift))
        signal_time_domain = idft(polar1)
        final_cross_correlation = [int(a) * 1 / len(signal_value2) for a in signal_time_domain]
        print(f'correlation  : {final_cross_correlation}')

        signal1_sum_square = np.sum(np.square(signal_value1))
        signal2_sum_square = np.sum(np.square(signal_value2))
        normalization_term = 1 / len(signal_value2) * np.sqrt(signal2_sum_square * signal1_sum_square)
        normalized_signal = [a / normalization_term for a in final_cross_correlation]
        print(f'final after normalization : {normalized_signal}')

        if TestCases:
            output_file_path = "Task 9/Fast Correlation/Corr_Output.txt"
            Task_9_CompareSignal.Compare_Signals(output_file_path, signal_time1, final_cross_correlation)

        self.window_1_plots([signal_time2],
                            [normalized_signal],
                            ['Correlation'],
                            "Time",
                            'Amplitude',
                            'Task 9.2 - Correlation (Frequency Domain)')

    def window_2_plots(self, signal_times, signal_values, legends, x_label, y_label, title_1, title_2):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.screen_width / 100, self.screen_height / 110))
        fig.subplots_adjust(hspace=0.3)
        fig.patch.set_facecolor(self.plots_bg_color)

        number_of_signals = len(legends)

        x_axis = [x_label, x_label]
        y_axis = [y_label, y_label]

        if isinstance(y_label, list):
            y_axis = y_label
        if isinstance(x_label, list):
            x_axis = x_label
        colors = ['green', 'orange', 'blue', 'yellow']

        for i in range(number_of_signals - 1):
            if not signal_times:
                ax1.plot(signal_values[i], color=colors[i], label=legends[i])
            else:
                ax1.plot(signal_times[i], signal_values[i], color=colors[i], label=legends[i])
        ax1.legend()
        ax1.set_xlabel(x_axis[0])
        ax1.set_ylabel(y_axis[0])
        ax1.set_title(title_1)
        ax1.grid(True)

        if not signal_times:
            ax2.plot(signal_values[-1], color='red', label=legends[-1])
        else:
            ax2.plot(signal_times[-1], signal_values[-1], color='red', label=legends[-1])
        ax2.legend()
        ax2.set_xlabel(x_axis[1])
        ax2.set_ylabel(y_axis[1])
        ax2.set_title(title_2)
        ax2.grid(True)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def window_2_plots_freq_domain(self, x_axis, amplitudes, phase_shifts):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.screen_width / 100, self.screen_height / 110))
        fig.subplots_adjust(hspace=0.3)
        fig.patch.set_facecolor(self.plots_bg_color)

        ax1.stem(x_axis, amplitudes)
        ax1.set_xticks(x_axis)
        ax1.set_xticklabels(x_axis)
        ax1.set_xlabel("Frequency Index")
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Task 4 - Amplitude vs Frequencies')
        ax1.grid(True)

        ax2.stem(x_axis, phase_shifts)
        ax2.set_xticks(x_axis)
        ax2.set_xticklabels(x_axis)
        ax2.set_xlabel("Frequency Index")
        ax2.set_ylabel('Phase Shift (in Degrees)')
        ax2.set_title('Task 4 - Phase Shift vs Frequencies')
        ax2.grid(True)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def window_1_plots(self, signal_times, signal_values, legends, x_label, y_label, title):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))
        fig.patch.set_facecolor(self.plots_bg_color)

        number_of_signals = len(legends)

        colors = ['green', 'orange', 'blue', 'yellow', 'red']

        for i in range(number_of_signals):
            if not signal_times:
                plt.plot(signal_values[i], color=colors[i], label=legends[i])
            else:
                plt.plot(signal_times[i], signal_values[i], color=colors[i], label=legends[i])
        plt.legend()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid(True)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="U really want 2 quit? :("):
            print("Bye! :\" ")
            self.root.destroy()


GUI()

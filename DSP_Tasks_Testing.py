import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import numpy as np
from numpy import outer

from comparesignals import SignalSamplesAreEqual
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler


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

        # self.root.geometry("800x800")
        self.root.title("DSP Tasks - CS6")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.menubar = tk.Menu(self.root)
        self.task_1_menu = tk.Menu(self.menubar, tearoff=0)
        self.task_1_menu.add_command(label="(1.1) Generate Cont. & Disc. Signals", command=self.task_1_1)
        self.task_1_menu.add_separator()
        self.task_1_menu.add_command(label="(1.2) Generate Sin/Cos Signal", command=self.task_1_2)

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

        self.root.config(menu=self.menubar)

        self.plots_frame = tk.Frame(self.root)
        self.plots_frame.grid(row=0, column=0)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def sort_2_lists(self, list_1, list_2):
        combined_lists = list(zip(list_1, list_2))
        combined_lists.sort(key=lambda l: l[0])
        x, y = zip(*combined_lists)
        x = list(x)
        y = list(y)
        return x, y

    def extend_signal_calculation(self, signal_t, signal_val, new_max_length):
        signal_val = signal_val + [0] * (new_max_length - len(signal_val))
        signal_t.extend(range(len(signal_t), new_max_length))
        return signal_t, signal_val

    def extend_signals(self, list_signal_times, list_signal_values):
        signal_lengths = [len(signal) for signal in list_signal_times]
        max_len = max(signal_lengths)
        number_of_signals = len(signal_lengths)
        current_signal = 0
        while current_signal <= number_of_signals - 1:
            list_signal_values[current_signal], list_signal_times[current_signal] = self.extend_signal_calculation(list_signal_values[current_signal], list_signal_times[current_signal], max_len)
            current_signal += 1
        return list_signal_times, list_signal_values

    def read_only_signal(self, signal_file_path):
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

    def task_1_1(self):
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

            if signal_details[1] == 1:      # [1] Period
                periodic = 'Periodic'
                start_of_cycle = 0
                end_of_cycle = signal_details[2]
                temp_y = y
                for i in range(1, 3):
                    start_of_cycle += signal_details[2]
                    end_of_cycle += signal_details[2]
                    x.extend(range(start_of_cycle, end_of_cycle))
                    y = y + temp_y

            if signal_details[0] == 1:      # [0] Frequency Domain
                x_label = 'f'
                domain = 'Frequency'

            title = f'{periodic} {domain} Domain with {signal_details[2]} Samples'
            if signal_details[0] == 1 and signal_details[3]:      # [3] Phase Shift
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
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))


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
        
        x_values = np.arange(0, 1, 1/sampling_frequency)
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
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))


        output_path = "Task 2/output_signals/signal1+signal3.txt"
        signal_2_file_path = "Task 2/input_signals/signal3.txt"
        if messagebox.askyesno(title="Test Signal", message="Yes -> Signal 2 (S1 + S2)\nNo  -> Signal 3 (S1 + S3)"):
            output_path = "Task 2/output_signals/Signal1+signal2.txt"
            signal_2_file_path = "Task 2/input_signals/Signal2.txt"

        signal_1_file_path = "Task 2/input_signals/Signal1.txt"
        file_paths = [signal_1_file_path, signal_2_file_path]
        signal_number = 0
        lengths_equal = 1
        signal_times = []
        signal_values = []
        signal_time_temp, signal_value_temp = self.read_only_signal(file_paths[0])
        signal_times.append(signal_time_temp)
        signal_values.append(signal_value_temp)
        file_paths.pop(0)
        for file_path in file_paths:
            signal_number += 1
            signal_time_temp, signal_value_temp = self.read_only_signal(file_path)
            signal_times.append(signal_time_temp)
            signal_values.append(signal_value_temp)
            if len(signal_times[0]) != len(signal_times[signal_number]):
                lengths_equal = 0
            signal_times[signal_number], signal_values[signal_number] = self.sort_2_lists(signal_times[signal_number], signal_values[signal_number])

        if not lengths_equal:
            signal_times, signal_values = self.extend_signals(signal_times, signal_values)
            messagebox.showwarning(title="Warning", message="Signal Lengths are not Equal!")

        result_addition_signal = np.sum(signal_values, axis=0)

        SignalSamplesAreEqual(output_path, None, result_addition_signal)

        # plt.plot(signal_times[0], result_addition_signal, color='orange')
        plt.scatter(signal_times[0], result_addition_signal)
        plt.xlabel("Time")
        plt.ylabel('Amplitude')
        plt.title('Task 2.1 - Addition Signal')
        plt.grid(True)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def task_2_2_subtraction(self):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))

        output_path = "Task 2/output_signals/signal1-signal3.txt"
        signal_2_file_path = "Task 2/input_signals/signal3.txt"
        if messagebox.askyesno(title="Test Signal", message="Yes -> Signal 2 (S1 - S2)\nNo  -> Signal 3 (S1 - S3)"):
            output_path = "Task 2/output_signals/signal1-signal2.txt"
            signal_2_file_path = "Task 2/input_signals/Signal2.txt"

        signal_1_file_path = "Task 2/input_signals/Signal1.txt"
        signal_1_time, signal_1_value = self.read_only_signal(signal_1_file_path)
        signal_1_time, signal_1_value = self.sort_2_lists(signal_1_time, signal_1_value)

        signal_2_time, signal_2_value = self.read_only_signal(signal_2_file_path)
        signal_2_time, signal_2_value = self.sort_2_lists(signal_2_time, signal_2_value)

        # Not Equal Length Check
        if len(signal_1_time) < len(signal_2_time):
            signal_1_time, signal_1_value = self.extend_signal_calculation(signal_1_time, signal_1_value, len(signal_2_value))
            messagebox.showwarning(title="Warning", message="Signal Lengths are not Equal!")
        elif len(signal_1_time) > len(signal_2_time):
            signal_2_time, signal_2_value = self.extend_signal_calculation(signal_2_time, signal_2_value, len(signal_1_value))
            messagebox.showwarning(title="Warning", message="Signal Lengths are not Equal!")

        result_subtraction_signal = np.subtract(signal_2_value, signal_1_value)

        SignalSamplesAreEqual(output_path, None, result_subtraction_signal)

        # plt.plot(signal_1_time, result_subtraction_signal, color='orange')
        plt.scatter(signal_1_time, result_subtraction_signal)
        plt.xlabel("Time")
        plt.ylabel('Amplitude')
        plt.title('Task 2.2 - Subtraction Signal')
        plt.grid(True)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def task_2_3_multiplication(self):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))

        output_path = "Task 2/output_signals/MultiplySignalByConstant-signal2 - by 10.txt"
        signal_file_path = "Task 2/input_signals/Signal2.txt"
        factor = 10
        if messagebox.askyesno(title="Test Signal", message="Yes -> Signal 1 (Factor = 5)\nNo  -> Signal 2 (Factor = 10)"):
            output_path = "Task 2/output_signals/MultiplySignalByConstant-Signal1 - by 5.txt"
            signal_file_path = "Task 2/input_signals/Signal1.txt"
            factor = 5

        signal_time, signal_value = self.read_only_signal(signal_file_path)
        signal_value_multiplied = np.array(signal_value) * np.array(factor)
        signal_time, signal_value_multiplied = self.sort_2_lists(signal_time, signal_value_multiplied)
        SignalSamplesAreEqual(output_path, None, signal_value_multiplied)

        # plt.plot(signal_time, signal_value_multiplied, color='orange')
        plt.scatter(signal_time, signal_value_multiplied)
        plt.xlabel("Time")
        plt.ylabel('Amplitude')
        plt.title(f'Task 2.3 - Multiplication Signal by Factor = {factor}')
        plt.grid(True)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def task_2_4_squaring(self):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))

        signal_file_path = "Task 2/input_signals/Signal1.txt"
        signal_time, signal_value = self.read_only_signal(signal_file_path)
        square_signal = np.array(signal_value) * np.array(signal_value)
        SignalSamplesAreEqual("Task 2/output_signals/Output squaring signal 1.txt", None, square_signal)

        # plt.plot(signal_time, square_signal, color='orange')
        plt.scatter(signal_time, square_signal)
        plt.xlabel("Time")
        plt.ylabel('Amplitude')
        plt.title('Task 2.4 - Squared Signal')

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def task_2_5_shifting(self):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))

        signal_file_path = "Task 2/input_signals/Input Shifting.txt"
        signal_time, signal_value = self.read_only_signal(signal_file_path)
        old_min_time = min(signal_time)
        old_max_time = max(signal_time)
        shift_value = -500
        output_path = "Task 2/output_signals/output shifting by minus 500.txt"
        if messagebox.askyesno(title="Shifting Value", message="Yes -> +500\nNo  -> -500"):
            shift_value = 500
            output_path = "Task 2/output_signals/output shifting by add 500.txt"
        shifted_signal = np.array(signal_time) + shift_value
        shifted_signal, signal_value = self.sort_2_lists(shifted_signal, signal_value)
        SignalSamplesAreEqual(output_path, None, signal_value)

        new_min_time = min(shifted_signal)
        new_max_time = max(shifted_signal)

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
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))

        output_path = "Task 2/output_signals/normlize signal 2 -- output.txt"
        signal_file_path = "Task 2/input_signals/Signal2.txt"
        scaler = MinMaxScaler(feature_range=(0, 1))
        if messagebox.askyesno(title="Test Signal", message="Yes -> Signal 1\nNo  -> Signal 2"):
            output_path = "Task 2/output_signals/normalize of signal 1 -- output.txt"
            signal_file_path = "Task 2/input_signals/Signal1.txt"
            scaler = MinMaxScaler(feature_range=(-1, 1))
        signal_time, signal_value = self.read_only_signal(signal_file_path)
        signal_value = np.reshape(signal_value, (-1, 1))
        normalized_signal = scaler.fit_transform(np.array(signal_value))
        normalized_result = normalized_signal.flatten()
        SignalSamplesAreEqual(output_path, None, normalized_result)

        plt.plot(signal_time, normalized_result, color='orange')
        plt.scatter(signal_time, normalized_result)
        plt.xlabel("Time")
        plt.ylabel('Amplitude')
        plt.title('Task 6 - Normalized Signal')
        plt.grid(True)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def task_2_7_accumulation(self):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))

        signal_file_path = "Task 2/input_signals/Signal1.txt"
        signal_time, signal_value = self.read_only_signal(signal_file_path)
        accumulate_signal = [sum(signal_value[:i+1]) for i in range(len(signal_value))]
        SignalSamplesAreEqual("Task 2/output_signals/output accumulation for signal1.txt", None, accumulate_signal)

        # plt.plot(signal_time, square_signal, color='orange')
        plt.scatter(signal_time, accumulate_signal)
        plt.xlabel("Time")
        plt.ylabel('Amplitude')
        plt.title('Task 2.7 - Accumulated Signal')

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="U really want 2 quit? :("):
            print("Bye! :\" ")
            self.root.destroy()

GUI()

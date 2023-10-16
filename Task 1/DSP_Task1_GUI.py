import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import numpy as np
from comparesignals import SignalSamplesAreEqual
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter


# digital 	        -> stairs
# cont. or analog   -> plot
# discrete 	        -> stem

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
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="(1.1) Generate Cont. & Disc. Signals", command=self.task_1_1)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="(1.2) Generate Sin/Cos Signal", command=self.task_1_2)

        self.menubar.add_cascade(menu=self.filemenu, label="Task 1")

        self.root.config(menu=self.menubar)

        self.plots_frame = tk.Frame(self.root)
        self.plots_frame.grid(row=0, column=0)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def task_1_1(self):
        file_path = filedialog.askopenfilename(title="Select a Signal Data File")
        if not file_path:
            messagebox.showwarning(title="Warning", message="Signal Data File Not Found!")
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

            combined_lists = list(zip(x, y))
            combined_lists.sort(key=lambda l: l[0])
            x, y = zip(*combined_lists)
            x = list(x)
            y = list(y)

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
        plt.stem(self.Xs_ContDisc, self.Ys_ContDisc)
        plt.plot(self.Xs_ContDisc, self.Ys_ContDisc, color='green')
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
            x_values = np.arange(0, 1, 1/analog_frequency)
            self.Xs_SinCos = x_values
            self.Ys_sin_analog = amplitude * np.sin(2 * np.pi * analog_frequency * x_values + phase_shift)
            self.Ys_cos_analog = amplitude * np.cos(2 * np.pi * analog_frequency * x_values + phase_shift)
            if wave_type == 1:
                name = "Sin"
                plt.plot(self.Xs_SinCos, self.Ys_sin_analog)
                SignalSamplesAreEqual("SinOutput.txt", sampling_frequency, self.Ys_sin_analog)

            else:
                name = "Cosine"
                plt.plot(self.Xs_SinCos, self.Ys_cos_analog)
                SignalSamplesAreEqual("CosOutput.txt", sampling_frequency, self.Ys_cos_analog)
        else:
            x_values = np.arange(0, 1, 1/sampling_frequency)
            self.Xs_SinCos = x_values

            # num_cycles_sample = sampling_frequency/360
            # num_cycles_analog = analog_frequency/360

            # Equation -> y = amplitude * np.sin(2 * np.pi * x + phase_shift)
            self.Ys_sin_analog = amplitude * np.sin(2 * np.pi * analog_frequency   * x_values + phase_shift)
            self.Ys_sin_sample = amplitude * np.sin(2 * np.pi * sampling_frequency * x_values + phase_shift)

            # Equation -> y = amplitude * np.cos(2 * np.pi * x + phase_shift)
            self.Ys_cos_analog = amplitude * np.cos(2 * np.pi * analog_frequency   * x_values + phase_shift)
            self.Ys_cos_sample = amplitude * np.cos(2 * np.pi * sampling_frequency * x_values + phase_shift)

            # else :
            if wave_type == 1:
                name = "Sin"
                plt.plot(self.Xs_SinCos, self.Ys_sin_sample)
                SignalSamplesAreEqual("SinOutput.txt", sampling_frequency, self.Ys_sin_analog)

            else:
                name = "Cosine"
                plt.plot(self.Xs_SinCos, self.Ys_cos_sample)
                SignalSamplesAreEqual("CosOutput.txt", sampling_frequency, self.Ys_cos_analog)

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

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="U really want 2 quit?"):
            print("Bye!")
            self.root.destroy()

GUI()

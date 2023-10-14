import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np


from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# digital 	        -> stairs
# cont. or analog   -> plot
# discrete 	        -> stem

class GUI:
    def __init__(self):
        self.root = tk.Tk()

        # self.root.geometry("800x800")
        self.root.title("DSP Tasks - CS6")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="1. Generate Cont. & Disc. Signals", command=self.task_1_1)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="2.1. Generate Sin Signal", command=self.task_1_2_1)
        self.filemenu.add_command(label="2.2. Generate Cos Signal", command=self.task_1_2_2)

        self.menubar.add_cascade(menu=self.filemenu, label="Task 1")

        self.root.config(menu=self.menubar)

        self.plots_frame = tk.Frame(self.root)
        self.plots_frame.grid(row=0, column=0)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def task_1_1(self):
        # Clear the previous plot
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(self.screen_width / 100, self.screen_height / 110))
        # fig = plt.figure(figsize=(8, 4))

        # file_path = filedialog.askopenfilename(title="Select a Signal Data File")
        file_path = "Task 1/signal2.txt"

        if not file_path:
            messagebox.showwarning(title="Warning", message="Signal Data File Not Found!")
            return

        x = []
        y = []
        z = []
        signal_details = []
        x_label = 't'

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
                elif (line_count - 3) == (signal_details[2] + 1):
                    print("end")
                    signal_details.append(int(line))
                    continue
                print(f"[{line_count}, {signal_details[2] + 1}]")
                values = line.split()  # Separate by whitespace
                x.append(float(values[0]))  # [T] Sample Index      [F] Frequency
                y.append(float(values[1]))  # [T] Sample Amplitude  [F] Amplitude

            print("#1")
            combined_lists = list(zip(x, y))
            combined_lists.sort(key=lambda l: l[0])
            x, y = zip(*combined_lists)
            x = list(x)
            y = list(y)

            print("#2")
            if signal_details[1] == 1:      # [1] Period
                start_of_cycle = 0
                end_of_cycle = signal_details[2]
                temp_y = y
                for i in range(1, 3):
                    start_of_cycle += signal_details[2]
                    end_of_cycle += signal_details[2]
                    x.extend(range(start_of_cycle, end_of_cycle))
                    y = y + temp_y

            print("#3")
            if signal_details[0] == 1:      # [0] Frequency Domain
                x_label = 'f'

            print("#4")
            if signal_details[3]:      # [3] Phase Shift
                x = [value + 3 for value in x]
                print(x)

            print("#5")

        plt.xlim(1, max(x) + 3)
        plt.stem(x, y)
        plt.plot(x, y, color='green')
        plt.xlabel(x_label)
        plt.ylabel('Amplitude')
        plt.title('Task 1.1 Plot')

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plots_frame)
        canvas.get_tk_widget().pack()

    def task_1_2_1(self):

        print("Enter Signal Data ")

        amplitude = float(input("Amplitude : "))
        sampling_frequency = float(input("sampling frequency : "))
        phase_shift = float(input("phase shift : "))
        analog_frequency = float(input("analog frequency : "))

        wave_type = input("Enter Type of Signal:\n1- Sin\n2- Cosine\n")

        if sampling_frequency >= 2*analog_frequency:
            x_values = np.arange(0, 1, 1/sampling_frequency)
            # y_values_1 = amplitude * np.sin(2 * np.pi * x_values + phase_shift)

            num_cycles_sample = sampling_frequency/360
            num_cycles_analog = analog_frequency/360

            y_values_sample = 0
            y_values_analog = 0
            name = ""
            if wave_type == '1':
                y_values_analog = amplitude * np.sin(2 * np.pi * num_cycles_sample * x_values + phase_shift)
                y_values_sample = amplitude * np.sin(2 * np.pi * num_cycles_analog * x_values + phase_shift)
                name ="Sin"

            else:
                y_values_analog = amplitude * np.cos(2 * np.pi * num_cycles_analog * x_values + phase_shift)
                y_values_sample = amplitude * np.cos(2 * np.pi * num_cycles_sample * x_values + phase_shift)
                name = "Cosine"

            # plt.plot(x_values, y_values_1)
            plt.plot(x_values, y_values_sample)
            plt.plot(x_values, y_values_analog)

            # plt.stem(x_values, y_values_sample)
            # plt.stem(x_values, y_values_analog)

            # Set the plot title, axis labels, and grid.
            plt.title(f'{name} Wave Plot')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.grid(True)

            # Show the plot.
            plt.show()

        else:
            print("ERROR , Sampling Frequency MUST BE Greater Than 2*Analog Frequency")

    def task_1_2_2(self):
        pass

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="U really want 2 quit?"):
            print("Bye!")
            self.root.destroy()

    def clear(self):
        self.textbox.delete('1.0', tk.END)

GUI()

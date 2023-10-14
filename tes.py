import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Create a function to generate and display a Matplotlib plot
def display_plot():
    # Clear the previous plot
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a new plot
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 1, 3, 5]

    fig = plt.figure(figsize=(5, 3))
    plt.plot(x, y)
    plt.title("Matplotlib Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    # Embed the Matplotlib plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack()

# Create the Tkinter window
root = tk.Tk()
root.title("Matplotlib in Tkinter")

# Create a frame to contain the Matplotlib plot
frame = ttk.Frame(root)
frame.grid(row=0, column=0)

# Create a button to trigger the plot display
plot_button = ttk.Button(root, text="Display Plot", command=display_plot)
plot_button.grid(row=1, column=0)

# Run the Tkinter main loop
root.mainloop()

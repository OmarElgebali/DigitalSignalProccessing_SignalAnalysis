import tkinter as tk
from tkinter import messagebox

class GUI:
    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("800x800")
        self.root.title("DSP Tasks - CS6")

        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="1. Generate Cont. & Disc. Signals", command=self.task_1_1)
        # self.filemenu.add_separator()
        self.filemenu.add_command(label="2. Generate Sin & Cos Signals", command=self.task_1_2)

        self.menubar.add_cascade(menu=self.filemenu, label="Task 1")

        self.root.config(menu=self.menubar)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def task_1_1(self):
        pass

    def task_1_2(self):
        pass

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="U really want 2 quit?"):
            print("Bye!")
            self.root.destroy()

    def clear(self):
        self.textbox.delete('1.0', tk.END)

GUI()

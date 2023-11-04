import tkinter as tk
from tkinter import messagebox

class GUI:
    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("500x900")
        self.root.title("DSP Tasks - CS6")

        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close Without Asking", command=exit)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close", command=self.on_closing)

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="Show Message", command=self.show_message)

        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.menubar.add_cascade(menu=self.actionmenu, label="Action")

        self.root.config(menu=self.menubar)

        self.label = tk.Label(self.root, text="Your Message", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)

        # Frame
        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.columnconfigure(2, weight=1)

        self.btn1 = tk.Button(self.buttonframe, text="1", font=('Arial', 18))
        self.btn1.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.btn2 = tk.Button(self.buttonframe, text="2", font=('Arial', 18))
        self.btn2.grid(row=0, column=1, sticky=tk.W + tk.E)
        self.btn3 = tk.Button(self.buttonframe, text="3", font=('Arial', 18))
        self.btn3.grid(row=0, column=2, sticky=tk.W + tk.E)
        self.btn4 = tk.Button(self.buttonframe, text="4", font=('Arial', 18))
        self.btn4.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.btn5 = tk.Button(self.buttonframe, text="5", font=('Arial', 18))
        self.btn5.grid(row=1, column=1, sticky=tk.W + tk.E)
        self.btn6 = tk.Button(self.buttonframe, text="6", font=('Arial', 18))
        self.btn6.grid(row=1, column=2, sticky=tk.W + tk.E)

        self.buttonframe.pack(fill='x')

        self.modification_frame = tk.Frame(self.root)
        self.modification_frame.columnconfigure(0, weight=1)
        self.modification_frame.columnconfigure(1, weight=1)

        self.lbl1 = tk.Label(self.modification_frame, text="Frequency Index (0, N-1)", font=('Arial', 16))
        self.lbl1.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.txt1 = tk.Entry(self.modification_frame)
        self.txt1.grid(row=0, column=1, sticky=tk.W + tk.E)
        self.lbl2 = tk.Label(self.modification_frame, text="Amplitude (A)", font=('Arial', 16))
        self.lbl2.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.txt2 = tk.Entry(self.modification_frame)
        self.txt2.grid(row=1, column=1, sticky=tk.W + tk.E)
        self.lbl3 = tk.Label(self.modification_frame, text="Phase Shift (Ø)", font=('Arial', 16))
        self.lbl3.grid(row=2, column=0, sticky=tk.W + tk.E)
        self.txt3 = tk.Entry(self.modification_frame)
        self.txt3.grid(row=2, column=1, sticky=tk.W + tk.E)

        self.modification_frame.pack(fill='x')

        self.textbox = tk.Text(self.root, height=5, font=('Arial', 16))
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx=10, pady=10)

        self.check_state = tk.IntVar()

        self.check = tk.Checkbutton(self.root, text="Show Messagebox", font=('Arial', 16), variable=self.check_state)
        self.check.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="Show Message", font=('Arial', 16), command=self.show_message)
        self.button.pack(padx=10, pady=10)

        self.clear_button = tk.Button(self.root, text="Clear Text", font=('Arial', 18), command=self.clear)
        self.clear_button.pack(padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def show_message(self):
        if self.check_state.get() == 0:
            print(self.textbox.get('1.0', tk.END))
        else:
            messagebox.showinfo(title="Info", message= self.textbox.get('1.0', tk.END))

    def shortcut(self, event):
        if event.state == 12 and event.keysym == "Return":
            self.show_message()

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="U really want 2 quit?"):
            print("Bye!")
            self.root.destroy()

    def clear(self):
        self.textbox.delete('1.0', tk.END)

GUI()

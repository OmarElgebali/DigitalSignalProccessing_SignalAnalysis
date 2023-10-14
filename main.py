import tkinter as tk

root = tk.Tk()

# Pre

# Label
label = tk.Label(root, text="Hello", font=('Arial', 16))
label.pack(pady=20)

# Textbox
textbox = tk.Text(root, height=4, font=('Arial', 16))
textbox.pack(padx=30, pady=10)


# Button
button = tk.Button(root, text="Click", font=('Arial', 16))
button.pack(pady=10)


# Place method (floating widget)
button = tk.Button(root, text="Click", font=('Arial', 16))
button.place(x=200, y=200, height=100, width=100)

root.mainloop()

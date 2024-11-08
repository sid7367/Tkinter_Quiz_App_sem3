import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter App")

# Create a label
label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

# Start the main event loop
root.mainloop()

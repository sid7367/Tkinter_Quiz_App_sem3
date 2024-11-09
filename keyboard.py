import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Radio Button Example")

# Create an IntVar to store the selected option
selected_option = tk.IntVar()
# selected_option.set(1)  # Set a default value

# Create radio buttons linked to the IntVar
radio1 = tk.Radiobutton(root, text="Option 1", variable=selected_option, value=1)
radio1.pack()

radio2 = tk.Radiobutton(root, text="Option 2", variable=selected_option, value=2)
radio2.pack()

radio3 = tk.Radiobutton(root, text="Option 3", variable=selected_option, value=3)
radio3.pack()

# Function to display the selected option
def show_selection():
    print("Selected option:", selected_option.get())

# Function to handle keyboard input and update selected_option
def select_option_by_key(event):
    if event.char.isdigit():  # Check if the key pressed is a digit
        num = int(event.char)
        if num in [1, 2, 3]:  # Ensure the digit corresponds to an available option
            selected_option.set(num)
            # print(f"Option {num} selected by pressing {num}")

# Bind key events to the main window
root.bind('<Key>', select_option_by_key)

# Button to trigger the function and print the selected option
show_button = tk.Button(root, text="Show Selection", command=show_selection)
show_button.pack()

# Run the Tkinter event loop
root.mainloop()

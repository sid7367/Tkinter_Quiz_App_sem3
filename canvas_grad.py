import tkinter as tk

def create_gradient(canvas, color1, color2):
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()

    for i in range(height):
        ratio = i / height
        red = int(ratio * int(color2[1:3], 16) + (1 - ratio) * int(color1[1:3], 16))
        green = int(ratio * int(color2[3:5], 16) + (1 - ratio) * int(color1[3:5], 16))
        blue = int(ratio * int(color2[5:7], 16) + (1 - ratio) * int(color1[5:7], 16))
        color = f"#{red:02x}{green:02x}{blue:02x}"
        canvas.create_line(0, i, width, i, fill=color)

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Create a vertical gradient from blue to green
create_gradient(canvas, "#0000ff", "#00ff00")

root.mainloop()

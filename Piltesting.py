#creating a gradient image using PIL 👇
from tkinter import Tk, Label
from PIL import Image, ImageTk
from PIL import ImageDraw

# def create_gradient_image(width, height, color1, color2):
#     image = Image.new("RGB", (width, height))
#     for y in range(height):
#         ratio = y / height
#         r = int(ratio * color2[0] + (1 - ratio) * color1[0])
#         g = int(ratio * color2[1] + (1 - ratio) * color1[1])
#         b = int(ratio * color2[2] + (1 - ratio) * color1[2])
#         for x in range(width):
#             image.putpixel((x, y), (r, g, b))
#     return image

# root = Tk()
# width, height = 400, 300
# gradient_image = create_gradient_image(width, height, (0, 0, 255), (0, 255, 0))  # Blue to green
# photo = ImageTk.PhotoImage(gradient_image)

# label = Label(root, image=photo)
# label.pack()

# root.mainloop()

#opening using PIL
# from PIL import Image

# # Open an image file
# image = Image.open("example.jpg")

# # Display the image
# image.show()

# Create a new image with RGB mode, width of 200, height of 100, and white background
# new_image = Image.new("RGB", (200, 100), "white")
# new_image.show()


# Create a new image
image = Image.new("RGB", (300, 200), "lightblue")
draw = ImageDraw.Draw(image)

# Draw a rectangle and a line
draw.rectangle([50, 50, 250, 150], outline="black", fill="white")
draw.line([0, 0, 300, 200], fill="red", width=3)

# Add text
draw.text((100, 75), "Hello, Pillow!", fill="black")

image.show()
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

# Load the images
image1 = Image.open("images/light_mode.png")
image2 = Image.open("images/dark_mode.png")

# Create Tkinter PhotoImage objects for the images
image1_tk = ImageTk.PhotoImage(image1)
image2_tk = ImageTk.PhotoImage(image2)

# Add the images to the canvas
canvas.create_image(100, 100, image=image1_tk)
canvas.create_image(300, 300, image=image2_tk)

root.mainloop()

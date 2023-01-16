import tkinter as tk
import customtkinter
from PIL import Image

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")

def press():
    button.configure(attribute = my_image)

my_image = customtkinter.CTkImage(light_image=Image.open('images/light_mode.png'),
                                  dark_image=Image.open('images/dark_mode.png'),
                                  size=(30, 30))

# my_image = customtkinter.CTkImage(light_image=)                                  

button = customtkinter.CTkButton(app, image=my_image, text="", command=press)
button.pack()

app.mainloop()

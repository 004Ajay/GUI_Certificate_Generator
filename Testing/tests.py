import random, tkinter as tk
from tkinter import PhotoImage, filedialog, messagebox as mb
from PIL import Image, ImageTk
from PIL.Image import Resampling
from auto22 import generate

"""
to do:
finalize location of coordinates
"""
headFont = ('Montserrat-semibold', 25)
normalFont = ('Montserrat', 12)

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        dark_mode = PhotoImage(file='images/dark_mode.png') # get image using PhotoImage function
        dark_mode_img_lbl = tk.Label(image=dark_mode) # label for button event

        self.title("Certifly")
        # self.iconbitmap('') # place certifly icon image here.................................................................................................
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}") # "1920x1080"
        self.state('zoomed')

        self.dark_mode_button = tk.Button(self, image=dark_mode_img_lbl) # command=dark_mode_switch
        self.dark_mode_button.pack(side='right')
app = App()
app.mainloop()  
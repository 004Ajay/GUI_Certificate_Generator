import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from auto_copy import generate

class App(tk.Tk):

    def exit_window(e): app.destroy() # to exit window 

    def __init__(self):
        super().__init__()
        self.title("Image Viewer")

        # self.geometry('1920x1080')
        self.bind("<Escape>", self.close_window)

        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}") # "1920x1080"
        self.state('zoomed')

        self.crosshair_id = None

        # Create a button to open an image file
        self.open_button = tk.Button(self, text="Open Image", command=self.open_image)
        self.open_button.pack()

        # Create a frame to hold the canvas and scrollbars
        self.frame = tk.Frame(self)
        self.frame.pack()

        # Create a canvas to display the image
        self.canvas = tk.Canvas(self.frame, width=1280, height=904, bg='white', bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Create a vertical scrollbar for the canvas
        self.v_scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        # Create a horizontal scrollbar for the canvas
        self.h_scrollbar = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Create a label to show the coordinates of the point clicked
        self.coord_label = tk.Label(self, text="X: Y:")
        self.coord_label.pack()

    def close_window(self, event=None): self.destroy() # to exit the window

    def open_image(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        self.image = Image.open(filepath)
        self.photo = ImageTk.PhotoImage(self.image)
        
        # Create the image on the canvas
        self.img_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(self.img_on_canvas))
        self.canvas.bind("<Button-1>", self.show_coordinates)

        self.canvas.bind("<Enter>", self.change_cursor)
        self.canvas.bind("<Leave>", self.reset_cursor)

    def show_coordinates(self, event):
        x = event.x
        y = event.y
        self.coord_label.config(text="X: {} Y: {}".format(x, y))
        print(x,y)
        generate(x,y)

    def change_cursor(self, event):
        self.canvas.config(cursor="crosshair")

    def reset_cursor(self, event):
        self.canvas.config(cursor="")     


app = App()

app.mainloop()
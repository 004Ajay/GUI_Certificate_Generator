import tkinter as tk
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Certifly")
        # self.iconbitmap('') # place certifly icon image here.

        self.bind("<Escape>", self.exit_window) # press 'escape' to exit the window

        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}") # "1920x1080"
        self.state('zoomed')

        # Setting title & tagline
        self.title = tk.Label(self, text='CERTIFLY', font=('Montserrat-semibold', 25))
        self.tagline = tk.Label(self, text='Certificates on the Go', font=('Montserrat', 15))
        self.title.pack()
        self.tagline.pack()

        # for getting names from user
        self.name_entry = tk.Text(self, width=20, height=10,font=('Montserrat', 12), wrap='word')
        self.name_entry.pack(padx=30,pady=100, side="left",anchor="n")

        # Create button to enter the names
        self.name_button = tk.Button(self, text="Enter names", command=self.enter_names)
        self.name_button.pack(padx=10,pady=200, side="left")

        # Create a button to open an image file
        self.open_button = tk.Button(self, text="Open Image", command=self.open_image)
        self.open_button.pack()

        # Create a canvas Frame to hold the canvas and scrollbars
        self.canvasFrame = tk.Frame(self)
        self.canvasFrame.pack()

        # Create a canvas to display the image
        self.canvas = tk.Canvas(self.canvasFrame, width=900, height=650, bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Create a vertical scrollbar for the canvas
        self.v_scrollbar = tk.Scrollbar(self.canvasFrame, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.v_scrollbar.config(width=20) # increasing size of scroll bar
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        # Create a horizontal scrollbar for the canvas
        self.h_scrollbar = tk.Scrollbar(self.canvasFrame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.h_scrollbar.config(width=20) # increasing size of scroll bar
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Create a label to show the coordinates of the point clicked
        self.coord_label = tk.Label(self, text="X: Y:")
        self.coord_label.pack()

    def enter_names(self):
        names = self.name_entry.get("1.0","end").upper() # getting texts from start to end & changing to uppercase
        names_list = names.splitlines() # splitting texts by line 
        print(names_list)

    def open_image(self):
        try:
            filepath = filedialog.askopenfilename()
            self.image = Image.open(filepath)
            self.photo = ImageTk.PhotoImage(self.image)
        except:
            mb.showerror('Error', 'Please select an image')
        
        # Create the image on the canvas
        self.img_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(self.img_on_canvas))

        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Shift-MouseWheel>", self.on_shift_mousewheel)

        self.canvas.bind("<Button-1>", self.show_coordinates) # to get coordinates on mouse click 
        self.canvas.bind("<Enter>", self.change_cursor)
        self.canvas.bind("<Leave>", self.reset_cursor)

    def show_coordinates(self, event):
        x = event.x
        y = event.y
        self.coord_label.config(text="X: {} Y: {}".format(x, y))
        print(x,y) # remove at last ................................................................................................

    def on_shift_mousewheel(self, event): # for scrolling left-right using shift + (mousewheel or trackpad)
        pixels_per_unit = 50
        units_to_scroll = int(event.delta / pixels_per_unit)
        self.canvas.xview_scroll(-1*units_to_scroll, "units")     

    def on_mousewheel(self, event): # for scrolling up-down using mousewheel or trackpad
        pixels_per_unit = 50
        units_to_scroll = int(event.delta / pixels_per_unit)
        self.canvas.yview_scroll(-1*units_to_scroll, "units")  

    def change_cursor(self, event): self.canvas.config(cursor="crosshair")  # to change normal cursor to crosshair(+)
    def reset_cursor(self, event): self.canvas.config(cursor="")            # when cursor is hovered over placed image

    def exit_window(self, event=None): self.destroy() # to exit the window    

app = App()
app.mainloop()
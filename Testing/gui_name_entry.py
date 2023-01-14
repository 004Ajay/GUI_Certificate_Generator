import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk


# test the cordinates setting on left side scrollbar and on right side too, there
# may be amistake of cordinates..if so, delete all scrolls and related things
# set canvas size to normal certificate size


headFont = 'Montserrat-semibold', 25
normalFont = 'Montserrat', 12

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.bind("<Escape>", self.exit_window) # press 'escape' to exit the window

        self.title("Certifly")
        # self.iconbitmap('') # place certifly icon image here.
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}") # "1920x1080"
        self.state('zoomed')

        # Setting title & tagline
        self.title = tk.Label(self, text='CERTIFLY', font=headFont)
        self.tagline = tk.Label(self, text='Certificates on the Go', font=normalFont)
        self.title.pack()
        self.tagline.pack()

        # Create a canvas Frame to hold the name textbox and buttons
        self.sideFrame = tk.Frame(self)#, width=20, height=100)
        self.sideFrame.pack(side='left')
        # self.sideFrame.config(bg='#FEC868') # remove at last ................................................................................................
        
        self.name_entry_title = tk.Label(self.sideFrame, text='Enter names to be printed', font=normalFont)
        self.name_entry_title.pack(padx=30, pady=10, anchor='center')

        self.name_entry = tk.Text(self.sideFrame, width=20, height=10, font=normalFont, wrap='word') # for getting names from user
        self.name_entry.pack(padx=30, pady=10, anchor='center')

        self.name_button = tk.Button(self.sideFrame, text="Enter names", font=normalFont, command=self.enter_names) # button to enter the names
        self.name_button.pack(padx=30, pady=10, anchor='center')

        self.open_button = tk.Button(self.sideFrame, text="Open Image", font=normalFont, command=self.open_image) #  button to open an image file
        self.open_button.pack(padx=30, pady=10, anchor='center')

        self.generate_sample = tk.Button(self.sideFrame, text="Generate Sample", font=normalFont, command=self.generate_sample) #  button to open an image file
        self.generate_sample.pack(padx=30, pady=10, anchor='center')

        self.generate_all = tk.Button(self.sideFrame, text="Generate All",font=normalFont, command=self.generate_all) #  button to open an image file
        self.generate_all.pack(padx=30, pady=10, anchor='center')

        # Create a canvas Frame to hold the canvas and scrollbars for opened image
        self.canvasFrame = tk.Frame(self)
        self.canvasFrame.pack()
        self.canvasFrame.config(bg='#FDA769') # remove at last ................................................................................................

        self.canvas = tk.Canvas(self.canvasFrame, width=900, height=650, bd=0, highlightthickness=0) # canvas to display the image #1280, 904
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scrollbar = tk.Scrollbar(self.canvasFrame, orient="vertical", command=self.canvas.yview) # vertical scrollbar for the canvas
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.v_scrollbar.config(width=20) # increasing the width of scroll bar
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.h_scrollbar = tk.Scrollbar(self.canvasFrame, orient="horizontal", command=self.canvas.xview) # horizontal scrollbar for the canvas
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.h_scrollbar.config(width=20) # increasing the width of scroll bar
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        self.coord_label = tk.Label(self, text="X: Y:") # label to show the coordinates of the point clicked
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

            # Create the image on the canvas
            self.img_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            self.canvas.config(scrollregion=self.canvas.bbox(self.img_on_canvas))

        except:
            mb.showerror('Error', 'Please select an image')
        
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Shift-MouseWheel>", self.on_shift_mousewheel)

        self.canvas.bind("<Button-1>", self.show_coordinates) # to get coordinates on mouse click 
        self.canvas.bind("<Enter>", self.change_cursor)
        self.canvas.bind("<Leave>", self.reset_cursor)

        # Separator object
        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.config(width=2)
        self.separator.grid(column=1)#, relwidth=0.2, relheight=1)

    def show_coordinates(self, event):
        x = event.x
        y = event.y
        self.coord_label.config(text="X: {} Y: {}".format(x, y))
        print(x,y) # remove at last ................................................................................................

    def generate_sample(self):
        print('generate_sample')

    def generate_all(self):
        print('generate_all')

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
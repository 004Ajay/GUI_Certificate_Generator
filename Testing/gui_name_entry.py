import random
import tkinter as tk
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk

"""
to do:

define generate functions
add os lib
finalize location of coordinates
delete unwated comments

"""
# test the cordinates setting on left side scrollbar and on right side too, there
# may be amistake of cordinates..if so, delete all scrolls and related things
# set canvas size to normal certificate size


headFont = ('Montserrat-semibold', 25)
normalFont = ('Montserrat', 12)

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
        self.sideFrame.config(bg='#FEC868') # remove at last ................................................................................................
        
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

        self.coord_label = tk.Label(self.sideFrame, text="X: Y:",font=normalFont) # label to show the coordinates of the point clicked
        self.coord_label.pack(padx=30, pady=30, anchor='center')

        # Create a canvas Frame to hold the canvas and scrollbars for opened image
        self.canvasFrame = tk.LabelFrame(self)
        self.canvasFrame.pack(side="right", padx=50)
        # self.canvasFrame.config(bg='#FDA769') # remove at last ................................................................................................

        self.canvas = tk.Canvas(self.canvasFrame, width=1000, height=650, bd=0, highlightthickness=0) # canvas to display the image #1280, 904
        self.canvas.grid(row=0, column=0, sticky="nsew")

        """self.v_scrollbar = tk.Scrollbar(self.canvasFrame, orient="vertical", command=self.canvas.yview) # vertical scrollbar for the canvas
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.v_scrollbar.config(width=20) # increasing the width of scroll bar
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.h_scrollbar = tk.Scrollbar(self.canvasFrame, orient="horizontal", command=self.canvas.xview) # horizontal scrollbar for the canvas
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.h_scrollbar.config(width=20) # increasing the width of scroll bar
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)"""


    def enter_names(self):
        global name_list
        names = self.name_entry.get("1.0","end").upper() # getting texts from start to end & changing to uppercase
        name_list = names.splitlines() # splitting texts by line 
        print(name_list)

    def open_image(self):
        try:
            filepath = filedialog.askopenfilename()
            self.image = Image.open(filepath)

            width, height = 1000, 650
            self.ratio = min(width/self.image.width, height/self.image.height)
            self.image = self.image.resize((int(self.image.width*self.ratio), int(self.image.height*self.ratio)), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(self.image)
            self.img_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            self.canvas.bind("<Button-1>", self.show_coordinates)

            """self.image.thumbnail((self.winfo_width(), self.winfo_height()))
            self.photo = ImageTk.PhotoImage(self.image)
            self.img_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")"""

            """# Scale the image down to fit the window
            width, height = self.image.size
            ratio = min(600/width, 400/height)
            self.image = self.image.resize((int(width*ratio), int(height*ratio)))
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            self.canvas.bind("<Button-1>", self.show_coordinates)"""

            # self.photo = ImageTk.PhotoImage(self.image)

            # Create the image on the canvas
            # self.img_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            # self.canvas.config(scrollregion=self.canvas.bbox(self.img_on_canvas))

        except:
            mb.showerror('Error', 'Please select an image')
        
        """self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Shift-MouseWheel>", self.on_shift_mousewheel)"""

        self.canvas.bind("<Button-1>", self.show_coordinates) # to get coordinates on mouse click 
        self.canvas.bind("<Enter>", self.change_cursor)
        self.canvas.bind("<Leave>", self.reset_cursor)

    def show_coordinates(self, event):
        """x = event.x
        y = event.y
        self.coord_label.config(text="X: {} Y: {}".format(x, y))"""
        x = round((event.x/self.ratio), 2)
        y = round((event.y/self.ratio), 2)
        self.coord_label.config(text=f"X: {x}, Y: {y}")

        print(f"X: {x}, Y: {y}") # remove at last ................................................................................................

    def generate_sample(self):
        os.mkdir()
        chosen_names = []
        for i in range(2):
            chosen_names.append(random.choice(name_list))

        for name in chosen_names:  
            print("Generating " + name + ".png")

            img = Image.open("ctf.png") # Loading the certificate template
            draw = ImageDraw.Draw(img)
            # w, h = draw.textsize(name, font=font)

            name_x, name_y = 639.75, 468.69 # Setting the co-ordinates to where the names should be entered
            draw.text((name_x, name_y), name, fill="black")

            img.save(r'generated_certificates/' + name + ".png") # Saving the images to the generated_certificates directory    

            # print('generate_sample')

    def generate_all(self):
        print('generate_all')

    """def on_shift_mousewheel(self, event): # for scrolling left-right using shift + (mousewheel or trackpad)
        pixels_per_unit = 50
        units_to_scroll = int(event.delta / pixels_per_unit)
        self.canvas.xview_scroll(-1*units_to_scroll, "units")     

    def on_mousewheel(self, event): # for scrolling up-down using mousewheel or trackpad
        pixels_per_unit = 50
        units_to_scroll = int(event.delta / pixels_per_unit)
        self.canvas.yview_scroll(-1*units_to_scroll, "units")  """

    def change_cursor(self, event): self.canvas.config(cursor="crosshair")  # to change normal cursor to crosshair(+)
    def reset_cursor(self, event): self.canvas.config(cursor="")            # when cursor is hovered over placed image

    def exit_window(self, event=None): self.destroy() # to exit the window    

app = App()
app.mainloop()
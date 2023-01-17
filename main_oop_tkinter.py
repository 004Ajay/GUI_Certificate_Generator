import random, tkinter as tk
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk, ImageFont
from PIL.Image import Resampling
from write_certificate import generate

headFont = ('fonts/Montserrat-SemiBold.ttf', 25)
normalFont = ('fonts/Montserrat-Regular.ttf', 12)

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.bind("<Escape>", self.exit_window) # press 'escape' to exit the window
        self.dark_mode = Image.open('images/dark_mode.png')
        self.dark_mode_img = ImageTk.PhotoImage(self.dark_mode)    

        self.title("Certifly")
        self.iconbitmap('images/icon.ico') # certifly window icon
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}") # "1920x1080"
        self.state('zoomed')
        self.title = tk.Label(self, text='CERTIFLY', font=headFont) # Setting title & tagline
        self.tagline = tk.Label(self, text='Certificates on the Go', font=normalFont)
        self.dark_mode_button = tk.Button(self, image=self.dark_mode_img, height=30, width=30, bg='White') # command=dark_mode_switch) # dark_mode button
        
        self.title.pack()
        self.tagline.pack()
        self.dark_mode_button.pack(side='right', anchor='ne', padx=30)

        # Create a canvas Frame to hold the name textbox and buttons
        self.sideFrame = tk.LabelFrame(self)#, width=20, height=100)
        self.sideFrame.pack(side='left', padx=20)
        
        ########## making widgets ##########
        self.name_entry_title = tk.Label(self.sideFrame, text='Enter names to be printed', font=normalFont)
        self.name_entry = tk.Text(self.sideFrame, width=20, height=10, font=normalFont, wrap='word') # for getting names from user
        self.name_button = tk.Button(self.sideFrame, text="Enter names", font=normalFont, command=self.enter_names) # button to enter the names
        self.open_button = tk.Button(self.sideFrame, text="Open Image", font=normalFont, command=self.open_image) #  button to open an image file
        self.gen_sample_button = tk.Button(self.sideFrame, text="Generate Sample", font=normalFont, command=self.generate_sample) #  button to open an image file
        self.gen_all_button = tk.Button(self.sideFrame, text="Generate All",font=normalFont, command=self.generate_all) #  button to open an image file
        self.coord_label = tk.Label(self.sideFrame, text="X: Y:",font=normalFont) # label to show the coordinates of the point clicked
        self.info_label = tk.Label(self.sideFrame, text='',font=normalFont, fg='green') # label to show info about button clicks & all
        ########## placing widgets ##########
        self.name_entry_title.pack(padx=30, pady=10, anchor='center')
        self.name_entry.pack(padx=30, pady=5, anchor='center')
        self.name_button.pack(padx=30, pady=10, anchor='center')
        self.open_button.pack(padx=30, pady=10, anchor='center')
        self.gen_sample_button.pack(padx=30, pady=10, anchor='center')
        self.gen_all_button.pack(padx=30, pady=10, anchor='center')
        self.coord_label.pack(padx=30, pady=20, anchor='center')
        self.info_label.pack(padx=30, pady=20, anchor='center')

        # Create a canvas Frame to hold the canvas and scrollbars for opened image
        self.canvasFrame = tk.LabelFrame(self)
        self.canvasFrame.pack(side="right", padx=50)
        self.canvas = tk.Canvas(self.canvasFrame, width=910, height=650, bd=0, highlightthickness=0) # canvas to display the image #1280, 904
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def enter_names(self):
        global name_list # for checking in generate_sample() function
        names = self.name_entry.get("1.0","end").upper() # getting texts from start to end & changing to uppercase
        name_list = names.splitlines() # splitting texts by line
        self.info_label.config(text='Names Entered')
        self.after(5000, self.clear_label)

    def open_image(self):
        if len(self.name_entry.get("1.0","end")) == 1: # chcecking if text box is empty
            mb.showerror('Name error', 'Please add some names')
        else:
            try:
                filepath = filedialog.askopenfilename()
                self.image = Image.open(filepath)
                width, height = 1000, 650
                self.ratio = min(width/self.image.width, height/self.image.height) # problem here===============================================================
                self.image = self.image.resize((int(self.image.width*self.ratio), int(self.image.height*self.ratio)), Resampling.BILINEAR)
                self.photo = ImageTk.PhotoImage(self.image)
                self.img_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
                self.canvas.bind("<Button-1>", self.show_coordinates)
            except:
                mb.showerror('Error', 'Please select an image')

            self.canvas.bind("<Button-1>", self.show_coordinates) # to get coordinates on mouse click 
            self.canvas.bind("<Enter>", self.change_cursor) # to change cursor icon to crosshair (+)
            self.canvas.bind("<Leave>", self.reset_cursor)

    global x, y # for checking in generate functions
    x = y = None
    def show_coordinates(self, event):
        global x, y # for changing gobal values of x & y
        x = event.x/self.ratio 
        y = event.y/self.ratio
        self.coord_label.config(text=f"X: {round(x,2)}, Y: {round(y,2)}")
        self.info_label.config(text='Coordinates Set')
        self.after(5000, self.clear_label)

    def generate_sample(self):
        sample_names = []
        if len(name_list) == 0:
            mb.showerror('Add name list', 'Please add some names')
        elif x is None: # no check for 'y' as it is selected with 'x'
            mb.showerror('Coordinates error', 'Please select coordinates')
        else:
            for _ in range(2):
                sample_names.append(random.choice(name_list))
            generate(sample_names, x, y)
            mb.showinfo('Cerificates Generated', 'Sample cerificates has been generated')

    def generate_all(self):
        if x is None: # no check for 'y' as it is selected with 'x'
            mb.showerror('Coordinates error', 'Please select coordinates')
        else:
            generate(name_list, x, y) # generating certificates with all given names
            mb.showinfo('Cerificates Generated', 'All cerificates has been generated')

    def change_cursor(self, event): self.canvas.config(cursor="crosshair")  # to change normal cursor to crosshair(+)
    def reset_cursor(self, event): self.canvas.config(cursor="")            # when cursor is hovered over placed image
    def clear_label(self): self.info_label['text'] = "" # to remove text from info label
    def exit_window(self, event=None): self.destroy() # to exit the window

app = App()
app.mainloop()
import os, random
import customtkinter as ctk
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL.Image import Resampling

headFont = ('fonts/Montserrat-SemiBold.ttf', 35)
normalFont = ('fonts/Montserrat-Regular.ttf', 17)
writerFont = ImageFont.truetype('fonts/Poppins-Medium.ttf', 40)

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark. Window theme
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green, used for default button colors & other 

def folder_check(): # Creates a new 'generated_certificates' folder if not already present
    if os.path.isdir("generated_certificates"): 
        os.system("rmdir /s /q generated_certificates") # not recommended to use 
        os.mkdir("generated_certificates")
    else:
        os.mkdir("generated_certificates")

names = []
def generate(names, x, y):
    folder_check()
    for name in names:
        img = Image.open(filepath) # Loading the certificate template
        draw = ImageDraw.Draw(img)
        name_x, name_y = x, y # Setting the co-ordinates to where the names should be entered
        draw.text((name_x, name_y), name, font=writerFont, fill="black")      
        img.save(r'generated_certificates/' + name + ".png") # Saving the images to the generated_certificates directory
            
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.bind("<Escape>", self.exit_window) # press 'escape' to exit the window
        self.dark_mode = Image.open('images/dark_mode.png')
        self.dark_mode_img = ctk.CTkImage(self.dark_mode, size=(30, 30))
        self.light_mode = Image.open('images/light_mode.png')
        self.light_mode_img = ctk.CTkImage(self.light_mode, size=(30, 30))

        self.title("Certifly")
        self.iconbitmap('images/icon.ico') # certifly window icon
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}") # getting user's screen size
        self.state('zoomed')
        self.title = ctk.CTkLabel(self, text='CERTIFLY', font=headFont) # Setting title
        self.tagline = ctk.CTkLabel(self, text='Certificates on the Go', font=normalFont) # Setting tagline
        self.mode_switch_button = ctk.CTkButton(self, image=self.light_mode_img, text="", height=20, width=20, corner_radius=50, fg_color="transparent", command=self.mode_switcher)
        
        self.title.pack()
        self.tagline.pack()
        self.mode_switch_button.pack(side='right', anchor='ne', padx=30)

        # Creating Frame to hold the name textbox and buttons
        self.sideFrame = ctk.CTkFrame(self)#, width=20, height=100)
        self.sideFrame.pack(side='left', padx=20)
        ########## making widgets ##########
        self.name_entry_title = ctk.CTkLabel(self.sideFrame, text='Enter names to be printed', font=normalFont)
        self.name_entry = ctk.CTkTextbox(self.sideFrame, width=170, height=120, font=normalFont, wrap='word') # for getting names from user
        self.name_button = ctk.CTkButton(self.sideFrame, text="Enter names", font=normalFont, corner_radius=40, command=self.enter_names) # button to enter the names
        self.open_button = ctk.CTkButton(self.sideFrame, text="Open Image", font=normalFont, corner_radius=40, command=self.open_image) #  button to open an image file
        self.gen_sample_button = ctk.CTkButton(self.sideFrame, text="Generate Sample", font=normalFont, corner_radius=40, command=self.generate_sample) #  button to open an image file
        self.gen_all_button = ctk.CTkButton(self.sideFrame, text="Generate All",font=normalFont, corner_radius=40, command=self.generate_all) #  button to open an image file
        self.coord_label = ctk.CTkLabel(self.sideFrame, text="X: Y:",font=normalFont) # label to show the coordinates of the point clicked
        self.info_label = ctk.CTkLabel(self.sideFrame, text='',font=normalFont, text_color='green') # label to show info about button clicks & all
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
        self.canvasFrame = ctk.CTkFrame(self)
        self.canvasFrame.pack(side="right", padx=50)
        self.canvas = ctk.CTkCanvas(self.canvasFrame, width=910, height=650, highlightthickness=0) # canvas to display the image #1280, 904
        self.canvas.grid(row=0, column=0, sticky="nsew")

    global name_list
    name_list = []
    def enter_names(self):
        global name_list # for checking in generate_sample() function
        names = self.name_entry.get("1.0","end").upper() # getting texts from start to end & changing to uppercase
        name_list = names.splitlines() # splitting texts by line
        self.info_label.configure(text='Names Entered')
        self.after(5000, self.clear_label)    

    def open_image(self):
        if len(self.name_entry.get("1.0","end")) == 1: # chcecking if text box is empty
            mb.showerror('Name error', 'Please add some names')
        else:
            try:
                global filepath
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
        self.coord_label.configure(text=f"X: {round(x,2)}, Y: {round(y,2)}")
        self.info_label.configure(text='Coordinates Set')
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
        if len(name_list) == 0:
            mb.showerror('Add name list', 'Please add some names')
        if x is None: # no check for 'y' as it is selected with 'x'
            mb.showerror('Coordinates error', 'Please select coordinates')
        else:
            generate(name_list, x, y) # generating certificates with all given names
            mb.showinfo('Cerificates Generated', 'All cerificates has been generated')

    global is_dark
    is_dark = False # initializing the variable

    def mode_switcher(self):
        global is_dark
        is_dark = not is_dark # toggle the value of is_dark
        if is_dark:
            ctk.set_appearance_mode("light")
            self.mode_switch_button.configure(image=self.dark_mode_img)
        else:
            ctk.set_appearance_mode("dark")  # Modes: system, light, dark 
            self.mode_switch_button.configure(image=self.light_mode_img)
            
    def change_cursor(self, event): self.canvas.configure(cursor="crosshair")  # to change normal cursor to crosshair(+)
    def reset_cursor(self, event): self.canvas.configure(cursor="")            # when cursor is hovered over placed image
    def clear_label(self): self.info_label['text'] = "" # to remove text from info label
    def exit_window(self, event=None): self.destroy() # to exit the window

app = App()
app.mainloop()
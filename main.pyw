import os, subprocess, random, customtkinter as ctk
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL.Image import Resampling

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark. ### Window theme
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green. ### Used for default button colors & other

normalFont = ('fonts/Montserrat-Regular.ttf', 17) # used many times for buttons, small headings etc...

def open_folder():
    if os.path.isdir("generated_certificates"):
        os.startfile('generated_certificates')

def folder_check(): # Creates a new 'generated_certificates' folder if not already present
    if os.path.isdir("generated_certificates"): 
        os.system("rmdir /s /q generated_certificates") # not recommended to use 
        os.mkdir("generated_certificates")
    else:
        os.mkdir("generated_certificates")

def generate(names, x, y):
    folder_check()
    for name in names:
        img = Image.open(filepath) # loading the selected certificate template
        draw = ImageDraw.Draw(img)
        draw.text((x, y), name, font=ImageFont.truetype('fonts/Poppins-Medium.ttf', 40), fill="black") # setting the co-ordinates to draw the names     
        img.save(r'generated_certificates/' + name + ".png") # saving the images to the generated_certificates directory   
            
class App(ctk.CTk): ####### ↓↓↓ Main Window or Root ↓↓↓ #######
    def __init__(self):
        super().__init__()
        self.title("Certifly")
        self.iconbitmap('images/icon.ico') # certifly window icon
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}") # getting user's screen size
        self.state('zoomed')
        self.title = ctk.CTkLabel(self, text='CERTIFLY', font=('fonts/Montserrat-Bold.ttf', 50)) # Setting title
        self.tagline = ctk.CTkLabel(self, text='Certificates on the Go', font=normalFont) # Setting tagline
        self.bind("<Escape>", self.exit_window) # press 'escape' to exit the window
        self.dark_mode_img = ctk.CTkImage(Image.open('images/dark_mode.png'), size=(30, 30))
        self.light_mode_img = ctk.CTkImage(Image.open('images/light_mode.png'), size=(30, 30))
        self.mode_switch_button = ctk.CTkButton(self, image=self.light_mode_img, text="", height=20, width=20, corner_radius=50, fg_color="transparent", command=self.mode_switcher)
        self.title.pack() ####### ↓↓↓ placing title, tagline & mode switcher ↓↓↓ ####### 
        self.tagline.pack()
        self.mode_switch_button.pack(side='right', anchor='ne', padx=30)
        self.sideFrame = ctk.CTkFrame(self) ####### ↓↓↓ Frame to hold the name textbox and related buttons ↓↓↓ #######
        self.sideFrame.pack(side='left', padx=20)
        self.name_entry_title = ctk.CTkLabel(self.sideFrame, text='Enter names to be printed', font=normalFont) ####### ↓↓↓ making widgets ↓↓↓ #######
        self.name_entry = ctk.CTkTextbox(self.sideFrame, width=170, height=120, font=normalFont, wrap='word') # for getting names from user
        self.name_button = ctk.CTkButton(self.sideFrame, text="Enter names", font=normalFont, corner_radius=40, command=self.enter_names) # button to enter the names
        self.open_button = ctk.CTkButton(self.sideFrame, text="Open Image", font=normalFont, corner_radius=40, command=self.open_image) #  button to open an image file
        self.gen_sample_button = ctk.CTkButton(self.sideFrame, text="Generate Sample", font=normalFont, corner_radius=40, command=self.generate_sample) #  button to open an image file
        self.gen_all_button = ctk.CTkButton(self.sideFrame, text="Generate All",font=normalFont, corner_radius=40, command=self.generate_all) #  button to open an image file
        self.coord_label = ctk.CTkLabel(self.sideFrame, text="X: Y:",font=normalFont) # label to show the coordinates of the point clicked
        self.info_label = ctk.CTkLabel(self.sideFrame, text='',font=normalFont, text_color='green') # label to show info about button clicks & all
        self.name_entry_title.pack(padx=30, pady=10, anchor='center') ####### ↓↓↓ placing widgets ↓↓↓ #######
        self.name_entry.pack(padx=30, pady=5, anchor='center')
        self.name_button.pack(padx=30, pady=10, anchor='center')
        self.open_button.pack(padx=30, pady=10, anchor='center')
        self.gen_sample_button.pack(padx=30, pady=10, anchor='center')
        self.gen_all_button.pack(padx=30, pady=10, anchor='center')
        self.coord_label.pack(padx=30, pady=20, anchor='center')
        self.info_label.pack(padx=30, pady=20, anchor='center')
        self.canvasFrame = ctk.CTkFrame(self) ####### ↓↓↓ Frame to hold canvas and dragging & opened image ↓↓↓ #######
        self.canvasFrame.pack(side="right", padx=50)
        self.canvas = ctk.CTkCanvas(self.canvasFrame, width=910, height=650) # canvas to display dragging & opened image
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def non_empty_textbox(self):    
        if len(self.name_entry.get("1.0","end")) == 1: # checking if text box is empty, 1 denotes a (end-of-line(EOL), newline character, invisible character) 
            mb.showerror('Name error', 'Please add some names')
        else: return True    

    global name_list
    name_list = []
    def enter_names(self):
        if self.non_empty_textbox():       
            global name_list
            names = self.name_entry.get("1.0","end").upper() # getting all texts from textbox & changing to uppercase
            name_list = names.splitlines() # splitting texts by line
            self.info_label.configure(text='Names Entered')
            self.after(3000, self.clear_label)  
            
    def open_image(self):
        if self.non_empty_textbox():
            try:
                global filepath # for accessing the selected image on generate() function
                filepath = filedialog.askopenfilename()
                self.image = Image.open(filepath)
                width, height = 1000, 650
                self.ratio = min(width/self.image.width, height/self.image.height)
                self.image = self.image.resize((int(self.image.width*self.ratio), int(self.image.height*self.ratio)), Resampling.BILINEAR)
                self.photo = ImageTk.PhotoImage(self.image)
                self.img_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
                self.sample_name_image = ImageTk.PhotoImage(Image.open("images/name.png")) ####### ↓↓↓ dragging name box ↓↓↓ #######
                self.drag_image = self.canvas.create_image(100, 100, image=self.sample_name_image, anchor="nw")   
                self.canvas.configure(scrollregion=self.canvas.bbox(self.drag_image))
            except:
                mb.showerror('Error', 'Please select an image') 
            self.canvas.tag_bind(self.drag_image,"<Button1-Motion>", self.move, add="+") ####### ↓↓↓ key binds ↓↓↓ #######
            self.canvas.bind("<Button-3>", self.scan)
            self.canvas.bind("<Button3-Motion>", self.drag)
            self.canvas.tag_bind(self.drag_image, "<Button1-Motion>", self.show_coordinates, add="+")

    global x, y # for checking in generate functions
    x = y = None
    def show_coordinates(self, event):
        global x, y # for changing global values of x & y
        x = event.x/self.ratio 
        y = event.y/self.ratio
        self.coord_label.configure(text=f"X: {round(x,2)}, Y: {round(y,2)}")

    def gen_err_check(self):
        if len(name_list) == 0:
            mb.showerror('Name error', 'Please add some names')
        elif x is None: # no check for 'y' as it is selected with 'x'
            mb.showerror('Coordinates error', "Drag & place 'Sample Name' to set coordinates")
        else: return True    

    def generate_sample(self):
        sample_names = []
        if self.gen_err_check():
            try:                
                sample_names = [random.choice(name_list) for _ in range(2)] # list comprehension
                generate(sample_names, x, y)
                mb.showinfo('Cerificates Generated', 'Sample cerificates has been generated')
                open_folder()
            except: mb.showerror('Error', 'Unknown error occured')

    def generate_all(self):
        if self.gen_err_check():
            try:
                generate(name_list, x, y)
                mb.showinfo('Cerificates Generated', 'All cerificates has been generated')
                open_folder()
            except: mb.showerror('Error', 'Unknown error occured')
                
    global is_dark
    is_dark = False # initializing the variable
    def mode_switcher(self):
        global is_dark
        is_dark = not is_dark # toggle the value of is_dark
        if is_dark:
            ctk.set_appearance_mode("light")
            self.mode_switch_button.configure(image=self.dark_mode_img)
            self.canvas.configure(bg='#dbdbdb')
        else:
            ctk.set_appearance_mode("dark")  # Modes: system, light, dark 
            self.mode_switch_button.configure(image=self.light_mode_img)

    def move(self, event): self.canvas.moveto(self.drag_image,event.x-103,event.y)
    def scan(self, event): self.canvas.scan_mark(event.x, event.y)
    def drag(self, event): self.canvas.scan_dragto(event.x, event.y, gain=2)
    def display_coords(self, event): self.coord_label.configure(text=f"X: {event.x} Y:{event.y}") 
    def clear_label(self): self.info_label.configure(text='') # to remove any text from info label
    def exit_window(self, event=None): self.destroy() # to exit the window

app = App()
app.mainloop()
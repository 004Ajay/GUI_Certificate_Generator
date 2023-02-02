import os, random, customtkinter as ctk
from tkinter import filedialog, messagebox as mb
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL.Image import Resampling

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark. ### Window theme
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green. ### Used for default button colors & other

normalFont = ('fonts/Montserrat-Regular.ttf', 17) # used many times for buttons, small headings etc...

win = ctk.CTk() ####### ↓↓↓ Main Window or Root ↓↓↓ #######
win.title("Certifly")
win.iconbitmap('images/icon.ico') # certifly window icon
win.geometry(f"{win.winfo_screenwidth()}x{win.winfo_screenheight()}") # getting user's screen size
win.state('zoomed')
title = ctk.CTkLabel(win, text='CERTIFLY', font=('fonts/Montserrat-Bold.ttf', 50)) # Setting title
tagline = ctk.CTkLabel(win, text='Certificates on the Go', font=normalFont) # Setting tagline

def move(event): canvas.moveto(drag_image,event.x-103,event.y)
def scan(event): canvas.scan_mark(event.x, event.y)
def drag(event): canvas.scan_dragto(event.x, event.y, gain=2)
def display_coords(event): coord_label.configure(text=f"X: {event.x} Y:{event.y}") 
def clear_label(): info_label.configure(text='') # to remove any text from info label
def exit_window(event): win.destroy() # to exit the window

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

def non_empty_textbox():    
    if len(name_entry.get("1.0","end")) == 1: # checking if text box is empty, 1 denotes a (end-of-line(EOL), newline character, invisible character) 
        mb.showerror('Name error', 'Please add some names')
    else: return True    

global name_list
name_list = []
def enter_names():
    if non_empty_textbox():       
        global name_list
        names = name_entry.get("1.0","end").upper() # getting all texts from textbox & changing to uppercase
        name_list = names.splitlines() # splitting texts by line
        info_label.configure(text='Names Entered')
        win.after(3000, clear_label)
        
def open_image():
    if non_empty_textbox():
        try:
            global ratio, drag_image, filepath # for accessing the selected image on generate() function
            filepath = filedialog.askopenfilename()
            image = Image.open(filepath)
            width, height = 1000, 650
            ratio = min(width/image.width, height/image.height)
            image = image.resize((int(image.width*ratio), int(image.height*ratio)), Resampling.BILINEAR)
            photo = ImageTk.PhotoImage(image)
            img_on_canvas = canvas.create_image(0, 0, image=photo, anchor="nw")
            canvas.configure(canvas.bbox(img_on_canvas))
            sample_name_image = ImageTk.PhotoImage(Image.open("images/name.png")) ####### ↓↓↓ dragging name box ↓↓↓ #######
            drag_image = canvas.create_image(100, 100, image=sample_name_image, anchor="nw")   
            canvas.configure(scrollregion=canvas.bbox(drag_image))
        except:
            mb.showerror('Error', 'Please select an image')

        """finally:
            canvas.tag_bind(drag_image,"<Button1-Motion>", move, add="+") ####### ↓↓↓ key binds ↓↓↓ #######
            canvas.bind("<Button-3>", scan)
            canvas.bind("<Button3-Motion>", drag)
            canvas.tag_bind(drag_image, "<Button1-Motion>", show_coordinates, add="+")"""

        canvas.tag_bind(drag_image,"<Button1-Motion>", move, add="+") ####### ↓↓↓ key binds ↓↓↓ #######
        canvas.bind("<Button-3>", scan)
        canvas.bind("<Button3-Motion>", drag)
        canvas.tag_bind(drag_image, "<Button1-Motion>", show_coordinates, add="+")    

global x, y # for checking in generate functions
x = y = None
def show_coordinates(event):
    global x, y # for changing global values of x & y
    x = event.x/ratio 
    y = event.y/ratio
    coord_label.configure(text=f"X: {round(x,2)}, Y: {round(y,2)}")

def gen_err_check():
    if len(name_list) == 0:
        mb.showerror('Name error', 'Please add some names')
    elif x is None: # no check for 'y' as it is selected with 'x'
        mb.showerror('Coordinates error', "Drag & place 'Sample Name' to set coordinates")
    else: return True    

def generate_sample():
    sample_names = []
    if gen_err_check():
        try:                
            sample_names = [random.choice(name_list) for _ in range(2)] # list comprehension
            generate(sample_names, x, y)
            mb.showinfo('Cerificates Generated', 'Sample cerificates has been generated')
        except:
            mb.showerror('Error', 'Unknown error occured')

def generate_all():
    if gen_err_check():
        try:
            generate(name_list, x, y)
            mb.showinfo('Cerificates Generated', 'All cerificates has been generated')
        except:
            mb.showerror('Error', 'Unknown error occured')
            
global is_dark
is_dark = False # initializing the variable
def mode_switcher():
    global is_dark
    is_dark = not is_dark # toggle the value of is_dark
    if is_dark:
        ctk.set_appearance_mode("light")
        mode_switch_button.configure(image=dark_mode_img)
        canvas.configure(bg='#dbdbdb')
    else:
        ctk.set_appearance_mode("dark")  # Modes: system, light, dark 
        mode_switch_button.configure(image=light_mode_img)

dark_mode_img = ctk.CTkImage(Image.open('images/dark_mode.png'), size=(30, 30))
light_mode_img = ctk.CTkImage(Image.open('images/light_mode.png'), size=(30, 30))
mode_switch_button = ctk.CTkButton(win, image=light_mode_img, text="", height=20, width=20, corner_radius=50, fg_color="transparent", command=mode_switcher)
sideFrame = ctk.CTkFrame(win) ####### ↓↓↓ Frame to hold the name textbox and related buttons ↓↓↓ #######
name_entry_title = ctk.CTkLabel(sideFrame, text='Enter names to be printed', font=normalFont) ####### ↓↓↓ making widgets ↓↓↓ #######
name_entry = ctk.CTkTextbox(sideFrame, width=170, height=120, font=normalFont, wrap='word') # for getting names from user
name_button = ctk.CTkButton(sideFrame, text="Enter names", font=normalFont, corner_radius=40, command=enter_names) # button to enter the names
open_button = ctk.CTkButton(sideFrame, text="Open Image", font=normalFont, corner_radius=40, command=open_image) #  button to open an image file
gen_sample_button = ctk.CTkButton(sideFrame, text="Generate Sample", font=normalFont, corner_radius=40, command=generate_sample) #  button to open an image file
gen_all_button = ctk.CTkButton(sideFrame, text="Generate All",font=normalFont, corner_radius=40, command=generate_all) #  button to open an image file
coord_label = ctk.CTkLabel(sideFrame, text="X: Y:",font=normalFont) # label to show the coordinates of the point clicked
info_label = ctk.CTkLabel(sideFrame, text='',font=normalFont, text_color='green') # label to show info about button clicks & all
title.pack() ####### ↓↓↓ placing widgets ↓↓↓ #######
tagline.pack()
mode_switch_button.pack(side='right', anchor='ne', padx=30)
sideFrame.pack(side='left', padx=20)
name_entry_title.pack(padx=30, pady=10, anchor='center')
name_entry.pack(padx=30, pady=5, anchor='center')
name_button.pack(padx=30, pady=10, anchor='center')
open_button.pack(padx=30, pady=10, anchor='center')
gen_sample_button.pack(padx=30, pady=10, anchor='center')
gen_all_button.pack(padx=30, pady=10, anchor='center')
coord_label.pack(padx=30, pady=20, anchor='center')
info_label.pack(padx=30, pady=20, anchor='center')
canvasFrame = ctk.CTkFrame(win) ####### ↓↓↓ Frame to hold canvas and dragging & opened image ↓↓↓ #######
canvasFrame.pack(side="right", padx=50)
canvas = ctk.CTkCanvas(canvasFrame, width=910, height=650) # canvas to display dragging & opened image
canvas.grid(row=0, column=0, sticky="nsew")

win.bind("<Escape>", exit_window) # press 'escape' to exit the window
win.mainloop()
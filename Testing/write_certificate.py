import os
from PIL import Image, ImageDraw, ImageFont

# Global Variables
font = ImageFont.truetype('fonts/Poppins-Medium.ttf', 40) # Setting the font to Poppins Medium and font size to 40
names = []


# Creates a new 'generated_certificates' folder if not already present
def folder_check():
    if os.path.isdir("generated_certificates"): 
        # shutil.rmtree("generated_certificates")
        os.system("rmdir /s /q generated_certificates")
        os.mkdir("generated_certificates")
    else:
        os.mkdir("generated_certificates")

def generate(names, x, y):
    folder_check()
    for name in names:  
        print("Generating " + name + ".png")
        
        img = Image.open("ctf.png") # Loading the certificate template
        draw = ImageDraw.Draw(img)
        # w, h = draw.textsize(name, font=font)

        name_x, name_y = x, y # Setting the co-ordinates to where the names should be entered
        draw.text((name_x, name_y), name, font=font, fill="black")      
        img.save(r'generated_certificates/' + name + ".png") # Saving the images to the generated_certificates directory
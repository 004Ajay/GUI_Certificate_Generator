from PIL import Image, ImageDraw, ImageFont
import os, shutil, xlrd

# Global Variables
spreadsheet_file = 'test.xlsx'
font = ImageFont.truetype('fonts/Poppins-Medium.ttf', 40) # Setting the font to Poppins Medium and font size to 40
names = []


# Creates a new 'generated' folder if not already present
def folder_check():
    if os.path.isdir("generated_certificates"): 
        shutil.rmtree("generated_certificates")
        os.mkdir("generated_certificates")
    else:
        os.mkdir("generated_certificates")


def findNameCol(sheet):
    for i in range(sheet.ncols):
        if "NAME" in sheet.cell_value(0, i).upper(): # Programmatically finds column heading 'name' in the spreadsheet, without explicitly asking the user
            name_col = i
    return name_col


def getNames(): # Gets names from the xlsx file
    
    workbook = xlrd.open_workbook(spreadsheet_file)
    sheet = workbook.sheet_by_index(0) # Getting first sheet of the xlsx workbook

    for i in range(sheet.nrows):
        names.append(sheet.cell_value(i, findNameCol(sheet))) # Extracts names from the column and inserts it into the array
    del names[0] # Deleting the column heading
    return names
        

def generate(names):
    folder_check()
    for name in names:  
        print("Generating " + name + ".png")
        
        img = Image.open("templates/ctf.png") # Loading the certificate template
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(name, font=font)

        name_x, name_y = (1280-w)/2, (((82-h)/2)+434) # Setting the co-ordinates to where the names should be entered
        draw.text((name_x, name_y), name, font=font, fill="black")          
        img.save(r'generated_certificates/' + name + ".png") # Saving the images to the generated_certificates directory
generate(getNames())
from tkinter import *

root = Tk()
root.geometry('250x150')

button1 = Button(text="button1")
button1.pack(side = BOTTOM, pady=6)

button2 = Button(text="button2")
button2.pack(side = BOTTOM, pady=3)

root.mainloop()
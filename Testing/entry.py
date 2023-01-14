import tkinter as tk

def on_submit():
    names = entry.get()
    names_list = names.splitlines()
    print(names_list)

def on_enter(event): entry.insert("end", "\n")

root = tk.Tk()
root.title("Name List")

root.geometry('500x500')

label = tk.Label(root, text="Enter names separated by new lines:")
label.pack()

entry = tk.Entry(root)
entry.bind("<Return>", on_enter)
entry.pack()

submit = tk.Button(root, text="Submit", command=on_submit)
submit.pack()

root.mainloop()
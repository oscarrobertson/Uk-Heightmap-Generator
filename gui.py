import sys
from Tkinter import *

gui = Tk()

gui.geometry('800x400+200+200')
gui.title('Heightmap Generator')

logo = PhotoImage(file="output.gif")
w1 = Label(gui, image=logo).pack(side="right")

gui.mainloop()

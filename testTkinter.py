# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 02:57:50 2019

@author: dlwjddnbest
"""

#from tkinter import *
from Tkinter import *

def sel():
    selection = "Value = " + str(var.get())
    label.config(text=selection)

def chg(value):
    selection = "Change = " + str(value)
    label.config(text=selection)
    

root = Tk()
#root.geometry('800x480+500+500')
root.attributes("-fullscreen", True)
var = DoubleVar()
scale = Scale(root, variable=var, command=chg, from_=6, to=-20)
scale.place(x=100, y=100, width=100, height=300)
#scale.pack(anchor=W)

button = Button(root, text="Get Scale Value", command=sel)
button.pack(anchor=E)

label = Label(root)
label.pack()

root.mainloop()
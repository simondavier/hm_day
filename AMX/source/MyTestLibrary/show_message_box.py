# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:08:29 2018

@author: WeicZhang
"""

import tkinter
import tkinter.messagebox

def show_message_box():
    root = tkinter.Tk()
    tkinter.messagebox.showinfo('notice','please push reset button  at least 10 seconds!')
    root.destroy()
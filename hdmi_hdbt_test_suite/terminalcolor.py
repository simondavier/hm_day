#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes
  
STD_INPUT_HANDLE = -10  
STD_OUTPUT_HANDLE= -11  
STD_ERROR_HANDLE = -12  
  
FOREGROUND_DARKBLUE = 0x01 # dark blue
FOREGROUND_DARKGREEN = 0x02 # dark green
FOREGROUND_DARKSKYBLUE = 0x03 # dark sky blue
FOREGROUND_DARKRED = 0x04 # dark red
FOREGROUND_DARKPINK = 0x05 # dark pink
FOREGROUND_DARKYELLOW = 0x06 # dark yellow
FOREGROUND_DARKWHITE = 0x07 # dark white
FOREGROUND_DARKGRAY = 0x08 # dark gray
FOREGROUND_BLUE = 0x09 # blue
FOREGROUND_GREEN = 0x0a # green
FOREGROUND_SKYBLUE = 0x0b # sky blue
FOREGROUND_RED = 0x0c # red
FOREGROUND_PINK = 0x0d # pink
FOREGROUND_YELLOW = 0x0e # yellow
FOREGROUND_WHITE = 0x0f # white
 
std_out_handle=ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
 
def set_cmd_text_color(color, handle=std_out_handle):
    Bool=ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool
 
def resetColor():
    set_cmd_text_color(FOREGROUND_DARKWHITE)
 
def cprint(mess,color):
    if color=='DARKBLUE':
        set_cmd_text_color(FOREGROUND_DARKBLUE)
 
    elif color=='DARKGREEN':
        set_cmd_text_color(FOREGROUND_DARKGREEN)
 
    elif color=='DARKSKYBLUE':
        set_cmd_text_color(FOREGROUND_DARKSKYBLUE)
        
    elif color=='DARKRED':
        set_cmd_text_color(FOREGROUND_DARKRED)
 
    elif color=='DARKPINK':
        set_cmd_text_color(FOREGROUND_DARKPINK)
        
    elif color=='DARKYELLOW':
        set_cmd_text_color(FOREGROUND_DARKYELLOW)
 
    elif color=='DARKWHITE':
        set_cmd_text_color(FOREGROUND_DARKWHITE)
 
    elif color=='DARKGRAY':
        set_cmd_text_color(FOREGROUND_DARKGRAY)
 
    elif color=='BLUE':
        set_cmd_text_color(FOREGROUND_BLUE)
 
    elif color=='GREEN':
        set_cmd_text_color(FOREGROUND_GREEN)
 
    elif color=='SKYBLUE':
        set_cmd_text_color(FOREGROUND_SKYBLUE)
 
    elif color=='RED':
        set_cmd_text_color(FOREGROUND_RED)
 
    elif color=='PINK':
        set_cmd_text_color(FOREGROUND_PINK)
 
    elif color=='YELLOW':
        set_cmd_text_color(FOREGROUND_YELLOW)
 
    elif color=='WHITE':
        set_cmd_text_color(FOREGROUND_WHITE)
    print(mess)
    resetColor()
 
if __name__=='__main__':
        cprint("This is RED",'RED')
        cprint("This is BLUE",'BLUE')
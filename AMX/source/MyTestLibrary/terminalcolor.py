
import ctypes
  
STD_INPUT_HANDLE = -10  
STD_OUTPUT_HANDLE= -11  
STD_ERROR_HANDLE = -12  
  
FOREGROUND_DARKBLUE = 0x01 # 暗蓝色
FOREGROUND_DARKGREEN = 0x02 # 暗绿色
FOREGROUND_DARKSKYBLUE = 0x03 # 暗天蓝色
FOREGROUND_DARKRED = 0x04 # 暗红色
FOREGROUND_DARKPINK = 0x05 # 暗粉红色
FOREGROUND_DARKYELLOW = 0x06 # 暗黄色
FOREGROUND_DARKWHITE = 0x07 # 暗白色
FOREGROUND_DARKGRAY = 0x08 # 暗灰色
FOREGROUND_BLUE = 0x09 # 蓝色
FOREGROUND_GREEN = 0x0a # 绿色
FOREGROUND_SKYBLUE = 0x0b # 天蓝色
FOREGROUND_RED = 0x0c # 红色
FOREGROUND_PINK = 0x0d # 粉红色
FOREGROUND_YELLOW = 0x0e # 黄色
FOREGROUND_WHITE = 0x0f # 白色
 
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

def test(flag, h, v):
    x=h
    y=v
    if flag:
        x=round(x/2)
        y=round(y/2)
    print(x)
    print(y)


def test1(filename):
    str="This is:"
    with open(filename, 'a+') as f:
        f.write(str+"Simon"+'\n')
if __name__=='__main__':
        # cprint("This is RED",'RED')
        # cprint("This is BLUE",'BLUE')
        #test(0, 1080, 720)
        test1("111.log")

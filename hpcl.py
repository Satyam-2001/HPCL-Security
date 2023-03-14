# GLOBAL VARIABLES
WIDTH = 800
HEIGHT = 500
BG_COLOR = 'white'
BUTTON_COLOR = 'grey'
BUTTON_COLORS = 'blue'
BUTTON_GAP = 2
WIDTH_BUTTON = 80
DISTANCE_BW_DASHLINE_AND_BUTTON = 10
PADDING_X = 2 * BUTTON_GAP
PADDING_Y = 10
NO_OF_BUTTON = 5
INTERVAL = 7 # in seconds

# DERIVED VARIABLES
START_ANGLE = -90
ANGULAR_DISPLACEMENT = 180 // NO_OF_BUTTON

# STORAGE
ITEM_BUTTON = []
BUTTON_ACTION = [] # list of function which will execute on action
BUTTON_CLEAR = [] # list of function which will execute on lost focus

from tkinter import *
import math
from PIL import ImageTk, Image
from collections import deque
import pygame
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN)
GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)
GPIO.setup(25,GPIO.IN)
GPIO.setup(22,GPIO.IN)
GPIO.setup(17,GPIO.IN)

Active = 0
B = [0] * 5
mplay=1

pygame.init()
root = Tk()
canvas = Canvas(root, width = WIDTH, height = HEIGHT, borderwidth = 0, highlightthickness = 0,bg = BG_COLOR)
canvas.grid()
check_list = []
index = 0
CName = ['HCD ACTIVATED', 'SMOKE DETECTOR ACTIVATED', 'PLANT ESD ACTIVATED', 'DYKE VALVE OPENED', 'EMERGENCY GATE OPEN']
HName = ['हाइड्रोकार्बन डिटेक्टर सक्रिय','स्मोक डिटेक्टर सक्रिय','प्लांट इमरजेंसी शटडाउन सक्रिय','डाइक वाल्व खोला गया','इमरजेंसी गेट खुला']
KName = ['ಎಚ್ಸಿಡಿ ಸಕ್ರಿಯಗೊಳಿಸಲಾಗಿದೆ','ಸ್ಮೋಕ್ ಡಿಟೆಕ್ಟರ್ ಆನ್ ಆಗಿದೆ','ತುರ್ತು ಸ್ಥಗಿತಗೊಳಿಸುವಿಕೆ ಆನ್ ಆಗಿದೆ','ಡೈಕ್ ವಾಲ್ವ್ ತೆರೆಯಲಾಗಿದೆ','ತುರ್ತು ಗೇಟ್ ತೆರೆಯಲಾಗಿದೆ']

C = [[0, 0, 0, 0] for _ in range(5)]

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle_arc = _create_circle_arc


# CREATING ARC BUTTON
def button(start, end):
    return canvas.create_circle_arc(PADDING_X, HEIGHT // 2, HEIGHT // 2 - PADDING_Y, fill = BUTTON_COLOR, outline = "", start = start, end = end)

# CREATING CIRCULAR DASHED LINE
def dashed_circle(start, end, dash):
    for i in range(start, end + 1, sum(dash)):
        canvas.create_circle_arc(PADDING_X, HEIGHT // 2, HEIGHT // 2 - PADDING_Y - WIDTH_BUTTON - DISTANCE_BW_DASHLINE_AND_BUTTON, style="arc", outline = BUTTON_COLOR, width = 3, start = i, end = i + dash[0])

def on_remove(x):
    global C
    button_blur(x)
    if x == check_list[(index - 1) % len(check_list)]:
        pygame.mixer.music.stop()
    try: BUTTON_CLEAR[x]()
    except: pass

class MainLoop(Frame):
    global mplay
    def callback(self):
        global index, C, CName
        if check_list and not pygame.mixer.music.get_busy():
            index %= len(check_list)
            x = check_list[index]
            pygame.mixer.music.load(f'm{x + 1}.wav')
            if (mplay == 1):    
                pygame.mixer.music.play()
            index += 1
        self.after(1000, self.callback)
            

def button_in_action(x):
    canvas.itemconfig(ITEM_BUTTON[x], fill = 'red')
    C[x][0] = canvas.create_rectangle(280 , 490 - x * 100 ,720 , 410 - x * 100, outline = "blue" , fill = "red" , width = 2)
    C[x][1] = canvas.create_text(500, 425 - x * 100, text=CName[x] ,font = "black 18")
    C[x][2] = canvas.create_text(500, 450 - x * 100, text=HName[x] ,font = "black 18")
    C[x][3] = canvas.create_text(500, 475 - x * 100, text=KName[x] ,font = "black 18")
    

def button_blur(x):
    canvas.itemconfig(ITEM_BUTTON[x], fill = BUTTON_COLOR)
    canvas.delete(C[x][0])
    canvas.delete(C[x][1])
    canvas.delete(C[x][2])
    canvas.delete(C[x][3])

def sensor_event(sensor_pos, action):
    global index
    if action:
        if sensor_pos not in check_list:
            button_in_action(sensor_pos)
            check_list.append(sensor_pos)
    elif sensor_pos in check_list:
        j = check_list.index(sensor_pos)
        on_remove(sensor_pos)
        if j <= index:
            index -= 1
        check_list.pop(j)
        

# CREATING BUTTONS
for i in range(NO_OF_BUTTON):
    start = START_ANGLE + i * ANGULAR_DISPLACEMENT + BUTTON_GAP * int(i != 0)
    end = START_ANGLE + (i + 1) * ANGULAR_DISPLACEMENT - BUTTON_GAP * int(i != NO_OF_BUTTON - 1)
    ITEM_BUTTON.append(button(start, end))

canvas.create_circle_arc(PADDING_X, HEIGHT // 2, HEIGHT // 2 - PADDING_Y - WIDTH_BUTTON, fill= BG_COLOR, outline = "", start = -90, end = 90)


img = Image.open("HP.jpg")
w, h = img.size
img = ImageTk.PhotoImage(img)
canvas.create_image(w // 2 + PADDING_X, HEIGHT // 2, image=img)

img1 = Image.open("1.png")
img1 = ImageTk.PhotoImage(img1)
canvas.create_image(60, 60, image=img1)

img2 = Image.open("2.png")
img2 = ImageTk.PhotoImage(img2)
canvas.create_image(165, 130, image=img2)

img3 = Image.open("3.png")
img3 = ImageTk.PhotoImage(img3)
canvas.create_image(200, 250, image=img3)

img4 = Image.open("4.png")
img4 = ImageTk.PhotoImage(img4)
canvas.create_image(165, 375, image=img4)

img5 = Image.open("5.png")
img5 = ImageTk.PhotoImage(img5)
canvas.create_image(60, 440, image=img5)

dashed_circle(-90, 90, (3, 3))

def readeverysec():
    global B,mplay
    Active = GPIO.input(17)
    if (Active == 1):
        mplay=1
        for i in range(5):
            B[i] = GPIO.input(22 + i)
            sensor_event(i, not B[i])
    else:
        pygame.mixer.music.stop()
        mplay=0       
    root.after(700, readeverysec)


root.title("HP Graphics")
root.attributes('-fullscreen',True)
readeverysec()
MainLoop().callback()
root.mainloop()
# GLOBAL VARIABLES
WIDTH = 1000
HEIGHT = 600
BG_COLOR = 'white'
BUTTON_COLOR = 'grey'
PRESSED_BUTTON_COLOR = 'red'
NO_OF_BUTTON = 5
BUTTON_GAP = 18 / (NO_OF_BUTTON - 1)
WIDTH_BUTTON = WIDTH / 10
DISTANCE_BW_DASHLINE_AND_BUTTON = 10
PADDING_X = 2 * BUTTON_GAP
PADDING_Y = 10
INTERVAL = 7 # in seconds

# DERIVED VARIABLES
START_ANGLE = -90
ANGULAR_DISPLACEMENT = (180 - (NO_OF_BUTTON - 1) * BUTTON_GAP) / NO_OF_BUTTON
OUTER_RADIUS = HEIGHT / 2 - PADDING_Y
INNER_RADIUS = OUTER_RADIUS - WIDTH_BUTTON

# STORAGE
ITEM_BUTTON = []
BUTTON_ACTION = [] # list of function which will execute on action
BUTTON_CLEAR = [] # list of function which will execute on lost focus

from tkinter import *
import math
from PIL import ImageTk, Image
import pygame

B = [0] * NO_OF_BUTTON
mplay = True

pygame.init()
root = Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
canvas = Canvas(root, width = WIDTH, height = HEIGHT, borderwidth = 0, highlightthickness = 0,bg = BG_COLOR)
canvas.grid()
check_list = []
index = 0
CName = ['HCD ACTIVATED', 'SMOKE DETECTOR ACTIVATED', 'PLANT ESD ACTIVATED', 'DYKE VALVE OPENED', 'EMERGENCY GATE OPEN']
HName = ['हाइड्रोकार्बन डिटेक्टर सक्रिय','स्मोक डिटेक्टर सक्रिय','प्लांट इमरजेंसी शटडाउन सक्रिय','डाइक वाल्व खोला गया','इमरजेंसी गेट खुला']
KName = ['ಎಚ್ಸಿಡಿ ಸಕ್ರಿಯಗೊಳಿಸಲಾಗಿದೆ','ಸ್ಮೋಕ್ ಡಿಟೆಕ್ಟರ್ ಆನ್ ಆಗಿದೆ','ತುರ್ತು ಸ್ಥಗಿತಗೊಳಿಸುವಿಕೆ ಆನ್ ಆಗಿದೆ','ಡೈಕ್ ವಾಲ್ವ್ ತೆರೆಯಲಾಗಿದೆ','ತುರ್ತು ಗೇಟ್ ತೆರೆಯಲಾಗಿದೆ']

C = [[0, 0, 0, 0] for _ in range(NO_OF_BUTTON)]

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle_arc = _create_circle_arc

# CREATING ARC BUTTON
def button(start, end):
    return canvas.create_circle_arc(PADDING_X, HEIGHT // 2, OUTER_RADIUS, fill = BUTTON_COLOR, outline = "", start = start, end = end)

# CREATING CIRCULAR DASHED LINE
def dashed_circle(start, end, dash):
    for i in range(start, end + 1, sum(dash)):
        canvas.create_circle_arc(PADDING_X, HEIGHT // 2, INNER_RADIUS - DISTANCE_BW_DASHLINE_AND_BUTTON, style="arc", outline = BUTTON_COLOR, width = 3, start = i, end = i + dash[0])

# MUSIC PLAYER LOOP
class MainLoop(Frame):
    global mplay
    def callback(self):
        global index, C, CName
        if check_list and not pygame.mixer.music.get_busy():
            index %= len(check_list)
            x = check_list[index]
            try:
                pygame.mixer.music.load(f'audio/m{x + 1}.wav')
                if mplay: pygame.mixer.music.play()
            except: print('music not loaded!!')
            index += 1
        self.after(1000, self.callback)

# ENCOUNTER THE BUTTON CLICK
def click_event(event):
    global index
    x = (event.x - PADDING_X)
    y = (event.y - HEIGHT // 2)
    if x < 0: return
    r = (x * x + y * y) ** 0.5
    if not (INNER_RADIUS <= r <= OUTER_RADIUS): return
    theta = -math.atan(y / x) * 180 / math.pi - START_ANGLE
    if theta % (ANGULAR_DISPLACEMENT + BUTTON_GAP) > ANGULAR_DISPLACEMENT: return
    i = int(theta // (ANGULAR_DISPLACEMENT + BUTTON_GAP))
    if i not in check_list:
        check_list.append(i)
        button_focus(i)
    else:
        j = check_list.index(i)
        button_blur(i)
        if j <= index:
            index -= 1
        check_list.pop(j)

# REMOVING RECTANGULAR TEXT BOX
def button_blur(x):
    global C
    canvas.itemconfig(ITEM_BUTTON[x], fill = BUTTON_COLOR)
    canvas.delete(C[x][0])
    canvas.delete(C[x][1])
    canvas.delete(C[x][2])
    canvas.delete(C[x][3])
    if x == check_list[(index - 1) % len(check_list)]:
        pygame.mixer.music.stop()
    try: BUTTON_CLEAR[x]()
    except: pass
            
# CREATING RECTANGULAR TEXT BOX
def button_focus(x):
    canvas.itemconfig(ITEM_BUTTON[x], fill = PRESSED_BUTTON_COLOR)
    font_size = str(HEIGHT // (6 * NO_OF_BUTTON))
    margin_h = WIDTH // 12
    start_h = HEIGHT // 2 + margin_h // 1.5
    end_h = WIDTH - margin_h
    margin_w = int(HEIGHT * (3 / 100))
    height_w = (HEIGHT - (NO_OF_BUTTON + 1) * margin_w) // (NO_OF_BUTTON)
    start_w = HEIGHT - x * (height_w + margin_w) - margin_w
    end_w = start_w - height_w
    text_margin = (height_w - 3 * int(font_size)) // 4
    text_w = start_h + (end_h - start_h) // 2
    text_h = start_w - height_w + int(font_size) // 2 + text_margin
    C[x][0] = canvas.create_rectangle(start_h , start_w, end_h, end_w, outline = "blue" , fill = "red" , width = 2)
    C[x][1] = canvas.create_text(text_w, text_h, text=CName[x] ,font = ("black 18", font_size))
    C[x][2] = canvas.create_text(text_w, text_h + int(font_size) + text_margin, text=HName[x] ,font = ("black 18", font_size))
    C[x][3] = canvas.create_text(text_w, text_h + 2 * (int(font_size) + text_margin), text=KName[x] ,font = ("black 18", font_size))

# TAKING ACTION ON THE INPUT SIGNAL [NOT FOR PC]
def sensor_event(sensor_pos, action):
    global index
    if action:
        if sensor_pos not in check_list:
            button_focus(sensor_pos)
            check_list.append(sensor_pos)
    elif sensor_pos in check_list:
        j = check_list.index(sensor_pos)
        button_blur(sensor_pos)
        if j <= index:
            index -= 1
        check_list.pop(j)

# CREATING BUTTONS
for i in range(NO_OF_BUTTON):
    start = START_ANGLE + i * (ANGULAR_DISPLACEMENT + BUTTON_GAP)
    end = start + ANGULAR_DISPLACEMENT
    ITEM_BUTTON.append(button(start, end))

canvas.bind('<Button-1>', click_event)
canvas.create_circle_arc(PADDING_X, HEIGHT // 2, INNER_RADIUS, fill= BG_COLOR, outline = "", start = -90, end = 90)

# HP LOGO
img = Image.open("images/HP.jpg")
w, h = img.size
img = ImageTk.PhotoImage(img)
canvas.create_image(w // 2 + PADDING_X, HEIGHT // 2, image=img)

# SHOWING IMAGES
images =  []
for i in range(NO_OF_BUTTON):
    img_ = Image.open(f"images/{i + 1}.png")
    images.append(ImageTk.PhotoImage(img_))
    angle = (START_ANGLE + i * (ANGULAR_DISPLACEMENT + BUTTON_GAP) + ANGULAR_DISPLACEMENT / 2) * math.pi / 180
    r = INNER_RADIUS + WIDTH_BUTTON / 2
    x = PADDING_X +  r * math.cos(angle)
    y = HEIGHT / 2 + r * math.sin(angle)
    canvas.create_image(x, y, image=images[i])

dashed_circle(-90, 90, (3, 3))

root.title("HP Graphics")
# root.attributes('-fullscreen',True)
MainLoop().callback()
root.mainloop()
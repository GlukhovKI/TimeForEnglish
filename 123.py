import random
import time
from datetime import datetime
from tkinter import *


def button_exit():
    exit()


def change():
    translate = english_dict.get(label['text'])
    key = translate[0] if isinstance(translate, list) else translate
    answer = entry.get()

    if answer == key:
        b1['text'] = "Круто!"
        b1['bg'] = '#000000'
        b1['activebackground'] = '#555555'
        b1['fg'] = '#ffffff'
        b1['activeforeground'] = '#ffffff'

        del english_dict[label['text']]
        if not english_dict:
            exit()
        label['text'] = random.choice(list(english_dict.keys()))
        entry.delete(0, END)

    else:
        b1['text'] = "Проверить"
        b1['bg'] = '#ffffff'
        b1['activebackground'] = '#ffffff'
        b1['fg'] = '#000000'
        b1['activeforeground'] = '#555555'


root = Tk()
frame_top = Frame()
frame_bot = Frame()

# узнаем размеры экрана
screen_width = root.winfo_screenwidth()  # ширина экрана
screen_height = root.winfo_screenheight()  # высота экрана

width = screen_width // 2  # середина экрана
height = screen_height // 2
width -= 200  # смещение от середины
height -= 200
root.geometry('600x600+{}+{}'.format(width, height))

# установка цвета фона окна
background_color = '#555'
root.configure(background=background_color)

english_dict = {'Ходить': ['go', 'went', 'gone'],
                'Спорить': 'argue',
                'Привести в порядок свою комнату': 'tidy your room',
                }

label = Label(frame_top,
              fg='black',
              # bg=background_color,
              )
label['text'] = text = random.choice(list(english_dict.keys()))
label.place(relx=0.5, rely=0.5)

entry = Entry(frame_top, width=20)

b1 = Button(frame_top, text="Проверить", width=10, height=1)

b1.config(command=change)

button = Button(frame_bot, text="Закрыть")
# button.bind('<Button-1>', button_exit)
button.config(command=button_exit)

frame_top.pack(padx=10, pady=10)
frame_bot.pack(padx=10, pady=10)

label.pack(side=LEFT, padx=10, pady=10)
entry.pack(side=LEFT, padx=10, pady=10)
b1.pack(side=LEFT, padx=10, pady=10)
button.pack(side=RIGHT)

root.mainloop()
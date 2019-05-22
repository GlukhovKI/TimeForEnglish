import random
from tkinter import *


def button_exit():
    exit()


def change():
    translate = english_dict.get(label['text'])
    key = translate[0] if isinstance(translate, list) else translate
    answer = entry.get()

    if answer == key:

        info_label['text'] = 'Молодчик!'
        info_label.config(fg='blue')

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
        entry.config(fg='red')
        info_label['text'] = 'ЛОШАРА!'
        info_label.config(fg='red')


root = Tk()
info_frame_top = Frame()
frame_top = Frame()
frame_bot = Frame()

# узнаем размеры экрана
screen_width = root.winfo_screenwidth()  # ширина экрана
screen_height = root.winfo_screenheight()  # высота экрана

width = screen_width // 2  # середина экрана
height = screen_height // 2
width -= 450  # смещение от середины
height -= 350
root.geometry('900x700+{}+{}'.format(width, height))

# установка цвета фона окна
background_color = '#555'
root.configure(background=background_color)

english_dict = {'Ходить': ['go', 'went', 'gone'],
                'Спорить': 'argue',
                'Привести в порядок свою комнату': 'tidy your room',
                'Выносить мусор': 'take out the rubbish',
                }

info_label = Label(info_frame_top)
info_label.config(fg='black', height=2, width=15, font="Arial 12")
info_label['text'] = 'Ну попробуй!'
info_label.place(relx=0.5, rely=0.5)

label = Label(frame_top)
label.config(fg='black', height=2, width=45, font="Arial 12")
label['text'] = text = random.choice(list(english_dict.keys()))
label.place(relx=0.5, rely=0.5)

entry = Entry(frame_top, width=20, font="Arial 12")

b1 = Button(frame_top, text="Проверить", width=10, height=1, font="Arial 12")

b1.config(command=change)

button = Button(frame_bot, text="Выход", font="Arial 12")
# button.bind('<Button-1>', button_exit)
button.config(command=button_exit)

info_frame_top.pack(padx=10, pady=10)
frame_top.pack(padx=10, pady=10, expand=1)
frame_bot.pack(padx=10, pady=10)

info_label.pack(side=BOTTOM, padx=10, pady=10)
label.pack(side=LEFT, padx=10, pady=10)
entry.pack(side=LEFT, padx=10, pady=10)
b1.pack(side=LEFT, padx=10, pady=10)
button.pack(side=RIGHT)

root.mainloop()
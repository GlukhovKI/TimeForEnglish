import random
import csv
from tkinter import *


def window_deleted():
    print(1)
    root.quit()


def csv_reader() -> dict:
    """
    Read a csv file
    """

    english_dict = {}
    csv_path = "English_dictionary.csv"

    with open(csv_path, "r") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            english_dict[row['key']] = row

    if english_dict:
        return english_dict
    else:
        raise Exception('Нет данных для изучения - файл English_dictionary.csv')


def button_exit():
    """
    Реализация кнопки "Выход"
    """
    exit()


def change():
    """
    Проверка введенного пользователем значения перевода
    """
    key = label['text']
    key_result = english_dict.get(key, {})
    translate = key_result.get('translate')
    answer = entry.get().lower()
    print('answer -', answer)
    print('translate -', translate)
    if answer == translate:
        text_example['text'] = key_result.get('example_text')
        print('example_text -', key_result.get('example_text'))
        info_label['text'] = 'Молодчик!'
        info_label.config(fg='blue')
        entry.config(fg='black')

        del english_dict[key]
        if not english_dict:
            exit()
            
        label['text'] = random.choice(list(english_dict.keys()))
        entry.delete(0, END)

    else:
        entry.config(fg='red')
        info_label['text'] = 'ЛОШАРА!'
        info_label.config(fg='red')


# подготавливаем массив слов для изучения из файла English_dictionary.csv
english_dict = csv_reader()

# создаем основное окно программы
root = Tk()
root.title('Time For English')

# запрещаем пользователю менять размеры окна!
root.resizable(False, False)

# для особенных
root.protocol('WM_DELETE_WINDOW', window_deleted) # обработчик закрытия окна

# установка цвета фона окна
background_color = '#555'
root.configure(background=background_color)

info_frame_top = Frame(background=background_color)
text_example_frame = Frame(background=background_color)
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

info_label = Label(info_frame_top)
info_label.config(fg='white', height=2, width=15, font="Arial 16", background=background_color, text='Ну попробуй!')
info_label.place(relx=0.5, rely=0.5)

label = Label(frame_top)
label.config(fg='black', height=2, width=45, font="Arial 12")
label['text'] = random.choice(list(english_dict.keys()))
label.place(relx=0.5, rely=0.5)

text_example = Label(text_example_frame)
text_example.config(height=2, font="Arial 12", background=background_color, fg='white')
text_example.place(relx=0.5, rely=0.5)

entry = Entry(frame_top, width=20, font="Arial 12")

b1 = Button(frame_top, text="Проверить", width=10, height=1, font="Arial 12")

b1.config(command=change)

button = Button(frame_bot, text="Выход", font="Arial 12")
# button.bind('<Button-1>', button_exit)
button.config(command=button_exit)

info_frame_top.pack(padx=10, pady=10)
frame_top.pack(expand=1)
text_example.pack(padx=10, pady=10)
text_example_frame.pack(fill=X)
frame_bot.pack(padx=10, pady=10)

info_label.pack(side=BOTTOM, padx=10, pady=10)
label.pack(side=LEFT, padx=10, pady=10)
entry.pack(side=LEFT, padx=10, pady=10)
b1.pack(side=LEFT, padx=10, pady=10)
button.pack(side=RIGHT)

root.mainloop()
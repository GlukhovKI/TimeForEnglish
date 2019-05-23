import random
import csv
from tkinter import *


def window_deleted():
    from tkinter import messagebox
    messagebox.showinfo("Попалась", 'Блять! ВЕРА! Для кого кнопка "Выход"???')
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


def close_button_func():
    """
    Реализация кнопки "Close"
    """
    root.quit()


def change(event=None):
    """
    Проверка введенного пользователем значения перевода
    """
    key = label['text']
    key_result = english_dict.get(key, {})
    translate = key_result.get('translate', '').lower()
    answer = entry.get().lower()
    print(answer, ' -> ', translate)
    if answer == translate:
        text_example['text'] = key_result.get('example_text')
        info_label['text'] = 'Молодчик!'
        info_label.config(fg='white')
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


def set_root_config() -> Tk:
    """
    Создание и заполнение конфигурации для корневого окна (root)
    """
    root = Tk()
    root.title('Time For English')

    # Запрещаем пользователю менять размеры окна!
    root.resizable(False, False)

    # для особенных
    root.protocol('WM_DELETE_WINDOW', window_deleted)  # обработчик закрытия окна

    # Установка цвета фона окна
    root.configure(background=background_color)

    # Размеры экрана
    screen_width = root.winfo_screenwidth()  # ширина экрана
    screen_height = root.winfo_screenheight()  # высота экрана

    width = screen_width // 2  # середина экрана
    height = screen_height // 2
    width -= 450  # смещение от середины
    height -= 350
    root.geometry('900x700+{}+{}'.format(width, height))
    return root


if __name__ == '__main__':
    background_color = '#555'

    # Подготавливаем массив слов для изучения из файла English_dictionary.csv
    english_dict = csv_reader()

    # Создаем основное окно программы
    root = set_root_config()

    # Виджет Frame (рамка) предназначен для организации виджетов внутри окна.
    info_frame_top = Frame(root, background=background_color)
    text_example_frame = Frame(root, background='green')
    frame_top = Frame(root)
    frame_bot = Frame(root)

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

    # Entry - это виджет, позволяющий пользователю ввести одну строку текста.
    entry = Entry(frame_top, width=20, font="Arial 12")
    # Метод bind привязывает событие к какому-либо действию (нажатие кнопки мыши, нажатие клавиши на клавиатуре).
    entry.bind("<Return>", change)
    entry.focus()

    check_button = Button(frame_top, text="Проверить", width=10, height=1, font="Arial 12")
    check_button.config(command=change)

    close_button = Button(text="Close", font="Arial 12")
    close_button.config(command=close_button_func)

    info_frame_top.pack(padx=10, pady=10)
    frame_top.pack(expand=1)
    text_example.pack(padx=10, pady=10)
    text_example_frame.pack(side=TOP,fill=X)
    frame_bot.pack(padx=10, pady=10)

    info_label.pack(side=BOTTOM, padx=10, pady=10)
    label.pack(side=LEFT, padx=10, pady=10)
    entry.pack(side=LEFT, padx=10, pady=10)
    check_button.pack(side=LEFT, padx=10, pady=10)
    close_button.pack(side=RIGHT, padx=5, pady=5)

    root.mainloop()
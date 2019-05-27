import csv
import random
import tkinter

SECOND = MINUTE = HOUR = 0


def window_deleted():
    from tkinter import messagebox
    messagebox.showwarning("Блять", 'Блять! ВЕРА! Для кого кнопка "Close"???')
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
        example_text['text'] = key_result.get('example_text')

        # если примера текста нет, то в верхний блок примеров встанет вопрос
        if not example_text['text']:
            example_text['text'] = key_result.get('example_question')
        else:
            example_question['text'] = key_result.get('example_question')

        info_label['text'] = 'Молодчик!'
        info_label.config(fg='white')
        entry.config(fg='black')

        del english_dict[key]
        if not english_dict:
            root.after(3000, root.quit())

        check_button.after(3000, new_test)
        entry.delete(0, tkinter.END)

    else:
        entry.config(fg='#CC3366')
        info_label['text'] = 'Turn on your brain!'
        info_label.config(fg='#993333')


def new_test():
    label['text'] = random.choice(list(english_dict.keys()))


def set_root_config() -> tkinter.Tk:
    """
    Создание и заполнение конфигурации для корневого окна (root)
    """
    root = tkinter.Tk()
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


def tick():
    global SECOND, MINUTE, HOUR
    timer.after(1000, tick)
    SECOND += 1
    if SECOND == 59:
        MINUTE += 1
        SECOND = -1
    elif MINUTE == 59:
        HOUR += 1
        MINUTE = -1
    timer['text'] = "%s:%s:%s" % (HOUR, MINUTE, SECOND)


if __name__ == '__main__':
    background_color = '#669999'

    # Подготавливаем массив слов для изучения из файла English_dictionary.csv
    english_dict = csv_reader()

    # Создаем основное окно программы
    root = set_root_config()

    # Виджет Frame (рамка) предназначен для организации виджетов внутри окна.
    info_frame_top = tkinter.Frame(root, background=background_color)
    example_text_frame = tkinter.Frame(root, background=background_color)
    example_question_frame = tkinter.Frame(root, background=background_color)
    frame_top = tkinter.Frame(root)

    info_frame_top.pack(fill=tkinter.X)
    frame_top.pack()
    frame_top.place(rely=0.4, relx=0.08)
    example_text_frame.pack(fill=tkinter.X)
    example_text_frame.place(rely=0.5, relx=0.1)
    example_question_frame.pack(fill=tkinter.X)
    example_question_frame.place(rely=0.54, relx=0.1)

    info_label = tkinter.Label(info_frame_top)
    info_label.config(fg='white', height=2, width=150, font="Arial 16",
                      background=background_color, text='You need to study more!')
    info_label.place(relx=0.5, rely=0.5)

    label = tkinter.Label(frame_top)
    label.config(fg='black', height=2, width=45, font="Arial 12")
    label['text'] = random.choice(list(english_dict.keys()))
    label.place(relx=0.5, rely=0.5)

    example_text = tkinter.Label(example_text_frame)
    example_text.config(height=3, width=70, font="Purisa 14", background=background_color, fg='white')

    example_question = tkinter.Label(example_question_frame)
    example_question.config(height=3, width=70, font="Purisa 14", background=background_color, fg='white')

    # Entry - это виджет, позволяющий пользователю ввести одну строку текста.
    entry = tkinter.Entry(frame_top, width=20, font="Arial 12")
    # Метод bind привязывает событие к какому-либо действию (нажатие кнопки мыши, нажатие клавиши на клавиатуре).
    entry.bind("<Return>", change)
    entry.focus()

    check_button = tkinter.Button(frame_top, text="Проверить", width=10, height=1, font="Arial 12")
    check_button.config(command=change)

    close_button = tkinter.Button(text="Close", font="Arial 12")
    close_button.config(command=close_button_func)

    info_label.pack(side=tkinter.BOTTOM, padx=10, pady=10)
    example_text.pack(padx=10)
    example_question.pack(padx=10)

    label.pack(side=tkinter.LEFT, padx=10, pady=10)
    entry.pack(side=tkinter.LEFT, padx=10, pady=10)
    check_button.pack(side=tkinter.LEFT, padx=10, pady=10)
    close_button.pack(padx=5, pady=5)
    close_button.place(relx=0.93, rely=0.94)

    timer = tkinter.Label(text="%s:%s:%s" % (HOUR, MINUTE, SECOND), font=("Consolas", 14), fg='white', background=background_color)
    timer.pack()
    timer.after_idle(tick)

    root.mainloop()
import csv
import random
import tkinter

SECOND = MINUTE = HOUR = 0
MISTAKE = False


class SampleApp(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.set_root_config()
        self._frame = None
        self.default_entry_color = 'black'

        # TODO что то придумать с БД и заменить это говно (работа с файлом csv)
        # Подготавливаем массив слов для изучения из файла English_dictionary.csv
        self.csv_reader()

        menu_frame = tkinter.Frame(self, background=self.background_color)
        last_ten_words_button = tkinter.Button(menu_frame, text="Testing Page", font="Arial 12",
                                               command=lambda: self.switch_frame(StartPage))

        last_ten_words_button.pack(side=tkinter.LEFT, padx=10, pady=10)

        last_ten_words_button = tkinter.Button(menu_frame, text="Last 10 Words Added", font="Arial 12",
                                               command=lambda: self.switch_frame(PageOne))

        last_ten_words_button.pack(side=tkinter.LEFT, padx=10, pady=10)

        last_ten_words_button1 = tkinter.Button(menu_frame, text="Irregular Verbs", font="Arial 12",
                                               command=lambda: self.switch_frame(PageTwo))

        last_ten_words_button1.pack(side=tkinter.LEFT, padx=10, pady=10)

        menu_frame.pack(fill=tkinter.X)
        self.switch_frame(StartPage)

    @staticmethod
    def put_placeholder(entry_, text_):
        entry_.insert(0, text_)
        entry_['fg'] = 'grey'

    @staticmethod
    def focus_in(entry_, default_entry_color):
        print(entry_['fg'])
        print(entry_['fg'] == 'grey')
        if entry_['fg'] == 'grey':
            entry_.delete('0', 'end')
            entry_['fg'] = default_entry_color
            print('default_entry_color -', default_entry_color)

    @staticmethod
    def focus_out(entry_, text_):
        if not entry_.get():
            SampleApp.put_placeholder(entry_, text_)

    def switch_frame(self, frame_class):
        """ Destroys current frame and replaces it with a new one. """

        # проверка на повторное нажатие кнопки возврата к окну, в котором находишься,
        # при этом не нужно создавать окно заново
        if self._frame and self._frame.__class__.__name__ == frame_class.__name__:
            return

        # создаем новый виджет
        new_frame = frame_class(self)

        # удаляем старый
        if self._frame is not None:
            self._frame.destroy()

        self._frame = new_frame
        self._frame.pack(fill=tkinter.BOTH, expand=True)

    def set_root_config(self):
        """
        Заполнение конфигурации для корневого окна (root)
        """
        self.background_color = '#669999'
        self.title('Time For English')

        # Запрещаем пользователю менять размеры окна!
        self.resizable(False, False)

        # для особенных
        self.protocol('WM_DELETE_WINDOW', self._window_deleted)  # обработчик закрытия окна

        # Установка цвета фона окна
        self.configure(background=self.background_color)

        # Размеры экрана
        screen_width = self.winfo_screenwidth()  # ширина экрана
        screen_height = self.winfo_screenheight()  # высота экрана

        width = screen_width // 2  # середина экрана
        height = screen_height // 2
        width -= 450  # смещение от середины
        height -= 350
        self.geometry('900x700+{}+{}'.format(width, height))

    @staticmethod
    def _window_deleted():
        from tkinter import messagebox
        messagebox.showwarning("Блять", 'Блять! ВЕРА! Для кого кнопка "Close"???')
        root.quit()

    def close_button_func(self):
        """
        Реализация кнопки "Close"
        """
        self.quit()

    def csv_reader(self) -> (dict, str):
        """
        Получения списка вссех слов и последних 10ти добавленных
        """

        self.words_dict = {}
        self.irregular_verbs_dict = {}
        csv_path = "English_dictionary.csv"

        last_ten_words = []
        with open(csv_path, "r") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            for row in reader:
                if row['irregular_verbs']:
                    print(row)
                    self.irregular_verbs_dict[row['key']] = row
                else:
                    self.words_dict[row['key']] = row
                    last_ten_words.append(row['key'])

        if self.words_dict:
            self.last_ten_words = "\n".join(
                [word + ' -> ' + self.words_dict[word].get('translate', '').lower() for word in last_ten_words[-10:]])

            print('Общее количество записей в файле -', len(self.words_dict) + len(self.irregular_verbs_dict), '\n')
            print(self.last_ten_words)
        else:
            raise Exception('Нет данных для изучения - файл English_dictionary.csv')


class StartPage(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.configure(background=master.background_color)

        # Виджет Frame (рамка) предназначен для организации виджетов внутри окна.
        info_frame_top = tkinter.Frame(self, background=master.background_color)
        example_text_frame = tkinter.Frame(self, background=master.background_color)
        example_question_frame = tkinter.Frame(self, background=master.background_color)
        frame_top = tkinter.Frame(self)

        info_frame_top.pack(fill=tkinter.X)
        frame_top.place(rely=0.4, relx=0.08)
        example_text_frame.pack(fill=tkinter.X)
        example_text_frame.place(rely=0.5, relx=0.1)
        example_question_frame.pack(fill=tkinter.X)
        example_question_frame.place(rely=0.54, relx=0.1)

        self.info_label = tkinter.Label(info_frame_top)
        self.info_label.config(fg='white', height=2, width=150, font="Arial 16",
                               background=master.background_color, text='You need to study more!')
        self.info_label.place(relx=0.5, rely=0.5)

        self.label = tkinter.Label(frame_top)
        self.label.config(fg='black', height=2, width=45, font="Arial 12")
        self.label['text'] = random.choice(list(master.words_dict.keys()))
        self.label.place(relx=0.5, rely=0.5)

        self.example_text = tkinter.Label(example_text_frame)
        self.example_text.config(height=1, width=50, font="Purisa 18", background=master.background_color, fg='white')

        self.example_question = tkinter.Label(example_question_frame)
        self.example_question.config(height=1, width=50, font="Purisa 18", background=master.background_color,
                                     fg='white')

        # Entry - это виджет, позволяющий пользователю ввести одну строку текста.
        self.entry = tkinter.Entry(frame_top, width=20, font="Arial 12", fg='grey')
        # Метод bind привязывает событие к какому-либо действию (нажатие кнопки мыши, нажатие клавиши на клавиатуре).
        # self.entry.bind("<Return>", self.change)
        self.default_entry_color = 'black'
        # master.put_placeholder(self.entry, 'ewrwerw')
        # self.entry.bind("<FocusIn>", master.focus_in(self.entry, self.default_entry_color))
        # self.entry.bind("<FocusOut>", master.focus_out(self.entry, 'ghjsdg'))
        self.entry.focus()

        self.check_button = tkinter.Button(frame_top, text="Проверить", width=10, height=1, font="Arial 12")
        self.check_button.config(command=self.change)

        close_button = tkinter.Button(text="Close", font="Arial 12")
        close_button.config(command=master.close_button_func)

        self.info_label.pack(side=tkinter.BOTTOM, padx=10, pady=10)
        self.example_text.pack(padx=10)
        self.example_question.pack(padx=10)

        self.label.pack(side=tkinter.LEFT, padx=10, pady=10)
        self.entry.pack(side=tkinter.LEFT, padx=10, pady=10)
        self.check_button.pack(side=tkinter.LEFT, padx=10, pady=10)
        close_button.place(relx=0.90, rely=0.90)

        self.timer = tkinter.Label(self, text="%s:%s:%s" % (HOUR, MINUTE, SECOND), font=("Consolas", 14), fg='white',
                                   background=master.background_color)
        self.timer.pack()
        self.timer.after_idle(self.tick)

    def tick(self):
        global SECOND, MINUTE, HOUR
        # Через каждую секунду происходит рекурсивый вызов функции
        self.timer.after(1000, self.tick)
        SECOND += 1
        if SECOND == 59:
            MINUTE += 1
            SECOND = -1
        elif MINUTE == 59:
            HOUR += 1
            MINUTE = -1
        self.timer['text'] = "%s:%s:%s" % (HOUR, MINUTE, SECOND)

    def change(self, event=None):
        """
        Проверка введенного пользователем значения перевода
        """

        global MISTAKE
        key = self.label['text']
        key_result = self.master.words_dict.get(key, {})
        translate = key_result.get('translate', '').lower()
        answer = self.entry.get().lower()
        print(answer, ' -> ', translate)

        if answer == translate:
            self.example_text['text'] = key_result.get('example_text')

            # если примера текста нет, то в верхний блок примеров встанет вопрос
            if not self.example_text['text']:
                self.example_text['text'] = key_result.get('example_question')
            else:
                self.example_question['text'] = key_result.get('example_question')

            self.info_label['text'] = 'I knew you could do it!'
            self.info_label.config(fg='white')
            self.entry.config(fg='black')

            # Если пользователь совершил ошибку, слово не считается пройденным
            if not MISTAKE:
                del self.master.words_dict[key]
            MISTAKE = False

            if not self.master.words_dict:
                root.after(5000, root.quit())

            # Если есть текстовый пример, то следующее тестовое слово появится через 3 сек.
            if self.example_text['text']:
                self.check_button.after(3000, self.new_text_message)
            else:
                self.new_text_message()
            self.entry.delete(0, tkinter.END)
        else:
            MISTAKE = True
            self.entry.config(fg='#CC3366')
            self.info_label['text'] = 'Turn on your brain!'
            self.info_label.config(fg='#993333')

    def new_text_message(self):
        self.label['text'] = random.choice(list(self.master.words_dict.keys()))


class PageOne(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.configure(background=master.background_color)
        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(3, pad=7)
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(5, pad=20)

        ten_words = tkinter.Label(self)
        ten_words.config(fg='white', height=10, width=50, font="Arial 14",
                         background=master.background_color, text=master.last_ten_words)
        ten_words.pack()

        close_button = tkinter.Button(self, text="Close", font="Arial 12")
        close_button.config(command=master.close_button_func)

        close_button.place(relx=0.90, rely=0.90)


class PageTwo(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.configure(background=master.background_color)

        # Виджет Frame (рамка) предназначен для организации виджетов внутри окна.
        info_frame_top = tkinter.Frame(self, background=master.background_color)
        example_text_frame = tkinter.Frame(self, background=master.background_color)
        example_question_frame = tkinter.Frame(self, background=master.background_color)
        frame_top = tkinter.Frame(self)

        info_frame_top.pack(fill=tkinter.X)
        frame_top.place(rely=0.4, relx=0.08)
        example_text_frame.place(rely=0.5, relx=0.1)
        example_question_frame.place(rely=0.54, relx=0.1)

        self.info_label = tkinter.Label(info_frame_top)
        self.info_label.config(fg='white', height=2, width=150, font="Arial 16",
                               background=master.background_color, text='You need to study more!')
        self.info_label.place(relx=0.5, rely=0.5)

        self.label = tkinter.Label(frame_top)
        self.label.config(fg='black', height=2, width=35, font="Arial 12")
        self.label['text'] = random.choice(list(master.irregular_verbs_dict.keys()))
        self.label.place(relx=0.5, rely=0.5)

        self.example_text = tkinter.Label(example_text_frame)
        self.example_text.config(height=1, width=50, font="Purisa 18", background=master.background_color, fg='white')

        self.example_question = tkinter.Label(example_question_frame)
        self.example_question.config(height=1, width=50, font="Purisa 18", background=master.background_color,
                                     fg='white')

        # Entry - это виджет, позволяющий пользователю ввести одну строку текста.
        self.entry_form_1 = tkinter.Entry(frame_top, width=30, font="Arial 12")
        self.entry_form_2 = tkinter.Entry(frame_top, width=30, font="Arial 12")
        self.entry_form_3 = tkinter.Entry(frame_top, width=30, font="Arial 12")
        # Метод bind привязывает событие к какому-либо действию (нажатие кнопки мыши, нажатие клавиши на клавиатуре).
        self.entry_form_1.bind("<Return>", self.change)
        self.entry_form_2.bind("<Return>", self.change)
        self.entry_form_3.bind("<Return>", self.change)
        self.entry_form_1.focus()

        self.check_button = tkinter.Button(frame_top, text="Проверить", width=10, height=1, font="Arial 12")
        self.check_button.config(command=self.change)

        close_button = tkinter.Button(text="Close", font="Arial 12")
        close_button.config(command=master.close_button_func)

        self.info_label.pack(side=tkinter.BOTTOM, padx=10, pady=10)
        self.example_text.pack(padx=10)
        self.example_question.pack(padx=10)

        self.label.pack(side=tkinter.LEFT, padx=10, pady=10)
        self.entry_form_1.pack(side=tkinter.TOP, padx=10, pady=10)
        self.entry_form_2.pack(side=tkinter.BOTTOM, padx=10, pady=10)
        self.entry_form_3.pack(side=tkinter.BOTTOM, padx=10, pady=10)
        self.check_button.pack(side=tkinter.RIGHT, padx=10, pady=10)
        close_button.place(relx=0.90, rely=0.90)

        self.timer = tkinter.Label(self, text="%s:%s:%s" % (HOUR, MINUTE, SECOND), font=("Consolas", 14), fg='white',
                                   background=master.background_color)
        self.timer.pack()
        self.timer.after_idle(self.tick)

    def change(self, event=None):
        """
        Проверка введенного пользователем значения перевода
        """

        global MISTAKE
        key = self.label['text']
        key_result = self.master.irregular_verbs_dict.get(key, {})

        translate_form_1 = key_result.get('translate', '').lower()
        translate_form_2 = key_result.get('form_2', '').lower()
        translate_form_3 = key_result.get('form_3', '').lower()
        answer_form_1 = self.entry_form_1.get().lower()
        answer_form_2 = self.entry_form_2.get().lower()
        answer_form_3 = self.entry_form_3.get().lower()
        print(answer_form_1, ' -> ', translate_form_1)
        print(answer_form_2, ' -> ', translate_form_2)
        print(answer_form_3, ' -> ', translate_form_3)
        print()
        if answer_form_1 == translate_form_1 \
                and answer_form_2 == translate_form_2 \
                and answer_form_3 == translate_form_3:
            self.example_text['text'] = key_result.get('example_text')

            # если примера текста нет, то в верхний блок примеров встанет вопрос
            if not self.example_text['text']:
                self.example_text['text'] = key_result.get('example_question')
            else:
                self.example_question['text'] = key_result.get('example_question')

            self.info_label['text'] = 'I knew you could do it!'
            self.info_label.config(fg='white')
            self.entry_form_1.config(fg='black')
            self.entry_form_2.config(fg='black')
            self.entry_form_3.config(fg='black')

            # Если пользователь совершил ошибку, слово не считается пройденным
            if not MISTAKE:
                del self.master.irregular_verbs_dict[key]
            MISTAKE = False

            if not self.master.irregular_verbs_dict:
                root.after(5000, root.quit())

            # Если есть текстовый пример, то следующее тестовое слово появится через 3 сек.
            if self.example_text['text']:
                self.check_button.after(3000, self.new_text_message)
            else:
                self.new_text_message()
            self.entry_form_1.delete(0, tkinter.END)
            self.entry_form_2.delete(0, tkinter.END)
            self.entry_form_3.delete(0, tkinter.END)
        else:
            MISTAKE = True
            self.entry_form_1.config(fg='#CC3366')
            self.entry_form_2.config(fg='#CC3366')
            self.entry_form_3.config(fg='#CC3366')
            self.info_label['text'] = 'Turn on your brain!'
            self.info_label.config(fg='#993333')

    def new_text_message(self):
        self.label['text'] = random.choice(list(self.master.irregular_verbs_dict.keys()))

    def tick(self):
        global SECOND, MINUTE, HOUR
        # Через каждую секунду происходит рекурсивый вызов функции
        self.timer.after(1000, self.tick)
        SECOND += 1
        if SECOND == 59:
            MINUTE += 1
            SECOND = -1
        elif MINUTE == 59:
            HOUR += 1
            MINUTE = -1
        self.timer['text'] = "%s:%s:%s" % (HOUR, MINUTE, SECOND)


if __name__ == '__main__':
    root = SampleApp()
    root.mainloop()

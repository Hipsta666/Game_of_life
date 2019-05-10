from tkinter import filedialog as fd
from tkinter import *
from math import floor
from time import sleep
import numpy


class App(Frame):
    GREEN = '#48ff00'
    BLACK = '#000'
    new_WIDTH = 800
    new_HEIGHT = 800

    def __init__(self, master):
        super(App, self).__init__(master)
        self.grid()
        self.menu()
        self.STOP = False
        self.generation = 1

    def menu(self):
        """
        Построение меню выбора размерности поля.
        """
        self.label = Label(self)
        self.label['text'] = 'Укажите размеры поля: '
        self.label.grid(row=0, column=0, sticky=W)

        self.char_x = Label(self)
        self.char_x['text'] = 'X'
        self.char_x.grid(row=0, column=2, sticky=W)

        self.width_window = Entry(self, width=5)
        self.width_window.grid(row=0, column=1, sticky=W)

        self.height_window = Entry(self, width=5)
        self.height_window.grid(row=0, column=3, sticky=W)

        self.btn_create = Button(self)
        self.btn_create['text'] = 'СОЗДАТЬ ПОЛЕ'
        self.btn_create.grid(row=1, column=0, columnspan=4, sticky=W)
        self.btn_create['command'] = self.w_personal

        self.btn_create_30 = Button(self, width=20)
        self.btn_create_30['text'] = '20x20'
        self.btn_create_30.grid(row=2, column=0, columnspan=4, sticky=W)
        self.btn_create_30['command'] = self.w_20

        self.btn_create_60 = Button(self, width=20)
        self.btn_create_60['text'] = '50x50'
        self.btn_create_60.grid(row=2, column=1, columnspan=4, sticky=W)
        self.btn_create_60['command'] = self.w_50

        self.btn_create_90 = Button(self, width=20)
        self.btn_create_90['text'] = '70x70'
        self.btn_create_90.grid(row=3, column=0, columnspan=4, sticky=W)
        self.btn_create_90['command'] = self.w_70

        self.btn_create_120 = Button(self, width=20)
        self.btn_create_120['text'] = '100x100'
        self.btn_create_120.grid(row=3, column=1, columnspan=4, sticky=W)
        self.btn_create_120['command'] = self.w_100

    def start_field(self, len_side, WIDTH):
        """
        Создание игровой решетки посредством объектов класса Canvas.
        Каждому прямоугольнику-объекту присваивается общий тег и тег индивидуальный,
        для дальнейших манипулаций над цветом. Создание множества живых клеток.
        """
        self.set_alive = set()
        self.w = Canvas(root, width=App.new_WIDTH - 50, height=App.new_HEIGHT - 50)
        self.w.grid()
        for i in range(int(len_side) ** 2):
            row = floor(i / len_side)
            col = i - row * len_side
            self.w.create_rectangle(float(col) * WIDTH, float(row) * WIDTH,
                                    float(col) * WIDTH + WIDTH, float(row) * WIDTH + WIDTH,
                                    fill=App.BLACK, outline='#555666', tags=('all', str(i)))

    def w_personal(self):
        """Функция-обработчик нажатия, установливает персональные размеры поля."""
        self.len_side = int(self.width_window.get())
        self.create_window()

    def w_20(self):
        """Установливает размер поля 20х20."""
        self.len_side = 20
        self.create_window()

    def w_50(self):
        """Установливает размер поля 50х50."""
        self.len_side = 50
        self.create_window()

    def w_70(self):
        """Установливает размер поля 70х70."""
        self.len_side = 70
        self.create_window()

    def w_100(self):
        """Установливает размер поля 100х100."""
        self.len_side = 100
        self.create_window()

    def destroy_elements(self):
        """
        'Закрытие' меню выбора выбора размерности поля.
        """
        self.label.destroy()
        self.char_x.destroy()
        self.width_window.destroy()
        self.height_window.destroy()
        self.btn_create.destroy()
        self.btn_create_30.destroy()
        self.btn_create_60.destroy()
        self.btn_create_90.destroy()
        self.btn_create_120.destroy()

    def create_window(self):
        """
        Создание основного игрового поля, исходя из размеров, которые выбрал пользователь.
        Создание toolbar инструментария и переобозначение(root.bind(..)) левой кнопки мыши
        для дальнейшего вычисления координат нажатия.
        """
        self.WIDTH = (App.new_WIDTH - 50) / self.len_side
        self.HEIGHT = (App.new_WIDTH - 50) / self.len_side

        self.destroy_elements()
        root.geometry(str(App.new_WIDTH) + 'x' + str(App.new_HEIGHT) + "+300+0")

        self.btn_start = Button(self, width=6)
        self.btn_start['text'] = 'Старт'
        self.btn_start.grid(row=0, column=0, sticky=W)
        self.btn_start['command'] = self.start_generations

        self.btn_next = Button(self, width=18)
        self.btn_next['text'] = 'Следующее поколение'
        self.btn_next.grid(row=0, column=1, sticky=W)
        self.btn_next['command'] = self.next_generation

        self.btn_clean = Button(self, width=7)
        self.btn_clean['text'] = 'Очистить'
        self.btn_clean.grid(row=0, column=2, sticky=W)
        self.btn_clean['command'] = self.clean_field

        self.btn_save = Button(self, width=20)
        self.btn_save['text'] = 'Сохранить 1-е поколение'
        self.btn_save.grid(row=0, column=3, sticky=W)
        self.btn_save['command'] = self.save_generation

        self.btn_downloads = Button(self, width=20)
        self.btn_downloads['text'] = 'Загрузить 1-е поколение'
        self.btn_downloads.grid(row=0, column=4, sticky=W)
        self.btn_downloads['command'] = self.load_generation

        self.lbl = Label(self, width=15)
        self.lbl['text'] = 'Поколение: ' + str(self.generation)
        self.lbl.grid(row=0, column=5, sticky=W)

        self.start_field(self.len_side, self.WIDTH)
        root.bind('<Button-1>', self.click)

    def click(self, event):
        """
        Функция-обработчик нажатия левой кнопки мыши, вычисляющая координаты клика и назначающая живые клетки.
        """
        if event.y_root > 67:
            if 5 <= self.w.winfo_pointerx() - self.w.winfo_rootx() <= 750:
                if 5 <= self.w.winfo_pointery() - self.w.winfo_rooty() <= 751:
                    column = int(round(event.x // self.WIDTH))
                    row = int(round(event.y // self.HEIGHT))
                    index = column + row * self.len_side
                    #print('row ' + str(row) + ', ' + 'column ' + str(column))
                    color = self.w.itemcget(str(index + 1), 'fill')
                    if color == App.BLACK:
                        self.w.itemconfig(str(index + 1), fill=App.GREEN)
                        self.set_alive.add(str(index + 1))
                    else:
                        self.w.itemconfig(str(index + 1), fill=App.BLACK)
                        if str(index + 1) in self.set_alive:
                            self.set_alive.remove(str(index + 1))
                    self.for_save = self.set_alive.copy()

    def neighbors_of_alive(self, index, act):
        """
        Добавление соседей клеток.
        """
        if 'LtUp' in act:
            self.set_neighbors_of_alive.add(str(int(index) - self.len_side - 1))
        if 'Up' in act:
            self.set_neighbors_of_alive.add(str(int(index) - self.len_side))
        if 'RtUp' in act:
            self.set_neighbors_of_alive.add(str(int(index) - self.len_side + 1))
        if 'Lt' in act:
            self.set_neighbors_of_alive.add(str(int(index) - 1))
        if 'Rt' in act:
            self.set_neighbors_of_alive.add(str(int(index) + 1))
        if 'LtDn' in act:
            self.set_neighbors_of_alive.add(str(int(index) + self.len_side - 1))
        if 'Dn' in act:
            self.set_neighbors_of_alive.add(str(int(index) + self.len_side))
        if 'RtDn' in act:
            self.set_neighbors_of_alive.add(str(int(index) + self.len_side + 1))

    def add_neighbors(self, index):
        """
        Добавление соседей живых клеток.
        """
        rw = floor((int(index) - 1) / self.len_side)
        cl = (int(index) - 1) - rw * self.len_side
        r = [num for num in range(int(self.len_side))]
        if index == '1':  # left up
            self.neighbors_of_alive(index['Rt', 'Dn', 'RtDn'])

        elif rw == 0 and cl == r[-1]:  # right up
            self.neighbors_of_alive(index, ['Lt', 'Dn', 'LtDn'])

        elif rw == r[-1] and cl == 0:  # left down
            self.neighbors_of_alive(index, ['Up', 'RtUp', 'Rt'])

        elif rw == r[-1] and cl == r[-1]:  # right down
            self.neighbors_of_alive(index, ['Lt', 'Up', 'LtUp'])

        elif rw == 0 and cl != 0 and cl != r[-1]:  # up => (left <-> right)
            self.neighbors_of_alive(index, ['Lt', 'Rt', 'LtDn', 'Dn', 'RtDn'])

        elif rw == r[-1] and cl != 0 and cl != r[-1]:  # down => (left <-> right)
            self.neighbors_of_alive(index, ['Lt', 'Rt', 'LtUp', 'Up', 'RtUp'])

        elif rw != 0 and rw != r[-1] and cl == 0:  # left => (up <-> down)
            self.neighbors_of_alive(index, ['Up', 'RtUp', 'Rt', 'Dn', 'RtDn'])

        elif rw != 0 and rw != r[-1] and cl == r[-1]:  # right => (up <-> down)
            self.neighbors_of_alive(index, ['Up', 'LtUp', 'Lt', 'LtDn', 'Dn'])

        elif rw != 0 and rw != r[-1] and cl != 0 and cl != r[-1]:  # (up <-> down) and (left <-> right)
            self.neighbors_of_alive(index, ['LtUp', 'Up', 'RtUp', 'Lt', 'Rt', 'LtDn', 'Dn', 'RtDn'])

    def counter_generations(self):
        """
        Счётчик поколений, обновляющий label
        '"""
        self.generation += 1
        self.lbl['text'] = 'Поколение: ' + str(self.generation)

    def check(self, index, neighbors, act):
        """
        Функция подсчёта количества живых соседей клетки.
        """
        if 'LtUp' in act and self.w.itemcget(str(int(index) - self.len_side - 1), 'fill') == App.GREEN:
             neighbors += 1
        if 'Up' in act and self.w.itemcget(str(int(index) - self.len_side), 'fill') == App.GREEN:
            neighbors += 1
        if 'RtUp' in act and self.w.itemcget(str(int(index) - self.len_side + 1), 'fill') == App.GREEN:
            neighbors += 1
        if 'Lt' in act and self.w.itemcget(str(int(index) - 1), 'fill') == App.GREEN:
            neighbors += 1
        if 'Rt' in act and self.w.itemcget(str(int(index) + 1), 'fill') == App.GREEN:
            neighbors += 1
        if 'LtDn' in act and self.w.itemcget(str(int(index) + self.len_side - 1), 'fill') == App.GREEN:
            neighbors += 1
        if 'Dn' in act and self.w.itemcget(str(int(index) + self.len_side), 'fill') == App.GREEN:
            neighbors += 1
        if 'RtDn' in act and self.w.itemcget(str(int(index) + self.len_side + 1), 'fill') == App.GREEN:
            neighbors += 1
        return neighbors

    def neighbors(self, index):
        """
        Обновление множества живых клеток, исходя из количества соседей.
        """
        r = [num for num in range(int(self.len_side))]
        rw = floor((int(index) - 1) / self.len_side)
        cl = (int(index) - 1) - rw * self.len_side
        neighbors = 0
        if rw == 0 and cl == 0:  # left up
            neighbors = self.check(index, neighbors, ['Rt', 'Dn', 'RtDn'])

        elif rw == 0 and cl == r[-1]:  # right up
            neighbors = self.check(index, neighbors, ['Lt', 'Dn', 'LtDn'])

        elif rw == r[-1] and cl == 0:  # left down
            neighbors = self.check(index, neighbors, ['Up', 'RtUp', 'Rt'])

        elif rw == r[-1] and cl == r[-1]:  # right down
            neighbors = self.check(index, neighbors, ['Lt', 'Up', 'LtUp'])

        elif rw == 0 and cl != 0 and cl != r[-1]:  # up => (left <-> right)
            neighbors = self.check(index, neighbors, ['Lt', 'Rt', 'LtDn', 'Dn', 'RtDn'])

        elif rw == r[-1] and cl != 0 and cl != r[-1]:  # down => (left <-> right)
            neighbors = self.check(index, neighbors, ['Lt', 'Rt', 'LtUp', 'Up', 'RtUp'])

        elif rw != 0 and rw != r[-1] and cl == 0:  # left => (up <-> down)
            neighbors = self.check(index, neighbors, ['Up', 'RtUp', 'Rt', 'Dn', 'RtDn'])

        elif rw != 0 and rw != r[-1] and cl == r[-1]:  # right => (up <-> down)
            neighbors = self.check(index, neighbors, ['Up', 'LtUp', 'Lt', 'LtDn', 'Dn'])

        elif rw != 0 and rw != [-1] and cl != 0 and cl != r[-1]:  # (up <-> down) and (left <-> right)
            neighbors = self.check(index, neighbors, ['LtUp', 'Up', 'RtUp', 'Lt', 'Rt', 'LtDn', 'Dn', 'RtDn'])

        if self.w.itemcget(index, 'fill') == App.BLACK and neighbors == 3:  # cell alive
            self.set_alive.add(index)
        elif self.w.itemcget(index, 'fill') == App.GREEN and neighbors < 2:  # cell dead
            self.set_alive.add(index)
        elif self.w.itemcget(index, 'fill') == App.GREEN and neighbors > 3:  # cell dead
            self.set_alive.add(index)

    def open_file(self):
        """
        Открытие файла, содержащего состояние 1-го поколения и обновление игрового поля.
        """
        fname = fd.askopenfilename()
        with open(fname) as file:
            file_len = int(file.readlines()[-1])
        if file_len != self.len_side:
            self.lbl['text'] = 'Поля не совпадают!'
        else:
            with open(fname) as file:
                text = file.read()
            self.clean_field()
            c = 0
            string = ''
            for value in text:
                if value != ' ' and value != '\t' and value != '\n':
                    string += value
                    if value == '1':
                        self.set_alive.add(string.index(value, c) + 1)
                    c += 1
            self.update_cell()
            self.generation = 1
            self.lbl['text'] = 'Поколение: 1'

    def save_file(self):
        """
        Сохранение файла, содержащего состояние 1-го поколения.
        """
        fname = fd.asksaveasfilename()
        data = []
        for index in range(int(self.len_side ** 2)):
            if str(index + 1) in self.for_save:
                data.append(1)
            else:
                data.append(0)
        A = numpy.array(data)
        B = A.reshape(-1, self.len_side)
        numpy.savetxt(fname, B, fmt='%d', delimiter='\t')
        with open(fname, 'a') as file:
            file.write(str(self.len_side))

    def exit_app(self):
        """
        Закрытие диалогового окна.
        """
        self.first_item.destroy()

    def file_system(self, action):
        """
        Создание файлового диалога для сохранения файла или для открытия ранее сохранённого файла.
        """
        self.first_item = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label='Файл', menu=self.first_item)
        if action == 'open':
            self.first_item.add_cascade(label='Открыть', command=self.open_file)
        elif action == 'save':
            self.first_item.add_cascade(label='Сохранить', command=self.save_file)
        self.first_item.add_cascade(label='Выйти', command=self.exit_app)
        self.txt = Text(root, width=40, height=15, font=12)
        self.txt.grid()

    def update_cell(self):
        """
        Обновление игрового поля.
        """
        for index in self.set_alive:
            if self.w.itemcget(index, 'fill') == App.GREEN:
                self.w.itemconfig(index, fill=App.BLACK)
            else:
                self.w.itemconfig(index, fill=App.GREEN)

    # Buttons.
    def clean_field(self):
        """
        Функция-обработчик нажатия кнопки очистки поля.
        """
        self.generation = 1
        self.lbl['text'] = 'Поколение: ' + str(self.generation)
        self.set_alive = set()
        self.w.itemconfig('all', fill=App.BLACK)
        self.STOP = True

    def next_generation(self):
        """
        Функция-обработчик нажатия кнопки 'Следующее поколение'. Создание множества всех соседей живых клеток,
        подсчёт количества соседей каждого из соседей, обновление игрового поля.
        """
        self.set_neighbors_of_alive = self.set_alive.copy()
        for cell in self.set_alive:
            self.add_neighbors(str(int(cell)))
        self.set_alive = set()

        for cell in self.set_neighbors_of_alive:
            self.neighbors(str(int(cell)))
        if self.set_alive == set():
            self.lbl['text'] = 'Поколение: ' + str(self.generation)
        else:
            self.counter_generations()
        self.set_neighbors_of_alive = set()
        self.update_cell()
        root.bind('<Button-1>', self.click)

    def start_generations(self):
        """
        Функция-обработчик нажатия кнопки 'Старт'. Зацикливание 'обновления поколения'.
        """
        self.STOP = False
        while not self.STOP:
            self.next_generation()
            sleep(0.065)
            if self.set_alive == set():
                self.STOP = True
            root.update()

    def save_generation(self):
        """
        Функция-обработчик нажатия кнопки 'Сохранить 1-е поколение'.
        """
        self.file_system('save')

    def load_generation(self):
        """
        Функция-обработчик нажатия кнопки 'Загрузить 1-е поколение'.
        """
        self.file_system('open')


root = Tk()
root.title('Game of life')
main_menu = Menu(root)
root['menu'] = main_menu
root.resizable(False, False)
app = App(root)
root.mainloop()









import json
from tkinter import *


class App(Frame):

    def __init__(self, master):
        super(App, self).__init__(master)
        self.grid()
        self.menu()
        self.generation = 1
        self.new_WIDTH = 800
        self.new_HEIGHT = 800

    def menu(self):
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
        self.btn_create['command'] = self.create_window



    def create_window(self):

        self.WIDTH = self.new_WIDTH / int(self.width_window.get())
        self.HEIGHT = self.new_WIDTH / int(self.height_window.get())

        self.label.destroy()
        self.char_x.destroy()
        self.width_window.destroy()
        self.height_window.destroy()
        self.btn_create.destroy()
        root.geometry(str(self.new_WIDTH) + 'x' + str(self.new_HEIGHT) + "+300+0")

        self.w = Canvas(root, width=self.new_WIDTH, height=self.new_HEIGHT)
        len_side = int(self.new_WIDTH / self.WIDTH)
        for i in range(len_side):
            for j in range(len_side):
                self.w.create_rectangle(i * int(self.WIDTH), j * int(self.WIDTH),
                                   i * int(self.WIDTH) + int(self.WIDTH),
                                   j * int(self.WIDTH) + int(self.WIDTH), fill='#000', outline='#555666')
        self.w.grid()

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
        self.btn_save['command'] = self.save_grnrration

        self.btn_downloads = Button(self, width=20)
        self.btn_downloads['text'] = 'Загрузить 1-е поколение'
        self.btn_downloads.grid(row=0, column=4, sticky=W)
        self.btn_downloads['command'] = self.load_generation

        self.lbl = Label(self, width=15)
        self.lbl['text'] = 'Поколение: ' + str(self.generation)
        self.lbl.grid(row=0, column=5, sticky=W)

        root.bind('<Button-1>', self.click)


    def click(self, event):
        if root.winfo_pointerx() > root.winfo_rootx() and root.winfo_pointery() > root.winfo_rooty() and event.y_root > 67:
            x_click = root.winfo_pointerx() - root.winfo_rootx()
            y_click = root.winfo_pointery() - root.winfo_rooty() - 24
            column = int(y_click // self.HEIGHT)
            row = int(x_click // self.WIDTH)
            print('row ' + str(row) + ', ' + 'column ' + str(column))

            cells = []
            with open('f.txt', 'r+') as self.file:
                a = int(self.new_WIDTH / self.WIDTH)                        # количество клеток в строке и столбце
                self.create_generation(self.file, cells, row, column, self.WIDTH, a, self.w)


    @staticmethod
    def create_generation(file, lst, row, column, WIDTH, num_of_cell, draw):
        info = file.read()
        if info == '':
            for rw in range(num_of_cell):
                lst.append([])
                for cl in range(num_of_cell):
                    lst[rw].append(0)
            lst[row][column] = 1
            draw.create_rectangle(row * int(WIDTH), column * int(WIDTH),
                                    row * int(WIDTH) + int(WIDTH),
                                    column * int(WIDTH) + int(WIDTH), fill='#00ff3f')
            draw.grid()
            file.write(json.dumps([lst]))

        else:
            info_json = json.loads(info)
            new_lst = info_json[-1].copy()

            if new_lst[row][column] == 0:
                new_lst[row][column] = 1
                draw.create_rectangle(row * int(WIDTH), column * int(WIDTH),
                                        row * int(WIDTH) + int(WIDTH),
                                        column * int(WIDTH) + int(WIDTH), fill='#00ff3f')
            elif new_lst[row][column] == 1:
                new_lst[row][column] = 0
                draw.create_rectangle(row * int(WIDTH), column * int(WIDTH),
                                        row * int(WIDTH) + int(WIDTH),
                                        column * int(WIDTH) + int(WIDTH),
                                        fill='#000', outline='#555666')
            info_json.append(new_lst)
            with open('f.txt', 'w') as file:
                file.write(json.dumps(info_json))

    def clean_field(self):
        pass

    def next_generation(self):
        pass

    def start_generations(self):
        pass

    def load_generation(self):
        pass

    def save_grnrration(self):
        pass


root = Tk()
root.title('Game of life')
root.resizable(False, False)
app = App(root)


root.mainloop()



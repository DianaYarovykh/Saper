from tkinter import *
from tkinter import messagebox
import pickle
from random import choice

def enter():

    root = Tk()
    root.geometry("600x600")
    root.title("Вход в систему")

    button_regist = Button(text="Зарегистрироваться", command=lambda: registration())
    button_enter = Button(text="Войти", command=lambda: login())

    button_regist.pack()
    button_enter.pack()

    root.mainloop()

def registration():

    text = Label (text = "Для того чтобы начать игру - зарегистрируйтесь!")
    text_log = Label(text = "Введите логин: ")
    registr_login = Entry()
    text_password1 = Label(text = "Введите пароль: ")
    registr_password1 = Entry()
    text_password2 = Label(text = "Введите пароль ещё раз: ")
    registr_password2 = Entry(show="*")
    button_regist = Button(text = "Зарегистрироваться", command=lambda: save())
    global filename
    filename = registr_login.get()

    text.pack()
    text_log.pack()
    registr_login.pack()
    text_password1.pack()
    registr_password1.pack()
    text_password2.pack()
    registr_password2.pack()
    button_regist.pack()

    def save():

        login_pass_save = {}
        login_pass_save[registr_login.get()] = registr_password1.get()
        f  = open("login.txt", "wb")
        users = open("users.txt", "wb")
        pickle.dump(registr_login.get(), users)
        pickle.dump(login_pass_save, f)
        users.close()
        f.close()
        startGame()

def login():

    text_enter_login = Label(text  = "Введите логин: ")
    enter_login = Entry()
    text_enter_pass = Label(text = "Введите пароль: ")
    enter_password = Entry(show="*")
    button_enter = Button(text="Войти", command=lambda: log_pass())
    global filename
    filename = enter_login.get()

    text_enter_login.pack()
    enter_login.pack()
    text_enter_pass.pack()
    enter_password.pack()
    button_enter.pack()


    def log_pass():
        f = open("login.txt", "rb")
        a = pickle.load(f)
        f.close()
        if enter_login.get() in a:
            if enter_password.get() == a[enter_login.get()]:
                startGame()
            else:
                messagebox.showerror("Ошибка!", "Вы ввели неверный пароль")
        else:
            messagebox.showerror("Ошибка!", "Вы ввели неверный логин")


def startGame():
    class Pole(object):
        def __init__(self, master, row, column):
            self.button = Button(master, text="   ", background="yellow")
            self.mine = False
            self.value = 0
            self.viewed = False
            self.flag = 0
            self.around = []
            self.clr = 'black'
            self.bg = None
            self.row = row
            self.column = column


        def viewAround(self):
            return self.around

        def setAround(self):
            if self.row == 0:
                self.around.append([self.row + 1, self.column])
                if self.column == 0:
                    self.around.append([self.row, self.column + 1])
                    self.around.append([self.row + 1, self.column + 1])
                elif self.column == len(buttons[self.row]) - 1:
                    self.around.append([self.row, self.column - 1])
                    self.around.append([self.row + 1, self.column - 1])
                else:
                    self.around.append([self.row, self.column - 1])
                    self.around.append([self.row, self.column + 1])
                    self.around.append([self.row + 1, self.column + 1])
                    self.around.append([self.row + 1, self.column - 1])
            elif self.row == len(buttons) - 1:
                self.around.append([self.row - 1, self.column])
                if self.column == 0:
                    self.around.append([self.row, self.column + 1])
                    self.around.append([self.row - 1, self.column + 1])
                elif self.column == len(buttons[self.row]) - 1:
                    self.around.append([self.row, self.column - 1])
                    self.around.append([self.row - 1, self.column - 1])
                else:
                    self.around.append([self.row, self.column - 1])
                    self.around.append([self.row, self.column + 1])
                    self.around.append([self.row - 1, self.column + 1])
                    self.around.append([self.row - 1, self.column - 1])
            else:
                self.around.append([self.row - 1, self.column])
                self.around.append([self.row + 1, self.column])
                if self.column == 0:
                    self.around.append([self.row, self.column + 1])
                    self.around.append([self.row + 1, self.column + 1])
                    self.around.append([self.row - 1, self.column + 1])
                elif self.column == len(buttons[self.row]) - 1:
                    self.around.append([self.row, self.column - 1])
                    self.around.append([self.row + 1, self.column - 1])
                    self.around.append([self.row - 1, self.column - 1])
                else:
                    self.around.append([self.row, self.column - 1])
                    self.around.append([self.row, self.column + 1])
                    self.around.append([self.row + 1, self.column + 1])
                    self.around.append([self.row + 1, self.column - 1])
                    self.around.append([self.row - 1, self.column + 1])
                    self.around.append([self.row - 1, self.column - 1])

        def view(self, event):
            if mines == []:
                seter(0, self.around, self.row, self.column)
            if self.value == 0:
                self.clr = 'yellow'
                self.value = None
                self.bg = 'green'
            elif self.value == 1:
                self.clr = 'black'
            elif self.value == 2:
                self.clr = 'blue'
            elif self.value == 3:
                self.clr = 'red'
            elif self.value == 4:
                self.clr = 'purple'
            elif self.value == 5:
                self.clr = 'pink'
            elif self.value == 6:
                self.clr = 'orange'

            if self.mine and not self.viewed and not self.flag:
                self.button.configure(text='B', bg='red')
                self.viewed = True
                for q in mines:
                    buttons[q[0]][q[1]].view('<Button-1>')
                lose()

            elif not self.viewed and not self.flag:
                self.button.configure(text=self.value, fg=self.clr, bg=self.bg)
                self.viewed = True
                if self.value == None:
                    for k in self.around:
                        buttons[k[0]][k[1]].view('<Button-1>')

        def setFlag(self, event):
            global bom
            if self.flag == 0 and not self.viewed:
                self.flag = 1
                self.button.configure(text="F", bg='orange')
                flags.append([self.row, self.column])
                min_point.append(1)
                bom = sum(min_point)
                bombs_pointer()
            elif self.flag == 1:
                self.flag = 2
                self.button.configure(text="?", bg='white')
                flags.pop(flags.index([self.row, self.column]))
                min_point.pop()
                bom = sum(min_point)
                bombs_pointer()
            elif self.flag == 2:
                self.flag = 0
                self.button.configure(text='   ', bg='yellow')
            if sorted(mines) == sorted(flags) and mines != []:
                winer()


    def lose():
        pointes = 0
        messagebox.showinfo("Игра окончена","Вы проиграли(")
        save_rez(pointes)
        result_exit()
        messagebox.destroy()

    def seter(q, around, row, column):
        if q == bombs:
            for i in buttons:
                for j in i:
                    for k in j.around:
                        if buttons[k[0]][k[1]].mine:
                            buttons[buttons.index(i)][i.index(j)].value += 1
            return
        a = choice(buttons)
        b = choice(a)
        if [buttons.index(a), a.index(b)] not in mines and [buttons.index(a), a.index(b)] not in around and [
            buttons.index(a), a.index(b)] != [row,
                                              column]:
            b.mine = True
            mines.append([buttons.index(a), a.index(b)])
            seter(q + 1, around, row, column)
        else:
            seter(q, around, row, column)

    def winer():
        messagebox.showinfo("Вы выиграли", "Поздравляю!")
        pointes = 100
        result_exit()
        save_rez(pointes)
        messagebox.destroy()

    def cheat():
        for t in mines:
            buttons[t[0]][t[1]].setFlag('<Button-1>')

    def game(high, lenght):
        root = Tk()
        root.title('Сапёр')

        global buttons
        global mines
        global flags
        global min_point
        min_point = []
        flags = []
        mines = []
        buttons = [[Pole(root, row, column) for column in range(high)] for row in
                   range(lenght)]

        for i in buttons:
            for j in i:
                j.button.grid(column=i.index(j), row=buttons.index(i), ipadx=7,
                              ipady=1)
                j.button.bind('<Button-1>', j.view)
                j.button.bind('<Button-3>', j.setFlag)
                j.setAround()
        buttons[0][0].button.bind('<Control-Button-1>', cheat())

        root.resizable(False, False)
        root.mainloop()


    def bombs_pointer():
        text_bomb_lab2.configure(text = bom)



    text_levls = Label(text = "Выберите уровень игры")
    button_lvl_new = Button(text = "Новичок(9x9,10 мин)", command=lambda: newborn())
    button_lvl_like = Button(text = "Любитель(16x16,40 мин)", command= lambda: liker())
    button_lvl_hard = Button(text = "Профессионал(16x30,90 мин)", command=lambda: hardcore())
    exit_but = Button(text= "Выйти", command=lambda: sys.exit())
    global text_bomb_lab2
    text_bomb_lab1 = Label(text="Количество найденых бомб: ")
    text_bomb_lab2 = Label(text="0")

    button_lvl_new.place(x=5, y=5)
    button_lvl_like.place(x=5, y=35)
    button_lvl_hard.place(x=5, y=65)
    text_levls.pack()
    button_lvl_new.pack()
    button_lvl_like.pack()
    button_lvl_hard.pack()
    exit_but.pack()
    text_bomb_lab1.pack()
    text_bomb_lab2.pack()


    def newborn():
        global bombs
        high = 9
        lenght = 9
        bombs = 10
        game(high, lenght)


    def liker():
        global bombs
        high = 16
        lenght = 16
        bombs = 40
        game(high, lenght)


    def hardcore():
        global bombs
        high = 30
        lenght = 16
        bombs = 90
        game(high, lenght)



    def result_exit():

        t = Label(text="      ")
        text_exit = Label(text = "Игра окончена!")
        res_button = Button(text="Посмотреть результаты", command=lambda: rezults())
        t.pack()
        text_exit.pack()
        res_button.pack()


    def save_rez(pointes):
        with open(filename, "wb") as file:
            pickle.dump(pointes)
        file.close()

    def rezults():
        users = open("users.txt", "rb")
        us = pickle.load(users)
        users.close()
        label_u_name = Label(text = us)
        with open(filename, "rb") as file:
            p = pickle.load(filename)
        file.close()
        label_u_point = Label(text = p)
        label_u_name.pack()
        label_u_point.pack()

enter()

import tkinter as tk
from tkinter import ttk
import sqlite3

# Импортируем ttkthemes для настройки стиля виджетов
from ttkthemes import ThemedStyle

# Основной класс для приложения
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db  # Создаем экземпляр базы данных
        self.view_records()  # Отображаем записи из базы данных

    def init_main(self):
        style = ThemedStyle()
        style.set_theme("equilux")

        # Создаем верхнюю панель инструментов
        toolbar = tk.Frame(bg=style.lookup("TFrame", "background"), bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Загружаем изображения для кнопок
        self.add_img = tk.PhotoImage(file='./img/add.png')
        self.upd_img = tk.PhotoImage(file='./img/update.png')
        self.del_img = tk.PhotoImage(file='./img/delete.png')
        self.search_img = tk.PhotoImage(file='./img/search.png')
        self.refresh_img = tk.PhotoImage(file='img/refresh.png')

        # Создаем кнопки на панели инструментов
        btn_open_dialog = tk.Button(toolbar, bg=style.lookup("TButton", "background"),
                                    bd=0, image=self.add_img,
                                    command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        btn_upd_dialog = tk.Button(toolbar, bg=style.lookup("TButton", "background"),
                                   bd=0, image=self.upd_img,
                                   command=self.open_update_dialog)
        btn_upd_dialog.pack(side=tk.LEFT)

        btn_del_dialog = tk.Button(toolbar, bg=style.lookup("TButton", "background"),
                                   bd=0, image=self.del_img,
                                   command=self.delete_record)
        btn_del_dialog.pack(side=tk.LEFT)

        btn_search_dialog = tk.Button(toolbar, bg=style.lookup("TButton", "background"),
                                      bd=0, image=self.search_img,
                                      command=self.open_search_dialog)
        btn_search_dialog.pack(side=tk.LEFT)

        btn_refresh = tk.Button(toolbar, bg=style.lookup("TButton", "background"),
                                bd=0, image=self.refresh_img,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Создаем таблицу для отображения данных
        self.tree = ttk.Treeview(self, columns=['ID', 'name', 'phone', 'email', 'salary'],
                                 height=17, show='headings')

        # Настраиваем стиль выбранных элементов
        style.map("Treeview", background=[("selected", style.lookup("TButton", "background"))])
        self.tree["style"] = "mystyle.Treeview"

        # Настраиваем колонки таблицы
        self.tree.column('ID', width=35, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        # Заголовки колонок
        self.tree.heading('ID', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')
        self.tree.pack(side=tk.LEFT)

        # Полоса прокрутки для таблицы
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод для добавления записи в базу данных
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()  # Обновляем отображение

    # Метод для обновления записи в базе данных
    def update_record(self, name, phone, email, salary):
        row = self.tree.selection()[0]
        if row:
            self.db.c.execute('''
                UPDATE users
                SET name = ?, phone = ?, email = ?, salary = ?
                WHERE id = ?
            ''', (name, phone, email, salary, self.tree.set(row, '#1')))
            self.db.conn.commit()
            self.view_records()  # Обновляем отображение

    # Метод для удаления записи из базы данных
    def delete_record(self):
        selected_rows = self.tree.selection()
        for row in selected_rows:
            self.db.c.execute('DELETE FROM users WHERE id = ?', (self.tree.set(row, '#1'),))
        self.db.conn.commit()
        self.view_records()  # Обновляем отображение

    # Метод для поиска записей в базе данных
    def search_records(self, name):
        self.db.c.execute('SELECT * FROM users WHERE name LIKE ?', ('%' + name + '%',))
        result = self.db.c.fetchall()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for record in result:
            self.tree.insert('', 'end', values=record)

    # Метод для отображения всех записей из базы данных
    def view_records(self):
        self.db.c.execute('SELECT * FROM users')
        result = self.db.c.fetchall()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for record in result:
            self.tree.insert('', 'end', values=record)

    # Метод для открытия диалогового окна добавления записи
    def open_dialog(self):
        Child(self)

    # Метод для открытия диалогового окна редактирования записи
    def open_update_dialog(self):
        selected_row = self.tree.selection()
        if selected_row:
            item_name = self.tree.item(selected_row, 'values')[1]
            item_phone = self.tree.item(selected_row, 'values')[2]
            item_email = self.tree.item(selected_row, 'values')[3]
            item_salary = self.tree.item(selected_row, 'values')[4]
            Update(self, item_name, item_phone, item_email, item_salary)

    # Метод для открытия диалогового окна поиска записей
    def open_search_dialog(self):
        Search(self)

# Диалоговое окно для добавления записи
class Child(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_child()
        self.view = parent

    def init_child(self):
        self.title('Добавление контакта')
        self.geometry('400x200+200+200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Настройки цвета фона и шрифта
        self.configure(bg="#696969")
        label_name = tk.Label(self, text='ФИО:', bg='#696969', fg='white')
        label_name.place(x=50, y=50)

        label_phone = tk.Label(self, text='Телефон:', bg='#696969', fg='white')
        label_phone.place(x=50, y=80)

        label_email = tk.Label(self, text='E-mail:', bg='#696969', fg='white')
        label_email.place(x=50, y=110)

        label_salary = tk.Label(self, text='Зарплата:', bg='#696969', fg='white')
        label_salary.place(x=50, y=140)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=80)

        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=110)

        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.btn_cancel = tk.Button(self, text='Закрыть', bg='gray', command=self.destroy)
        self.btn_cancel.place(x=200, y=170)

        self.btn_ok = tk.Button(self, text='Добавить', bg='gray')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.records(self.entry_name.get(),
                                                                   self.entry_phone.get(),
                                                                   self.entry_email.get(), self.entry_salary.get()))
        self.btn_ok.place(x=300, y=170)

# Диалоговое окно для редактирования записи
class Update(Child):
    def __init__(self, parent, item_name, item_phone, item_email, item_salary):
        super().__init__(parent)
        self.init_edit()
        self.view = parent
        self.load_data(item_name, item_phone, item_email, item_salary)

    def init_edit(self):
        self.configure(bg="#696969")
        self.title('Редактирование контакта')
        btn_edit = tk.Button(self, text='Изменить', bg='gray')
        btn_edit.bind('<Button-1>', lambda ev: self.view.update_record(self.entry_name.get(),
                                                                    self.entry_phone.get(),
                                                                    self.entry_email.get(), self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        btn_edit.place(x=300, y=170)
        self.btn_ok.destroy()

    def load_data(self, name, phone, email, salary):
        self.entry_name.insert(0, name)
        self.entry_phone.insert(0, phone)
        self.entry_email.insert(0, email)
        self.entry_salary.insert(0, salary)

# Диалоговое окно для поиска записей
class Search(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_child()
        self.view = parent

    def init_child(self):
        self.title('Поиск')
        self.geometry('400x200+200+200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Настройки цвета фона и шрифта
        self.configure(bg="#696969")
        label_name = tk.Label(self, text='ФИО:', bg='#696969', fg='white')
        label_name.place(x=50, y=65)
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=65)

        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy, bg='gray')
        self.btn_cancel.place(x=200, y=150)

        self.btn_ok = tk.Button(self, text='Найти', bg='gray')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=300, y=150)

# Класс для работы с базой данных
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('workers.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                phone TEXT,
                                email TEXT,
                                salary TEXT )''')
        self.conn.commit()

    # Метод для добавления записи в базу данных
    def insert_data(self, name, phone, email, salary):
        self.c.execute('''INSERT INTO users (name, phone, email, salary)
                          VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
        self.conn.commit()

# Основная часть приложения
if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('800x425+300+200')
    root.resizable(False, False)
    root.mainloop()
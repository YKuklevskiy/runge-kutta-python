from email import message
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
import csv

def open_table():
    table_window = Toplevel() # новое окно
    screen_size = [table_window.winfo_screenwidth(), table_window.winfo_screenheight()] # размер экрана
    table_window.geometry(f"{screen_size[0]//2}x{screen_size[1]//2}") # размеры окна

    try: # на всякий случай проверяем на ошибки при открытии файла
        table_file = open('solution.csv', mode='r', newline='', encoding="utf-8")
    except OSError:
        messagebox.showerror("Ошибка", "Не удалось обработать файл с таблицей значений. Возможно, доступ к файлу ограничен.")
        return
    
    table_reader = csv.reader(table_file, delimiter=',')
    column_names = next(table_reader) # считали заголовки

    # создаем таблицу и заполняем заголовки
    value_table = Treeview(table_window, show="headings", columns=tuple(column_names))
    for i in range(len(column_names)):
        value_table.column(f"#{i+1}", anchor=CENTER) #anchor=E is a variant
        value_table.heading(f"#{i+1}", text=column_names[i])

    # заполняем данные
    for value_row in table_reader:
        value_table.insert("", END, values=value_row)

    table_file.close()

    
    # слайдеры для прокрутки таблицы
    x_scroll_bar = Scrollbar(table_window, orient='horizontal', command=value_table.xview)
    y_scroll_bar = Scrollbar(table_window, orient='vertical', command=value_table.yview)
    value_table.configure(xscrollcommand=x_scroll_bar.set, yscrollcommand=y_scroll_bar.set)
    
    value_table.grid(row=0, column=0, sticky=N+E+W+S)
    y_scroll_bar.grid(row=0, column=1, sticky=N+S)
    x_scroll_bar.grid(row=1, column=0, columnspan=1, sticky=W+E)
    table_window.rowconfigure(0, weight=1)
    table_window.columnconfigure(0, weight=1)

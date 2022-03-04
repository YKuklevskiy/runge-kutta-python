from tkinter import *
from tkinter import messagebox
import evaluation

# Настройка окна
window = Tk()
window.title('Решение дифференциального уравнения методом Рунге-Кутта')
screen_size = [window.winfo_screenwidth(), window.winfo_screenheight()] # размер экрана
window.geometry(f"{screen_size[0]//3}x{screen_size[1]//3}") # окно на треть экрана

# Чтобы поля были распределены по экрану
for i in range(0, 5):
    window.grid_rowconfigure(i, weight=1)
for i in range(0, 2):
    window.grid_columnconfigure(i, weight=1)

#
# Поля для введения условий задачи
#

# x нулевое
x_0_frame = Frame(window)
x_0_label = Label(x_0_frame, width=20, text="Введите x0: ", anchor='w')
x_0_entry = Entry(x_0_frame)
x_0_entry.insert(END, "2") # исходное значение в моем варианте

x_0_label.grid(column=0, row=0)
x_0_entry.grid(column=0, row=1)


# x n-ное
x_n_frame = Frame(window)
x_n_label = Label(x_n_frame, width=20, text="Введите xn: ", anchor='w')
x_n_entry = Entry(x_n_frame)
x_n_entry.insert(END, "3") # исходное значение в моем варианте

x_n_label.grid(column=0, row=0)
x_n_entry.grid(column=0, row=1)


# y нулевое
y_0_frame = Frame(window)
y_0_label = Label(y_0_frame, width=20, text="Введите y0: ", anchor='w')
y_0_entry = Entry(y_0_frame)
y_0_entry.insert(END, "-0.733026") # исходное значение в моем варианте

y_0_label.grid(column=0, row=0)
y_0_entry.grid(column=0, row=1)


# шаг
step_frame = Frame(window)
step_label = Label(step_frame, width=20, text="Введите шаг: ", anchor='w')
step_entry = Entry(step_frame)
step_entry.insert(END, "0.1") # исходное значение в моем варианте

step_label.grid(column=0, row=0)
step_entry.grid(column=0, row=1)


# аналитическое решение
analytic_bool = BooleanVar()
analytic_bool.set(1)
analytic_check = Checkbutton(window, text="Рисовать на графике аналитическое решение?",
                 variable=analytic_bool, onvalue=1, offvalue=0)

# точность
precision_frame = Frame(window)
precision_bool = BooleanVar()
precision_bool.set(0)
precision_check = Checkbutton(precision_frame, text="Вычислять с адаптивным уточнением сетки?",
                 variable=precision_bool, onvalue=1, offvalue=0)
precision_label = Label(precision_frame, width=20, text="Введите точность: ", anchor='w')
precision_entry = Entry(precision_frame)
precision_entry.insert(END, "0.001") # исходное значение точности


# функция для сокрытия или показания точности
def show_precision_field():
    if precision_bool.get() == False:
        precision_entry.configure(state='readonly')
    else:
        precision_entry.configure(state='normal')

show_precision_field()
precision_check.configure(command=show_precision_field) # привязываем поле с галочкой к функции отображения поля

precision_check.grid(column=0, row=0, rowspan=2)
precision_label.grid(column=1, row=0)
precision_entry.grid(column=1, row=1)


# функция для проверки правильности ввода числа в поле
def is_float(field: str) -> bool:
    try:
        float(field)
        return True
    except ValueError:
        return False

# функция вызываемая по нажатию на кнопку, проверяющая данные 
# и вызывающая решение уравнения с заданными условиями
def plot():
    params = [x_0_entry.get(), x_n_entry.get(), y_0_entry.get(), step_entry.get(), precision_entry.get()] # введенные данные
    if not precision_bool.get():
        params.pop() # убираем точность из передаваемых параметров
    
    for param in params: # проверка введенных данных на корректность
        if not is_float(param):
            messagebox.showerror("Ошибка", "Введенные данные неверны.")
            return

    calculated_data = evaluation.evaluate(*list(map(float, params))) # делаем расчеты
    if calculated_data != None:
        evaluation.plot_window(calculated_data, analytic_bool.get())
    else:
        messagebox.showerror("Ошибка", "Ошибка в вычислениях. Пожалуйста, проверьте вводные данные на корректность.")
    

# кнопка для решения задачи
solve_button = Button(window, text='Генерировать решение', command=plot)

# "выгружение" виджетов в окно
x_0_frame.grid(column=0, row=0)
x_n_frame.grid(column=1, row=0)
y_0_frame.grid(column=0, row=1)
step_frame.grid(column=1, row=1)
analytic_check.grid(column=0, row=2, columnspan=2)
precision_frame.grid(column=0, row=3, columnspan=2)
solve_button.grid(column=0, row=4, columnspan=2)

window.mainloop()
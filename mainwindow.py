from tkinter import *
from tkinter import messagebox

from matplotlib.pyplot import table
import evaluation

# Настройка окна
window = Tk()
window.title('Решение дифференциального уравнения методом Рунге-Кутта')
screen_size = [window.winfo_screenwidth(), window.winfo_screenheight()] # половина размера экрана
window.geometry(f"{screen_size[0]//3}x{screen_size[1]//3}") # окно на треть экрана
# Чтобы поля были распределены по экрану
for i in range(0, 3):
    window.grid_columnconfigure(i, weight=1)
    window.grid_rowconfigure(i, weight=1)

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
    params = [x_0_entry.get(), x_n_entry.get(), y_0_entry.get(), step_entry.get()] # введенные данные
    for param in params: # проверка введенных данных на корректность
        if not is_float(param):
            messagebox.showerror("Ошибка", "Введенные данные неверны.")
            return

    calculated_data = evaluation.evaluate(*list(map(float, params))) # делаем расчеты
    evaluation.plot_window(calculated_data)
    
# кнопка для решения задачи
solve_button = Button(window, text='Генерировать решение', command=plot)

# "выгружение" виджетов в окно
x_0_frame.grid(column=0, row=0)
x_n_frame.grid(column=1, row=0)
y_0_frame.grid(column=0, row=1)
step_frame.grid(column=1, row=1)
solve_button.grid(column=0, row=2, columnspan=2)

window.resizable(0, 0)
window.mainloop()
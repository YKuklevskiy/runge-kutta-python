from typing import List
import runge_kutta_function as rgkt
import math
import numpy as np
import matplotlib.pyplot as plt
import csv
import solution_table

# Функция варианта-18
def function_18(x, y):
    #f(x,y) = y/x + 1/ln|x|
    return float(y)/x + 1/math.log(abs(x))

# Аналитическое решение заданного вариантом уравнения
def analytic_solution_18(x: float, x_0: float, y_0: float) -> float:
    # y = x*ln(ln(|x|))+C*x
    C = float(y_0)/x_0 - math.log(math.log(abs(x_0))) # находим С, удовл. нач. условию
    return float(x)*math.log(math.log(abs(x)))+C*x


# в этих функциях вы выбираете, какие именно функции будут использоваться в программе. То есть, если вы хотите решить 
# другие уравнения, измените функции которые вызываются в return.
def rgkt_sol(x, y):
    return function_18(x, y)
def analytic_sol(x, x_0, y_0):
    return analytic_solution_18(x, x_0, y_0)


# функция вычисляющая таблицу всех значений, требующихся в задаче и возвращающая ее
def evaluate(x_0: float, x_n: float, y_0: float, h: float, eps = -1) -> List[List[float]]:
    # Первые значения нам известны до начала вычислений
    x = [x_0]
    y = [y_0]
    precise_y = [y_0]
    delta = [0]
    x_i = x_0
    last_y_i = y_0 # последнее вычисленное численно значение функции

    try:
        while x_i < x_n and not math.isclose(x_i, x_n):
            temp_h = h
            approximated_y = rgkt.calculate_next_y(x_i, last_y_i, h, rgkt_sol)
            if eps != -1: # разбиение сетки может быть неравномерным, считаем до введенной точности
                while True:
                    temp_y = rgkt.calculate_next_y(x_i, last_y_i, temp_h/2, rgkt_sol)
                    rule_met = abs(approximated_y-temp_y)/15.0 < eps

                    approximated_y = temp_y
                    temp_h = temp_h/2
                    if rule_met:
                        break
            last_y_i = approximated_y

            x_i += temp_h

            # ограничение, для уменьшения количества записей в таблице, если вычисляются очень близкие значения функции 
            if x_i-x[-1] < 0.01 and not math.isclose(x_i, x_n): 
                continue

            real_y = analytic_sol(x_i, x_0, y_0)
            y.append(approximated_y)
            x.append(x_i)
            precise_y.append(real_y)
            delta.append(abs(real_y-approximated_y))
    except (ArithmeticError, ValueError):
        return None
    
    return [x, y, precise_y, delta]

def plot_window(data: List[List[float]], analytic: bool):
    plt.close('all') # закрываем ранее открытые графики

    x_range = np.array(data[0], np.float64)
    y_values = np.array(data[1], np.float64)
    y_precise_values = np.array(data[2], np.float64)

    plt.figure(num="y' = f(x, y), y(x0)=y0")
    plt.title("y=y(x)")
    plt.xlabel("x")
    plt.ylabel("y(x)")
    plt.grid()
    plt.plot(x_range, y_values)

    if analytic: # если рисуем аналитическое решение
        plt.plot(x_range, y_precise_values, label='Аналитическое решение')

    plt.scatter(x_range, y_values, s=5, label='Численное решение', zorder=3) # для точек в месте вычисленных значений
    save_table(data)
    plt.legend()
    plt.show()

def save_table(data: List[List[float]]):
    preciseness_data = data[3] # потом припишем погрешность ее к транспонированному массиву с округленными данными
    entries_count = len(preciseness_data)
    data.pop()

    # т.к. data приходит в "горизонтальном, а не вертикальном виде", транспонируем массивы
    values_data = np.array(data).T.round(6)

    data = np.concatenate((values_data, np.array(preciseness_data).T[:, None]), axis=1).tolist()

    for i in range(entries_count):
        if str(data[i][3]).find("e") > 7:
            data[i][3] = "{:.3e}".format(data[i][3])
            continue
        data[i][3] = "{:6f}".format(data[i][3])

    # меняем отображение погрешности на вид _._*10^n по необходимости
    # for i in range(entries_count):
    #     str_num = str(data[i][3])
    #     if str_num.find("e") == -1:
    #         data[i][3] = "{:6f}".format(data[i][3])
    #         continue
    #     str_num = "{:.1e}".format(data[i][3])
    #     print(str_num)
    #     print(str_num[str_num.find("e")+1:])
    #     exp = int(str_num[str_num.find("e")+1:])
    #     str_num = str_num[:str_num.find("e")] + f"*10^({exp})"
    #     data[i][3] = str_num
        

    column_names = ('xᵢ', 'Числ. решение', 'Аналитич. решение', 'Погрешность')

    table_file = open('solution.csv', mode='w', newline='', encoding="utf-8")
    table_writer = csv.writer(table_file, delimiter=',', quotechar = '"')
    table_writer.writerow(column_names)
    table_writer.writerows(data)
    table_file.close()
    
    solution_table.open_table() # открываем окно, загружающее таблицу из файла и показывающее её


def print_table_console(data: List[List[float]]):
    print('      xᵢ       |          yᵢ         |   Погрешность')
    for i in range(len(data[0])):
        print("{:4.6f}   |   {:4.6f}   |   {:4.6f}".format(data[0], data[1], data[2]))
    print()
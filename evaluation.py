from typing import List
import runge_kutta_function as rgkt
import math
import numpy as np
import matplotlib.pyplot as plt
import csv

# Вариант-18
def function_18(x, y):
    #f(x,y) = y/x + 1/ln|x|
    return float(y)/x + 1/math.log(abs(x))

# Аналитическое решение заданного уравнения
def analytic_solution(x: float, x_0: float, y_0: float) -> float:
    # y = x*ln(ln(|x|))+C*x
    C = float(y_0)/x_0 - math.log(math.log(abs(x_0))) # находим С, удовл. нач. условию
    return float(x)*math.log(math.log(abs(x)))+C*x

# функция вычисляющая таблицу всех значений, требующихся в задаче и возвращающая ее
def evaluate(x_0: float, x_n: float, y_0: float, h: float, eps = -1) -> List[List[float]]:
    # Первые значения нам известны до начала вычислений
    x = [x_0]
    y = [y_0]
    precise_y = [y_0]
    delta = [0]
    x_i = x_0
    
    while x_i < x_n and not math.isclose(x_i, x_n):
        temp_h = h
        approximated_y = rgkt.calculate_next_y(x_i, y[-1], h, function_18)
        if eps != -1: # разбиение сетки может быть неравномерным, считаем до введенной точности
            while True:
                temp_y = rgkt.calculate_next_y(x_i, y[-1], temp_h/2, function_18)
                rule_met = abs(approximated_y-temp_y)/15.0 < eps

                approximated_y = temp_y
                temp_h = temp_h/2
                if rule_met:
                    break
        
        x_i += temp_h
        real_y = analytic_solution(x_i, x_0, y_0)
        y.append(approximated_y)
        x.append(x_i)
        precise_y.append(real_y)
        delta.append(abs(real_y-approximated_y))
    
    return [x, y, precise_y, delta]

def plot_window(data: List[List[float]]):
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
    plt.plot(x_range, y_precise_values)
    plt.scatter(x_range, y_values, s=4) # для точек в месте вычисленных значений
    save_table(data)
    plt.show()

def save_table(data: List[List[float]]):
    preciseness_data = data[3] # потом припишем погрешность ее к транспонированному массиву с округленными данными
    data.pop()

    # т.к. data приходит в "горизонтальном, а не вертикальном виде", транспонируем массивы
    values_data = np.array(data).T.round(6)

    data = np.concatenate((values_data, np.array(preciseness_data).T[:, None]), axis=1).tolist()
    column_names = ('xᵢ', 'yᵢ', 'yᵢ полученное аналитически', 'Погрешность численного решения')

    table_file = open('solution.csv', mode='w', newline='', encoding="utf-8")
    table_writer = csv.writer(table_file, delimiter=',', quotechar = '"')
    table_writer.writerow(column_names)
    table_writer.writerows(data)
    table_file.close()


def print_table_console(data: List[List[float]]):
    print('      xᵢ       |          yᵢ         |   Погрешность')
    for i in range(len(data[0])):
        print("{:4.6f}   |   {:4.6f}   |   {:4.6f}".format(data[0], data[1], data[2]))
    print()
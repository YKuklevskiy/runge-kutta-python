from typing import List
import runge_kutta_functions as rgkt
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
    return float(x_0)*math.log(math.log(abs(x)))+C*x

def evaluate(x_0: float, x_n: float, y_0: float, h: float) -> List[List[float]]:
    x = [x_0]
    y = [y_0]
    delta = [0]
    x_i = x_0
    
    while x_i < x_n and not math.isclose(x_i, x_n):
        approximated_y = rgkt.calculate_next_y(x_i, y[-1], h, function_18)
        x_i += h
        real_y = analytic_solution(x_i, x_0, y_0)
        y.append(approximated_y)
        x.append(x_i)
        delta.append(abs(real_y-approximated_y))
    
    return [x, y, delta]

def plot_window(data: List[List[float]]):
    plt.close('all') # закрываем ранее открытые графики

    x_range = np.array(data[0], np.float64)
    y_values = np.array(data[1], np.float64)

    plt.figure(num="y' = f(x, y), y(x0)=y0")
    plt.title("y=y(x)")
    plt.xlabel("x")
    plt.ylabel("y(x)")
    plt.grid()
    plt.plot(x_range, y_values)
    plt.scatter(x_range, y_values, s=10) # для точек в месте вычисленных значений
    save_table(data)
    plt.show()

def save_table(data: List[List[float]]):
    # т.к. data приходит в "горизонтальном, а не вертикальном виде", транспонируем массивы
    data = np.array(data).T.round(6).tolist()
    column_names = ('xᵢ', 'yᵢ', 'Погрешность численного решения')

    table_file = open('solution.csv', mode='w', newline='')
    table_writer = csv.writer(table_file, delimiter=',', quotechar = '"')
    table_writer.writerow(column_names)
    table_writer.writerows(data)


def print_table_console(data: List[List[float]]):
    print('      xᵢ       |          yᵢ         |   Погрешность')
    for i in range(len(data[0])):
        print("{:4.6f}   |   {:4.6f}   |   {:4.6f}".format(data[0], data[1], data[2]))
    print()
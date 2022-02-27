from typing import List
import runge_kutta_functions as rgkt
import math
import numpy as np
import matplotlib.pyplot as plt

# Вариант-18
def function_18(x, y):
    #f(x,y) = y/x + 1/ln|x|
    return float(y)/x + 1/math.log(abs(x))

def evaluate(x_0: float, x_n: float, y_0: float, h: float) -> List[List[float]]:
    x = [x_0]
    y = [y_0]
    x_i = x_0
    while(x_i < x_n):
        new_y = rgkt.calculate_next_y(x_i, y[-1], h, function_18)
        x_i += h
        y.append(new_y)
        x.append(x_i)

    return x, y

def plot_graph(x: List[float], y: List[float]):
    plt.close('all') # закрываем ранее открытые графики

    x_range = np.array(x, np.float64)
    y_values = np.array(y, np.float64)

    plt.figure(num="y' = f(x, y), y(x0)=y0")
    plt.title("y=y(x)")
    plt.xlabel("x")
    plt.ylabel("y(x)")
    plt.grid()
    plt.plot(x_range, y_values)
    plt.show()

def print_table_console(x: List[float], y: List[float]):
    for i in range(len(x)):
        print("{:8.6f} - {:8.6f}".format(x[i], y[i]))
    print()
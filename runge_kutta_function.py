import types

# имеем уравнение вида y'=f(x,y)

# вычисление y_{i+1} значения для функции function(x, y) методом Рунге-Кутта 4 порядка точности
def calculate_next_y(x_i: float, y_i: float, h: float, function: types.FunctionType) -> float:
    k1 = function(x_i, y_i)
    k2 = function(x_i+h/2, y_i+h/2*k1)
    k3 = function(x_i+h/2, y_i+h/2*k2)
    k4 = function(x_i+h, y_i+h*k3)

    y_i_plus_1 = y_i + h*(k1+2*k2+2*k3+k4)/6.0 # основная формула
    return y_i_plus_1

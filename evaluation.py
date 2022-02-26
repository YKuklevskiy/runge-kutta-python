import runge_kutta_functions as rgkt
import math

# Вариант-18
def function_18(x, y):
    #f(x,y) = y/x + 1/ln|x|
    return float(y)/x + 1/math.log(abs(x))

x_begin = 2
x_end = 3
y_begin = -0.733026
step = 0.1
x = [x_begin]
y = [y_begin]
x_i = x_begin
while(x_i <= x_end):
    new_y = rgkt.calculate_next_y(x_i, y[-1], step, function_18)
    x_i += step
    y.append(new_y)
    x.append(x_i)

for i in range(len(x)):
    print("{:8.6f} - {:8.6f}".format(x[i], y[i]))
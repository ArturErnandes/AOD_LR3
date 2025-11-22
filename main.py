import json
import math
from colorama import Fore, init
import matplotlib.pyplot as plt


DATA_FILE = "data.json"


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8-sig") as data_file:
        data = json.load(data_file)
    return data


def f(x, y):
    return x * math.exp(-x**2) - 2 * x * y


def y_analytic(x):
    return math.exp(-x**2) * (1 + x**2 / 2)


def euler_solve(data):
    a = data["begin"]
    b = data["end"]
    h = data["h"]
    y0 = data["y0"]

    x = a
    n_steps = int((b - a) / h)

    result = [(x, y0)]

    for _ in range(n_steps):
        y0 = y0 + h * f(x, y0)
        x = x + h
        result.append((x, y0))

    return result


def runge_kutta_solve(data):
    a = data["begin"]
    b = data["end"]
    h = data["h"]
    y0 = data["y0"]

    x = a
    n_steps = int((b - a) / h)

    result = [(x, y0)]

    for _ in range(n_steps):
        k1 = h * f(x, y0)
        k2 = h * f(x + h/2, y0 + k1/2)
        k3 = h * f(x + h/2, y0 + k2/2)
        k4 = h * f(x + h, y0 + k3)

        y0 = y0 + (k1 + 2*k2 + 2*k3 + k4) / 6
        x = x + h

        result.append((x, y0))

    return result


def graphic_maker(points, name):
    x, y = zip(*points)

    plt.plot(x, y, label=name)
    plt.xlabel("Значения x")
    plt.ylabel("Значения y")
    plt.grid(True)
    plt.legend()


def main():
    data = load_data()
    print(f"{Fore.LIGHTBLUE_EX}Исходные данные\n\n{Fore.WHITE}Отрезок: [{data['begin']}, {data['end']}]\nh: {data['h']}\ny0: {data['y0']}")

    print(f"\n\n{Fore.GREEN}Метод Эйлера")
    euler_result = euler_solve(data)
    print(euler_result)

    print(f"\n\n{Fore.GREEN}Метод Рунге-Кутта 4 порядка")
    runge_kutta_result = runge_kutta_solve(data)
    print(runge_kutta_result)

    print(f"\n\n{Fore.GREEN}Аналитическое значение y(x)")
    y_b = y_analytic(data['end'])
    analytic_result = [(x, y_analytic(x)) for x, _ in euler_result]
    print(f"y(b) = y({data['end']}) = {y_b:.4f}")

    euler_error = abs(euler_result[-1][-1] - y_b)
    runge_kutta_error = abs(runge_kutta_result[-1][-1] - y_b)

    print(f"\n\n{Fore.GREEN}Погрешности\n")
    print(f"Погрешность метода Эйлера: {Fore.LIGHTRED_EX}{euler_error:.4f}")
    print(f"Погрешность метода Рунге-Кутта: {Fore.LIGHTRED_EX}{runge_kutta_error:.6f}")

    print(f"\n\n{Fore.GREEN}Графики\n")

    plt.figure("Графики")
    graphic_maker(analytic_result, "График аналитической функции f(x)")
    graphic_maker(euler_result, "График приближенных значений по методу Эйлера")
    graphic_maker(runge_kutta_result, "График приближенных значений по методу Рунге-Кутта")
    plt.title("Графики")
    plt.show()


if __name__ == "__main__":
    init(autoreset=True)
    main()
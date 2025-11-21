import json
import math
from colorama import Fore, init

g = 9.81


def load_data(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def f(x1, x2, v1, v2, k):
    v = math.sqrt(v1**2 + v2**2)
    return (
        v1,
        v2,
        -k * v * v1,
        -k * v  * v2 - g
    )


def rk4_step(x1, x2, v1, v2, h, k):
    k1 = f(x1, x2, v1, v2, k)

    k2 = f(
        x1 + 0.5 * h * k1[0],
        x2 + 0.5 * h * k1[1],
        v1 + 0.5 * h * k1[2],
        v2 + 0.5 * h * k1[3],
        k
    )

    k3 = f(
        x1 + 0.5 * h * k2[0],
        x2 + 0.5 * h * k2[1],
        v1 + 0.5 * h * k2[2],
        v2 + 0.5 * h * k2[3],
        k
    )

    k4 = f(
        x1 + h * k3[0],
        x2 + h * k3[1],
        v1 + h * k3[2],
        v2 + h * k3[3],
        k
    )

    x1_new = x1 + h/6*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
    x2_new = x2 + h/6*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
    v1_new = v1 + h/6*(k1[2] + 2*k2[2] + 2*k3[2] + k4[2])
    v2_new = v2 + h/6*(k1[3] + 2*k2[3] + 2*k3[3] + k4[3])

    return x1_new, x2_new, v1_new, v2_new


def solve(k, data, title):
    print(Fore.GREEN + f"\nРешение методом Рунге–Кутты: {title}")

    h = 1
    t_max = 150

    # Начальные условия
    x1 = 0
    x2 = 0
    v0 = data["v_0"]
    alpha = math.radians(data["alpha"])

    v1 = v0 * math.cos(alpha)
    v2 = v0 * math.sin(alpha)

    T, X1, X2 = [], [], []

    for t in range(t_max + 1):
        T.append(t)
        X1.append(x1)
        X2.append(x2)

        x1, x2, v1, v2 = rk4_step(x1, x2, v1, v2, h, k)

    for i in range(0, len(T), 10):
        print(f"t={T[i]:3d}   x1={X1[i]:10.2f}   x2={X2[i]:10.2f}")
    return T, X1, X2


def main():
    data = load_data("data.json")

    ro = data["ro"]
    c = data["c"]
    ro_chugun = data["ro_chugun"]
    d = data["d"]

    S = math.pi * d**2 / 4
    V = math.pi * d**3 / 6
    m = ro_chugun * V

    k_b = c * ro * S / (2 * m)

    solve(k=0, data=data, title="(a) k = 0")

    solve(k=k_b, data=data, title=f"(б) k = {k_b:.6e}")


if __name__ == "__main__":
    init(autoreset=True)
    main()

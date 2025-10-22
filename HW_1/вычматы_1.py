import math

DELTA_T = 1e-3

def maclaurin_exp(t, n):
    """Частичная сумма ряда Маклорена для e^t"""
    s = 0
    for k in range(n + 1):
        s += t**k / math.factorial(k)
    return s

def maclaurin_sin(t, n):
    """Частичная сумма ряда Маклорена для sin(t)"""
    s = 0
    for k in range(n + 1):
        s += ((-1)**k) * (t**(2*k + 1)) / math.factorial(2*k + 1)
    return s

def find_min_n(func_maclaurin, func_true, t_values, delta):
    """Находит минимальное n, при котором ошибка < delta на всех t"""
    n = 0
    while True:
        max_err = max(abs(func_true(t) - func_maclaurin(t, n)) for t in t_values)
        if max_err < delta:
            return n, max_err
        n += 1
        if n > 100:  # защита от зацикливания
            break
    return None, None

intervals = {
    "[0, 1]": [i / 100 for i in range(0, 101)],
    "[10, 11]": [10 + i / 100 for i in range(0, 101)]
}

for func_name, (f_true, f_mac) in {
    "sin(t)": (math.sin, maclaurin_sin),
    "e^t": (math.exp, maclaurin_exp)
}.items():
    print(f"\nФункция {func_name}:")
    for name, t_vals in intervals.items():
        n, err = find_min_n(f_mac, f_true, t_vals, DELTA_T)
        print(f"  На отрезке {name}: минимальное n = {n}, max ошибка = {err:.2e}")


def taylor_exp_around(t, a, n):
    """Ряд Тейлора e^t около точки a"""
    return math.exp(a) * maclaurin_exp(t - a, n)

def taylor_sin_around(t, a, n):
    """Ряд Тейлора sin(t) около точки a"""
    # sin(t) = sin(a) + cos(a)*(t-a) - sin(a)*(t-a)^2/2! - cos(a)*(t-a)^3/3! + ...
    s = 0
    for k in range(n + 1):
        if k % 4 == 0:
            coef = math.sin(a)
            sign = 1
        elif k % 4 == 1:
            coef = math.cos(a)
            sign = 1
        elif k % 4 == 2:
            coef = math.sin(a)
            sign = -1
        else:
            coef = math.cos(a)
            sign = -1
        s += sign * coef * (t - a)**k / math.factorial(k)
    return s

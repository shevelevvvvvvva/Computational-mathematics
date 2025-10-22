import numpy as np
import matplotlib.pyplot as plt
import math

x_circle = np.linspace(-1, 1, 400)
y_circle_pos = np.sqrt(1 - x_circle**2)
y_circle_neg = -np.sqrt(1 - x_circle**2)

x_tan = np.linspace(-1.3, 1.3, 800)
y_tan = np.tan(x_tan)
y_tan[np.abs(y_tan) > 5] = np.nan

plt.figure(figsize=(8, 8))
plt.plot(x_circle, y_circle_pos, 'b', label='$x^2 + y^2 = 1$')
plt.plot(x_circle, y_circle_neg, 'b')
plt.plot(x_tan, y_tan, 'r', label='$y = \\tan(x)$')

plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.title("Графическое отделение и определение корней системы")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.legend()


epsilon = 1e-6


def f(x):
    return x**2 + math.tan(x)**2 - 1

intervals = [(-0.7, -0.6), (0.6, 0.7)]
roots = []

for (a, b) in intervals:
    while (b - a) > epsilon:
        c = (a + b) / 2
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    roots.append((a + b) / 2)

for x_root in roots:
    y_root = math.tan(x_root)
    plt.scatter(x_root, y_root, color='green', s=80, zorder=5, label='Корень')
    plt.text(x_root + 0.05, y_root, f"({x_root:.3f}, {y_root:.3f})", fontsize=9, color='green')

plt.show()

for i, x_root in enumerate(roots, 1):
    y_root = math.tan(x_root)
    print(f"{i}. x = {x_root:.6f}, y = {y_root:.6f}")


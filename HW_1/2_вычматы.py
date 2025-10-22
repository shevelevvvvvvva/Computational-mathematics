import math
import matplotlib.pyplot as plt

fm = 1 / math.sqrt(2 * math.e)
eps = 0.001
q1 = 0.5
q2 = 0.26

def phi1(x):
    return fm * math.exp(x * x / 2)

def phi2(x):
    return math.sqrt(math.log(2 * x / fm))

def f(x):
    return x * math.exp(-x * x)

x1 = 0.1
x2 = 1.0

xnp1 = phi1(x1)
while abs(xnp1 - x1) > eps * (1 - q1) / 2:
    x1 = xnp1
    xnp1 = phi1(x1)
x1 = xnp1

xnp1 = phi2(x2)
while abs(xnp1 - x2) > eps * (1 - q2) / 2:
    x2 = xnp1
    xnp1 = phi2(x2)
x2 = xnp1


print(f"fm = {fm:.6f}")
print(f"x1 = {x1:.6f}, x2 = {x2:.6f}, ширина = {x2 - x1:.6f}")

xs = [i / 100 for i in range(0, 400)]  #x от 0 до 4
ys = [f(x) for x in xs]
f_half = fm / 2

plt.figure(figsize=(8, 5))
plt.plot(xs, ys, label="f(x) = x e^{-x^2}", color="blue")
plt.axhline(f_half, color="red", linestyle="--", label="f = f_m / 2")
plt.scatter([x1, x2], [f(x1), f(x2)], color="green", label="x1, x2 (полувысота)")
plt.title("Ширина функции f(x) = x e^{-x^2} на полувысоте")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()


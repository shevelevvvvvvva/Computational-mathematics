import numpy as np
import matplotlib.pyplot as plt

years = np.array([1910,1920,1930,1940,1950,1960,1970,1980,1990,2000], dtype=float)
population = np.array([
    92228496,106021537,123202624,132164569,151325798,
    179323175,203211926,226545805,248709873,281421906
], dtype=float)

true_2010 = 308745538.0  # точное значение


x = (years - 1910) / 10.0   # теперь узлы 0,1,...,9
y = population.copy()
n = len(x)
t2010 = (2010 - 1910)/10.0  # = 10


dd = np.zeros((n, n))
dd[:, 0] = y
for j in range(1, n):
    for i in range(n - j):
        dd[i, j] = (dd[i+1, j-1] - dd[i, j-1]) / (x[i+j] - x[i])
b = dd[0, :n].copy()  # коэффициенты Ньютона (b0,b1,...)


poly = np.poly1d([0.0])
for k in range(n):
    term = np.poly1d([1.0])
    for j in range(k):
        term *= np.poly1d([1.0, -x[j]])
    term *= b[k]
    poly += term


P2010 = poly(t2010)
error_poly = P2010 - true_2010
rel_error_poly = error_poly / true_2010 * 100


print(f"P(2010) = {P2010:.0f}")
print(f"Ошибка = {error_poly:.0f} ({rel_error_poly:.2f} %)")


h = np.diff(x)
n = len(x)

# Составляем систему для вторых производных M
m = n - 2  # внутренние узлы
A = np.zeros((m, m))
rhs = np.zeros(m)

for i in range(1, n - 1):
    idx = i - 1
    A[idx, idx] = 2 * (h[i - 1] + h[i])
    if idx - 1 >= 0:
        A[idx, idx - 1] = h[i - 1]
    if idx + 1 < m:
        A[idx, idx + 1] = h[i]
    rhs[idx] = 6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])

M_internal = np.linalg.solve(A, rhs)
M = np.zeros(n)
M[1:-1] = M_internal  # вторые производные

# Коэффициенты сплайна на каждом интервале [x_i, x_{i+1}]
spline_coeffs = []
for i in range(n - 1):
    xi, xi1 = x[i], x[i + 1]
    yi, yi1 = y[i], y[i + 1]
    hi = h[i]
    Mi, Mi1 = M[i], M[i + 1]

    # стандартная форма: S_i(x) = a + b*(x - xi) + c*(x - xi)^2 + d*(x - xi)^3
    a = yi
    b = (yi1 - yi) / hi - (2 * Mi + Mi1) * hi / 6
    c = Mi / 2
    d = (Mi1 - Mi) / (6 * hi)
    spline_coeffs.append((xi, a, b, c, d))

def spline_eval(x0, spline_coeffs, nodes):
    # поиск интервала
    if x0 <= nodes[0]:
        xi, a,b,c,d = spline_coeffs[0]
        dx = x0 - xi
        return a + b*dx + c*dx**2 + d*dx**3
    if x0 >= nodes[-1]:
        xi, a,b,c,d = spline_coeffs[-1]
        dx = x0 - xi
        return a + b*dx + c*dx**2 + d*dx**3
    for i in range(len(spline_coeffs)):
        xi, a,b,c,d = spline_coeffs[i]
        if nodes[i] <= x0 <= nodes[i+1]:
            dx = x0 - xi
            return a + b*dx + c*dx**2 + d*dx**3
    return None

S2010 = spline_eval(t2010, spline_coeffs, x)
error_spline = S2010 - true_2010
rel_error_spline = error_spline / true_2010 * 100

print(f"S(2010) = {S2010:.0f}")
print(f"Ошибка = {error_spline:.0f} ({rel_error_spline:.2f} %)")

if abs(error_spline) < abs(error_poly):
    print("Сплайн дал более точный результат.")
else:
    print("Полином Ньютона оказался точнее.")


tt = np.linspace(0, 10, 200)
yy_poly = poly(tt)
yy_spline = np.array([spline_eval(t, spline_coeffs, x) for t in tt])

plt.figure(figsize=(10,6))
plt.plot(1910+10*x, y, 'o', label='Данные переписи')
plt.plot(1910+10*tt, yy_poly, '--', label='Полином Ньютона')
plt.plot(1910+10*tt, yy_spline, '-', label='Кубический сплайн')
plt.axvline(2010, color='gray', linestyle=':')
plt.scatter(2010, true_2010, color='red', zorder=5, label='Реальное значение (2010)')
plt.legend()
plt.xlabel('Год')
plt.ylabel('Численность населения, чел.')
plt.title('Интерполяция и экстраполяция численности населения США')
plt.grid(True)
plt.show()
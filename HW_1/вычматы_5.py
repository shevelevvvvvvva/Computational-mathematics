import math
#y = sin(100x) * e^(-x^2) * cos(2x)

a = 0.0
b = 3.0

N = 10000

dx = (b - a) / N

#Метод прямоугольника
total_integral_rect = 0.0
for i in range(N):
    x = a + i * dx + dx / 2.0
    y = math.sin(100 * x) * math.exp(-x ** 2) * math.cos(2 * x)
    total_integral_rect += y * dx

print(f"Метод прямоугольников: {total_integral_rect}")

#Метод трапеций
total_integral_trap = 0.0
y_i = math.sin(100 * a) * math.exp(-a ** 2) * math.cos(2 * a)

for i in range(N):
    x_next = a + (i + 1) * dx #правый край
    y_next = math.sin(100 * x_next) * math.exp(-x_next ** 2) * math.cos(2 * x_next)
    total_integral_trap += (y_i + y_next) / 2.0 * dx
    y_i = y_next
print(f"Метод трапеций: {total_integral_trap}")

#Симпсон (плюс счиатем, что n должно быть четным)
if N % 2 != 0:
    print("\nДля метода Симпсона количество шагов N должно быть четным!")
else:
    # I = (dx/3) * (y0 + 4*y1 + 2*y2 + 4*y3 + ... + 2*y_{N-2} + 4*y_{N-1} + yN)
    integral_sum_simpson = 0.0

    for i in range(N + 1):
        x = a + i * dx
        y = math.sin(100 * x) * math.exp(-x ** 2) * math.cos(2 * x)
        if i == 0 or i == N:
            integral_sum_simpson += y
        elif i % 2 != 0:
            integral_sum_simpson += 4 * y
        else:
            integral_sum_simpson += 2 * y
    total_integral_simpson = integral_sum_simpson * (dx / 3.0)

    print(f"Метод Симпсона: {total_integral_simpson}")

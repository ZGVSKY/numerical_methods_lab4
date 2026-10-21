"""
Завдання 2, 3. Інтерполяційний многочлен Лаґранжа. (Степан)

Завдання 2: f(z1) = f(2) за чотирма вузлами (3-й степінь), eps = 0,01.
Завдання 3: додати (x4; y4) = (2,904; 8,011) і побудувати многочлен
за п'ятьма вузлами (4-й степінь).

Обчислювальна схема (таблиці 2.x зразка): різниці x_i - x_j та x_i - z,
добутки P_i, частки y_i / P_i; сума S, добуток D, L(z) = S * D.
"""

from src.common import Z1, EPS

def basis_products(xs, z):
    """Добутки P_i = prod_{j != i} (x_i - x_j) та добуток різниць (x_i - z)."""
    n = len(xs)
    P = []
    D = 1.0

    for i in range(n):
        D *= (z - xs[i])
        p_i = 1.0
        for j in range(n):
            if i != j:
                p_i *= (xs[i] - xs[j])
        P.append(p_i)

    return P, D

def lagrange(z, xs, ys):
    """Значення многочлена Лаґранжа у точці z (класична формула (5))."""
    P, D = basis_products(xs, z)
    S = 0.0

    print(f"{'i':<2} | {'x_i':<6} | {'P_i':<10} | {'y_i':<8} | {'y_i / P_i':<10}")
    print("-" * 45)

    for i in range(len(xs)):
        term = ys[i] / P[i]
        S += term
        print(f"{i:<2} | {xs[i]:<6.3f} | {P[i]:<10.3f} | {ys[i]:<8.3f} | {term:<10.3f}")

    print("-" * 45)
    print(f"Сума S = {S:.3f}")
    print(f"Добуток D = {D:.3f}")

    L_z = S * D
    return L_z

def run(xs=None, ys=None, z=Z1, eps=EPS):
    """
    Обчислити L_3(z) за 4 вузлами та L_4(z) за 5 вузлами.

    Повертає словник: {"L4": ..., "L5": ...} — значення за 4 і 5 вузлами.
    """
    if xs is None or ys is None or len(xs) < 5:
        raise ValueError("Потрібно 5 вузлів для повноцінного виконання.")

    # Завдання 2: 4 вузли
    print(f"Таблиця 2. Многочлен Лаґранжа (4 вузли) для z = {z}")
    L4_val = lagrange(z, xs[:4], ys[:4])
    print(f"L3({z}) = {L4_val:.3f}\n")

    # Завдання 3: 5 вузлів
    print(f"Таблиця 3. Многочлен Лаґранжа (5 вузлів) для z = {z}")
    L5_val = lagrange(z, xs, ys)
    print(f"L4({z}) = {L5_val:.3f}\n")

    return {"L4": L4_val, "L5": L5_val}
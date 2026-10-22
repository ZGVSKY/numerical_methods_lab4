"""
Завдання 4, 5. Многочлени Ньютона. (Даниїл)

Завдання 4: побудувати многочлени Ньютона за 4 вузлами (1-го, 2-го, 3-го
степенів), потім за 5 вузлами (до 4-го степеня).
Завдання 5: обчислити f(z2) = f(0,8) та f(z3) = f(3,1) за многочленом
Ньютона 4-го степеня з точністю eps = 0,01.

Вузли невіддалені, тож використовуємо розділені різниці (або скінченні —
якщо виявиться, що кроки рівні).
"""

import math
from src.common import Z2, Z3, EPS


def divided_differences(xs, ys):
    """Таблиця розділених різниць; повертає їх перший стовпець (коефіцієнти)."""
    n = len(xs)
    coef = list(ys)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (xs[i] - xs[i - j])
    return coef


def newton(z, xs, ys):
    """Значення многочлена Ньютона у точці z (стандартна форма через розділені різниці)."""
    coef = divided_differences(xs, ys)
    n = len(xs)
    result = coef[n - 1]
    for i in range(n - 2, -1, -1):
        result = result * (z - xs[i]) + coef[i]
    return result


def newton_t(z, xs, ys):
    """
    Значення многочлена Ньютона у формі зі змінною t = (z - x0)/h
    (як у зразку, завдання 5) — для рівновіддалених вузлів.
    """
    n = len(xs)
    h = xs[1] - xs[0]

    # таблиця скінченних значень
    diffs = [[0.0] * n for _ in range(n)]
    for i in range(n):
        diffs[i][0] = ys[i]

    for j in range(1, n):
        for i in range(n - j):
            diffs[i][j] = diffs[i+1][j-1] - diffs[i][j-1]

    # Якщо точка лежить у першій половині відрізка - використовуємо Перший многочлен (вперед)
    if z <= xs[n // 2]:
        t = (z - xs[0]) / h
        res = diffs[0][0]
        term = 1.0
        for i in range(1, n):
            term *= (t - (i - 1))
            res += (term / math.factorial(i)) * diffs[0][i]
        return res
    # Якщо точка у другій половині або екстраполяція справа - Другий многочлен (назад)
    else:
        t = (z - xs[-1]) / h
        res = diffs[n-1][0]
        term = 1.0
        for i in range(1, n):
            term *= (t + (i - 1))
            res += (term / math.factorial(i)) * diffs[n-1-i][i]
        return res


def run(xs=None, ys=None, points=(Z2, Z3), eps=EPS):
    """
    Побудувати многочлени Ньютона за 4 і 5 вузлами та обчислити
    значення у точках points за 5-вузловим многочленом.

    Повертає словник: {"N4": ..., "N5": ..., "values": {точка: значення}}.
    """
    print("\n" + "="*50)
    print("--- Етап 4, 5. Многочлени Ньютона (Даниїл) ---")
    print("="*50)

    # Берем перші 4 вузли
    xs4, ys4 = xs[:4], ys[:4]

    # Завдання 4:
    coef4 = divided_differences(xs4, ys4)
    coef5 = divided_differences(xs, ys)

    print("Коефіцієнти многочлена Ньютона (4 вузли):")
    print([round(c, 4) for c in coef4])
    print("\nКоефіцієнти многочлена Ньютона (5 вузлів):")
    print([round(c, 4) for c in coef5])

    # Перевіряємо, чи вузли рівновіддалені
    h = round(xs[1] - xs[0], 5)
    is_equidistant = all(round(xs[i+1] - xs[i], 5) == h for i in range(len(xs)-1))

    if is_equidistant:
        print(f"\nВузли рівновіддалені (крок h = {h}). Використовуємо формулу з t.")
        eval_func = newton_t
    else:
        print("\nВузли не є рівновіддаленими. Використовуємо стандартну форму.")
        eval_func = newton

    # Завдання 5:
    print("\nОбчислення f(z) за многочленом 4-го степеня (5 вузлів)")
    values = {}

    # Визначаєм до скількох знаків округлювати на основі eps
    decimals = abs(int(math.log10(eps))) if eps < 1 else 2

    for z in points:
        val_exact = eval_func(z, xs, ys)
        val_rounded = round(val_exact, decimals)
        values[z] = val_rounded
        print(f"Точка z = {z}: точне = {val_exact:.4f}  =>  Округлене (eps={eps}) = {val_rounded}")

    print("="*50 + "\n")

    return {
        "N4": coef4,
        "N5": coef5,
        "values": values
    }
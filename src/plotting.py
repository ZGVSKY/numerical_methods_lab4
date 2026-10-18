"""
Завдання 7. Спільний графік. (Олександр)

Зобразити в одній системі координат:
  - вузли інтерполювання (4 початкові + додане спостереження);
  - графік многочлена Ньютона 4-го степеня (за 5 вузлами);
  - лінійний сплайн;
  - квадратичний сплайн дефекту 2;
  - квадратичний сплайн дефекту 1.

Результат зберігається у results/interpolation.png.

Домовленість: newton_func та кожна функція зі spline_funcs приймають
одне число z і повертають наближене значення f(z). Якщо реалізація ще
не готова (NotImplementedError), відповідна крива просто не малюється,
а решта графіка будується.
"""

import os

import numpy as np

import matplotlib
matplotlib.use("Agg")  # безінтерфейсний бекенд: графік одразу у файл
import matplotlib.pyplot as plt

from src.common import X, Y, X4, Y4, Z2, Z3, nodes5, fmt

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
OUTPUT_PATH = os.path.join(RESULTS_DIR, "interpolation.png")

GRID_POINTS = 400      # точок на кожну криву
EXTRAPOLATION_MARGIN = 0.15   # на скільки виходити за вузли для Ньютона

NEWTON_STYLE = {"color": "black", "linewidth": 2.2, "zorder": 3,
                "label": "Ньютон, ст. 4 (5 вузлів)"}
SPLINE_STYLES = [
    {"color": "tab:blue", "linewidth": 1.8, "linestyle": "--",
     "label": "Лінійний сплайн"},
    {"color": "tab:green", "linewidth": 1.8, "linestyle": "-.",
     "label": "Квадратичний сплайн, d = 2"},
    {"color": "tab:red", "linewidth": 1.8, "linestyle": ":",
     "label": "Квадратичний сплайн, d = 1"},
]


def _default_newton():
    """Многочлен Ньютона з модуля Даниїла (лінивий імпорт)."""
    from src.newton import newton_t
    return newton_t


def _default_splines():
    """Словник сплайнів з модуля Тараса (лінивий імпорт)."""
    from src import splines
    return {
        "Лінійний": splines.linear_spline,
        "Квадратичний d=2": splines.quad_defect2,
        "Квадратичний d=1": splines.quad_defect1,
    }


def _evaluate(func, grid):
    """
    Обчислити функцію на сітці. Повертає (values, ready):
    ready=False — функція ще не реалізована (NotImplementedError скрізь).
    Точки, де функція з якихось причин не обчислилась, пропускаються.
    """
    values = []
    failed = 0
    for z in grid:
        try:
            values.append(float(func(z)))
        except NotImplementedError:
            values.append(None)
            failed += 1
        except (ValueError, ZeroDivisionError, FloatingPointError):
            # поза доменом визначення сплайна тощо — просто не ставимо точку
            values.append(None)
    if failed == len(grid):
        return None, False
    return values, True


def _draw_curve(ax, grid, values, style):
    """Намалювати криву, пропустивши необчислені точки."""
    xs, ys = [], []
    for z, v in zip(grid, values):
        if v is not None and np.isfinite(v):
            xs.append(z)
            ys.append(v)
    if xs:
        ax.plot(xs, ys, **style)


def run(xs=None, ys=None, newton_func=None, spline_funcs=None):
    """
    Побудувати та зберегти спільний графік.

    xs, ys — п'ять вузлів; newton_func — функція обчислення значення
    многочлена Ньютона; spline_funcs — словник {назва: функція сплайна}.

    Повертає шлях до зображення або None, якщо побудувати не вдалося.
    """
    if xs is None or ys is None:
        xs, ys = nodes5()
    if newton_func is None:
        newton_func = _default_newton()
    if spline_funcs is None:
        spline_funcs = _default_splines()

    x_left, x_right = xs[0], xs[-1]
    span = x_right - x_left
    margin = EXTRAPOLATION_MARGIN * span

    newton_grid = np.linspace(x_left - margin, x_right + margin, GRID_POINTS)
    spline_grid = np.linspace(x_left, x_right, GRID_POINTS)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    # Криві сплайнів (лише на [x0; x4], де вони визначені)
    for (name, func), style in zip(spline_funcs.items(), SPLINE_STYLES):
        values, ready = _evaluate(func, spline_grid)
        if ready:
            _draw_curve(ax, spline_grid, values, style)
        else:
            print(f"  графік: «{name}» ще не реалізовано — криву пропущено")

    # Многочлен Ньютона (з невеликим виходом за вузли — екстраполяція)
    values, ready = _evaluate(newton_func, newton_grid)
    if ready:
        _draw_curve(ax, newton_grid, values, NEWTON_STYLE)
    else:
        print("  графік: многочлен Ньютона ще не реалізовано — криву пропущено")

    # Вузли інтерполювання
    ax.scatter([X4], [Y4], s=70, marker="s", color="tab:orange", zorder=4,
               label="додане спостереження (x4; y4)")
    ax.scatter(xs[:4], ys[:4], s=55, color="crimson", zorder=4,
               label="вузли інтерполювання")
    ax.scatter(xs[:4], ys[:4], s=12, color="black", zorder=5)

    # Де шукаємо значення функції (завдання 5, 6)
    for z, name in ((Z2, f"z2 = {fmt(Z2, 1)}"), (Z3, f"z3 = {fmt(Z3, 1)}")):
        ax.axvline(z, color="gray", linewidth=0.8, linestyle=(0, (3, 5)),
                   zorder=1)
        ax.annotate(name, xy=(z, ax.get_ylim()[0]), xytext=(4, 6),
                    textcoords="offset points", fontsize=9, color="gray")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Поліноміальна та сплайн-інтерполяція (варіант 7)")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="best", fontsize=9)

    try:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        fig.tight_layout()
        fig.savefig(OUTPUT_PATH)
    except OSError as e:
        print(f"  графік: не вдалося зберегти файл — {e}")
        plt.close(fig)
        return None
    finally:
        plt.close(fig)

    print(f"  графік: збережено {OUTPUT_PATH}")
    return OUTPUT_PATH

"""
Завдання 7. Спільний графік. (Олександр)

Зобразити в одній системі координат:
  - вузли інтерполювання (4 початкові + додане спостереження);
  - графік многочлена Ньютона 4-го степеня (за 5 вузлами);
  - лінійний сплайн;
  - квадратичний сплайн дефекту 2;
  - квадратичний сплайн дефекту 1.

Зберегти результат у results/interpolation.png.
"""

import os

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
OUTPUT_PATH = os.path.join(RESULTS_DIR, "interpolation.png")


def run(xs=None, ys=None, newton_func=None, spline_funcs=None):
    """
    Побудувати та зберегти спільний графік.

    newton_func та spline_funcs — функції з src/newton.py та src/splines.py
    для обчислення значень у довільних точках (щоб графік будувався саме
    за реалізованими методами).

    Повертає шлях до збереженого зображення.
    """
    raise NotImplementedError("TODO (Олександр): завдання 7")

"""
Лабораторна робота №4 — Поліноміальна та сплайн-інтерполяція.
Чисельні методи, варіант 7. Мова реалізації: Python 3.

    x:      0,324   0,969   1,614   2,259      x4 = 2,904
    y:     -2,052  -1,597  -0,231   2,808      y4 = 8,011

    Точки: f(2) = ?      (завдання 1, 2 — схема Ейткіна, Лаґранж)
           f(0,8) = ?    (завдання 5, 6 — Ньютон, сплайни)
           f(3,1) = ?    (завдання 5, 6 — Ньютон, сплайни)
           eps = 0,01

Порядок виконання (кожен пункт — окремо і самостійно):
  1. схема Ейткіна (4 вузли)                  -> f(2)        [Степан]
  2. многочлен Лаґранжа (4 вузли)             -> f(2)        [Степан]
  3. додати (x4; y4), Лаґранж (5 вузлів)                      [Степан]
  4. многочлени Ньютона (4 і 5 вузлів)                       [Даниїл]
  5. Ньютон (5 вузлів)                        -> f(0,8), f(3,1) [Даниїл]
  6. сплайни: лінійний, квадратичні (d=2, d=1) -> f(0,8), f(3,1) [Тарас]
  7. спільний графік Ньютона та сплайнів                   [Олександр]

Запуск: python main.py

Частини, які реалізують учасники (виклик у потрібному порядку):
  1. src/aitkin.py     -> завдання 1 (схема Ейткіна)
  2. src/lagrange.py   -> завдання 2, 3 (многочлен Лаґранжа)
  3. src/newton.py     -> завдання 4, 5 (многочлени Ньютона)
  4. src/splines.py    -> завдання 6 (сплайни)
  5. src/plotting.py   -> завдання 7 (графік)
  6. перевірка: порівняння f(2) зі схеми Ейткіна і за Лаґранжем,
     порівняння значень у точках 0,8 і 3,1 (Ньютон проти сплайнів)
"""

import sys

from src import aitkin, lagrange, newton, splines, plotting
from src.common import X, Y, X4, Y4, Z1, Z2, Z3, EPS, fmt

# Примусово друкувати кирилицю коректно на будь-якій кодовці Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

LINE = "=" * 86


def z_label(z):
    """Підпис точки: 2 -> «2», 0.8 -> «0,8», 3.1 -> «3,1»."""
    return f"{z:g}".replace(".", ",")


def run_stage(stage, title, author, func, *args, **kwargs):
    """
    Викликати частину реалізовану учасником, надрукувавши заголовок етапу.
    Повертає результат функції або None, якщо частину ще не реалізовано.
    """
    print(f"\n{LINE}\nЕтап {stage}. {title.upper()}  ({author})\n{LINE}")
    try:
        return func(*args, **kwargs)
    except NotImplementedError as e:
        print(f"  [ ще не реалізовано ] {e}")
        return None


# ---------------------------------------------------------------- #
#  Перевірка та порівняння результатів (Олександр)
# ---------------------------------------------------------------- #

def _extract(container, z):
    """
    Дістати значення у точці z з різних форм результатів учасників:
    {"value": ...}, {"values": {z: ...}}, {z: ...} — усі варіанти підтримуються.
    """
    if container is None:
        return None
    if isinstance(container, (int, float)) and not isinstance(container, bool):
        return float(container)
    if isinstance(container, dict):
        for key in (z, str(z), f"{z:g}", fmt(z, 1), fmt(z)):
            if key in container:
                value = container[key]
                if isinstance(value, (int, float)):
                    return float(value)
        for key in ("value", "values", "result"):
            if key in container and container[key] is not container:
                found = _extract(container[key], z)
                if found is not None:
                    return found
    return None


def compare_and_report(aitkin_res, lagrange_res, newton_res, splines_res):
    """
    Порівняти результати етапів і підсумувати відповіді (Олександр).

    Контроль: f(2) за схемою Ейткіна і за многочленом Лаґранжа 3-го степеня
    мають збігатися в межах eps (обчислюють той самий многочлен).
    Значення Ньютона і сплайнів у точках 0,8 та 3,1 друкуються для
    порівняння (самі методи різні, тому розбіжність допустима).
    """
    print(f"\n{LINE}\nПОРІВНЯННЯ РЕЗУЛЬТАТІВ\n{LINE}")

    answers = {}

    # --- f(2): Ейткін vs Лаґранж (4 вузли) ---
    v_aitkin = _extract(aitkin_res, Z1)
    v_lagrange = _extract(lagrange_res, Z1)
    if v_lagrange is None and isinstance(lagrange_res, dict):
        v_lagrange = lagrange_res.get("L4")
    if v_aitkin is not None and v_lagrange is not None:
        diff = abs(v_aitkin - v_lagrange)
        verdict = ("збігаються в межах eps" if diff <= EPS + 1e-12
                   else "РОЗБІЖНІСТЬ БІЛЬША ЗА EPS — перевірити обчислення")
        print(f"  f({z_label(Z1)}):  Ейткін = {fmt(v_aitkin)}   "
              f"Лаґранж (4 вузли) = {fmt(v_lagrange)}   "
              f"|різниця| = {fmt(diff)}  ->  {verdict}")
        answers[Z1] = (v_aitkin + v_lagrange) / 2
    else:
        print(f"  f({z_label(Z1)}):  порівняння недоступне "
              f"(етапи 1-2 ще не реалізовано)")

    # --- f(0,8) та f(3,1): Ньютон vs сплайни ---
    spline_names = {"linear": "Лінійний сплайн",
                    "defect2": "Квадратичний, d = 2",
                    "defect1": "Квадратичний, d = 1"}
    for z in (Z2, Z3):
        newton_val = _extract(newton_res, z)
        if newton_val is not None:
            answers[z] = newton_val
        print(f"\n  f({z_label(z)}):")
        if newton_val is not None:
            print(f"    Ньютон (5 вузлів)        = {fmt(newton_val)}")
        else:
            print("    Ньютон (5 вузлів)        = ще не реалізовано")
        if not isinstance(splines_res, dict):
            print("    сплайни                  = ще не реалізовано")
            continue
        for key, name in spline_names.items():
            value = _extract(splines_res.get(key), z)
            if value is not None:
                note = ""
                if newton_val is not None:
                    note = f"   (від Ньютона: {fmt(abs(value - newton_val))})"
                print(f"    {name:<24}= {fmt(value)}{note}")
            else:
                print(f"    {name:<24}= ще не реалізовано")

    # --- Підсумкова відповідь ---
    print(f"\n{LINE}\nВІДПОВІДІ (найкращі наявні наближення)\n{LINE}")
    for z in (Z1, Z2, Z3):
        value = answers.get(z)
        label = f"f({z_label(z)})"
        if value is not None:
            print(f"  {label:<10}≈ {fmt(value)}   (з точністю до {fmt(EPS, 2)})")
        else:
            print(f"  {label:<10}— етапи ще не реалізовано")

    return answers


def main():
    xs, ys = X, Y                  # 4 початкові вузли
    xs5, ys5 = X + [X4], Y + [Y4]  # 5 вузлів (після додавання спостереження)

    # 1. Схема Ейткіна -> f(2) (Степан)
    aitkin_res = run_stage(1, "Схема Ейткіна", "Степан",
                           aitkin.run, xs, ys, Z1, EPS)

    # 2-3. Многочлен Лаґранжа: 4 і 5 вузлів (Степан)
    lagrange_res = run_stage("2-3", "Многочлен Лаґранжа", "Степан",
                             lagrange.run, xs5, ys5, Z1, EPS)

    # 4-5. Многочлени Ньютона та значення f(0,8), f(3,1) (Даниїл)
    newton_res = run_stage("4-5", "Многочлени Ньютона", "Даниїл",
                           newton.run, xs5, ys5, (Z2, Z3), EPS)

    # 6. Сплайни: значення f(0,8), f(3,1) (Тарас)
    splines_res = run_stage(6, "Інтерполяційні сплайни", "Тарас",
                            splines.run, xs5, ys5, (Z2, Z3), EPS)

    # 7. Спільний графік (Олександр)
    # plotting чекає функції вигляду f(z), тож прив'язуємо вузли
    newton_func = lambda z: newton.newton_t(z, xs5, ys5)
    spline_funcs = {
        "Лінійний": lambda z: splines.linear_spline(z, xs5, ys5),
        "Квадратичний d=2": lambda z: splines.quad_defect2(z, xs5, ys5),
        "Квадратичний d=1": lambda z: splines.quad_defect1(z, xs5, ys5),
    }
    run_stage(7, "Спільний графік", "Олександр",
              plotting.run, xs5, ys5, newton_func, spline_funcs)

    # Перевірка та порівняння результатів (Олександр)
    compare_and_report(aitkin_res, lagrange_res, newton_res, splines_res)

    print("\nГотово.")


if __name__ == "__main__":
    main()

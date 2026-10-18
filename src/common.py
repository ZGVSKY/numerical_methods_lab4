"""
Вхідні дані та спільні утиліти. Лабораторна робота №4, варіант 7.

Відповідальний: Олександр (тімлід)

    x:      0,324   0,969   1,614   2,259      x4 = 2,904
    y:     -2,052  -1,597  -0,231   2,808      y4 = 8,011

    Точки:   z1 = 2      (завдання 1, 2)
             z2 = 0,8    (завдання 5, 6)
             z3 = 3,1    (завдання 5, 6)
             eps = 0,01
"""

# --- Вузли інтерполювання (4 початкові спостереження) ---
X = [0.324, 0.969, 1.614, 2.259]
Y = [-2.052, -1.597, -0.231, 2.808]

# --- П'яте спостереження (додається у завданні 3) ---
X4 = 2.904
Y4 = 8.011

# --- Точки, у яких шукаємо значення функції ---
Z1 = 2.0    # завдання 1, 2
Z2 = 0.8    # завдання 5, 6
Z3 = 3.1    # завдання 5, 6

# --- Точність ---
EPS = 0.01

# Скільки знаків після коми тримаємо у проміжних обчисленнях
# («запасний» знак до точності eps = 0,01 — за методичкою)
DIGITS = 3


def nodes4():
    """Повертає (xs, ys) для чотирьох початкових вузлів."""
    return list(X), list(Y)


def nodes5():
    """Повертає (xs, ys) для п'яти вузлів (з доданим спостереженням)."""
    return list(X) + [X4], list(Y) + [Y4]


def fmt(value, digits=DIGITS):
    """
    Форматування числа для друку: округлення та кома замість десяткової крапки
    (як у методичці). None друкується як «—», -0.000 як 0,000.
    """
    if value is None:
        return "—"
    v = round(float(value), digits)
    if v == 0:
        v = 0.0
    return f"{v:.{digits}f}".replace(".", ",")


def _cell(value):
    """Підготувати клітинку таблиці до друку."""
    if value is None:
        return "—"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        return fmt(value)
    return str(value)


def _is_numeric(column):
    """Чи складається стовпець лише з чисел (для вирівнювання праворуч)."""
    for cell in column:
        if cell == "—":
            continue
        try:
            float(cell.replace(",", "."))
        except ValueError:
            return False
    return True


def print_table(headers, rows, title=None):
    """
    Друк таблиці у консолі з вирівнюванням за шириною колонок.

    headers — назви стовпців; rows — рядки даних (числа автоматично
    форматуються через fmt()); title — необов'язковий підпис над таблицею.

    Числові стовпці вирівнюються праворуч, текстові — ліворуч.
    """
    if title:
        print(f"\n{title}")

    cells = [[_cell(c) for c in row] for row in rows]
    heads = [str(h) for h in headers]

    widths = [len(h) for h in heads]
    for row in cells:
        for i, c in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(c))

    numeric = [_is_numeric([row[i] for row in cells if i < len(row)])
               for i in range(len(heads))]

    def line(values):
        out = []
        for i, v in enumerate(values):
            out.append(v.rjust(widths[i]) if numeric[i] else v.ljust(widths[i]))
        return " | ".join(out)

    print(line(heads))
    print("-+-".join("-" * w for w in widths))
    for row in cells:
        print(line(row))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

def get_rule_ternary(rule_number):
    """Преобразует номер правила в троичное представление длиной 27 бит"""
    # Для 3 состояний и 3 соседей нужно 3^3 = 27 правил
    return format(rule_number, '027b')  # 27 бит для троичной системы

def evolve_ternary_automaton(rule_number, steps, size):
    # Создаем сетку
    grid = np.zeros((steps, size), dtype=int)

    # Инициализируем среднюю клетку в первом ряду как состояние 1
    grid[0, size // 2] = 1

    # Получаем бинарное представление правила (27 бит)
    rule_bin = get_rule_ternary(rule_number)
    rules = {}

    # Создаем таблицу правил для всех комбинаций 3х клеток
    for i, bit in enumerate(rule_bin[::-1]):
        # Преобразуем индекс в троичный паттерн длиной 3 символа
        pattern = ""
        temp = i
        for j in range(3):
            pattern = str(temp % 3) + pattern
            temp //= 3
        rules[pattern] = int(bit)

    # Применяем правила для каждого шага
    for row in range(1, steps):
        for col in range(size):
            # Определяем соседей с циклическими границами
            left = grid[row-1, (col-1) % size]
            center = grid[row-1, col]
            right = grid[row-1, (col+1) % size]

            # Формируем паттерн
            pattern = f"{left}{center}{right}"
            # Применяем правило
            grid[row, col] = rules[pattern]

    return grid

def main():
    # Запрос правила
    rule = int(input("Введите правило (0-134217727): "))  # 3^27 = 134217727

    # Показываем правило в двоичном виде
    ternary_rule = get_rule_ternary(rule)
    print(f"Правило {rule} в двоичном виде: {ternary_rule}")

    # Параметры симуляции
    steps = 100  # Количество эпох
    size = 201  # Ширина сетки

    # Запуск симуляции
    result = evolve_ternary_automaton(rule, steps, size)

    # Создаем цветовую карту для трех состояний
    colors = ['black', 'red', 'yellow']  # 0=черный, 1=красный, 2=желтый
    cmap = ListedColormap(colors)

    # Визуализация
    plt.figure(figsize=(10, 6))
    plt.imshow(result, cmap=cmap, interpolation='nearest')
    plt.axis('off')
    plt.title(f"Троичный клеточный автомат - Правило {rule}")
    plt.show()

if __name__ == "__main__":
    main()



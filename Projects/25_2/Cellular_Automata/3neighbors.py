import matplotlib.pyplot as plt
import numpy as np

def get_rule_binary(rule_number):
    """Преобразует номер правила в бинарное представление длиной 8 бит"""
    return format(rule_number, '08b')

def evolve_cellular_automaton(rule_number, steps, size):
    # Создаем сетку
    grid = np.zeros((steps, size), dtype=int)

    # Инициализируем среднюю клетку в первом ряду как живую
    grid[0, size // 2] = 1

    # Получаем бинарное представление правила
    rule_bin = get_rule_binary(rule_number)
    rules = {}

    # Создаем таблицу правил для всех комбинаций 3х клеток
    for i, bit in enumerate(rule_bin[::-1]):
        pattern = format(i, '03b')
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
    rule = int(input("Введите правило (0-255): "))

    # Показываем правило в двоичном виде
    binary_rule = get_rule_binary(rule)
    print(f"Правило {rule} в двоичном виде: {binary_rule}")

    # Параметры симуляции
    steps = 100
      # Количество эпох
    size = 200  # Ширина сетки

    # Запуск симуляции
    result = evolve_cellular_automaton(rule, steps, size)

    # Визуализация без лишних надписей
    plt.figure(figsize=(10, 6))
    plt.imshow(result, cmap='binary', interpolation='nearest')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()


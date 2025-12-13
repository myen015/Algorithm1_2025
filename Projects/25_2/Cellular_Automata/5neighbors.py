import matplotlib.pyplot as plt
import numpy as np

def get_rule_binary(rule_number):
    return format(rule_number, '032b')

def evolve_cellular_automaton(rule_number, steps, size):
    grid = np.zeros((steps, size), dtype=int)
    grid[0, size // 2] = 1

    rule_bin = get_rule_binary(rule_number)
    rules = {}

    for i, bit in enumerate(rule_bin[::-1]):
        pattern = format(i, '05b')
        rules[pattern] = int(bit)

    for row in range(1, steps):
        for col in range(size):
            left = grid[row-1, (col-1) % size]
            double_left = grid[row-1, (col-2) % size]
            center = grid[row-1, col]
            right = grid[row-1, (col+1) % size]
            double_right = grid[row-1, (col+2) % size]
            pattern = f"{double_left}{left}{center}{right}{double_right}"
            grid[row, col] = rules[pattern]

    return grid

def main():
    rule = int(input("Введите правило (0 - 4 294 967 296): "))

    binary_rule = get_rule_binary(rule)
    print(f"Правило {rule} в двоичном виде: {binary_rule}")


    steps = 100
    size = 200

    result = evolve_cellular_automaton(rule, steps, size)

    plt.figure(figsize=(10, 6))
    plt.imshow(result, cmap='binary', interpolation='nearest')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()




 # 123456789 2^30 2^31 2^32 = 0
 # 865247931 85694734 2478962341 47895412365485 5248965317 24675915382 84629731 красиво
 # 2598436 95136842 3549494 7613496248 интересно

import random
import matplotlib.pyplot as plt
import numpy as np
from bst_tree import BST

def get_tree_height(node):
    if node is None:
        return 0
    return 1 + max(get_tree_height(node.left), get_tree_height(node.right))

def create_bst_from_keys(keys):
    tree = BST()
    for key in keys:
        tree.insert(key)
    return tree


def generate_unique_random_keys(n, min_val=1, max_val=1000000):
    return random.sample(range(min_val, max_val), n)


def experiment_height_vs_keys(max_n=3000, step=25, trials=10):
    n_values = []
    avg_heights = []
    min_heights = []
    max_heights = []

    for n in range(step, max_n + 1, step):
        heights = []
        for _ in range(trials):
            keys = generate_unique_random_keys(n)
            tree = create_bst_from_keys(keys)
            height = get_tree_height(tree.root)
            heights.append(height)

        # сохр рез
        n_values.append(n)
        avg_heights.append(np.mean(heights))
        min_heights.append(min(heights))
        max_heights.append(max(heights))

        if n % 500 == 0 or n == step or n == max_n:
            print(f"n={n:4} | Средняя высота: {np.mean(heights):6.2f} | Мин: {min(heights):3} | Макс: {max(heights):3}")

    return n_values, avg_heights, min_heights, max_heights


def plot_results(n_values, avg_heights, min_heights, max_heights):
    n_array = np.array(n_values)
    avg_array = np.array(avg_heights)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  #  фигура с двумя графиками

    # график 1 высота vs Количество ключей
    ax1.plot(n_values, avg_heights, 'b-', linewidth=2, label='Средняя высота', marker='o', markersize=3, markevery=5)
    ax1.fill_between(n_values, min_heights, max_heights,alpha=0.2, color='b', label='Диапазон (мин-макс)')
    ax1.set_xlabel('Количество ключей (n)')
    ax1.set_ylabel('Высота дерева (h)')
    ax1.set_title('Экспериментальная зависимость высоты BST от n')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)

    # График сравнение с теоретическими оценками
    ax2.plot(n_array, avg_array, 'b-', linewidth=2, label='Экспериментальная', marker='o', markersize=3, markevery=5)

    log2_n = np.log2(n_array)  # O(log n) - для сбалансированного дерева
    sqrt_n = np.sqrt(n_array)  # O(√n) - для случайного BST
    linear_n = n_array * 0.15  # O(n) - для вырожденного дерева

    ax2.plot(n_array, 2.8 * sqrt_n, 'r--', linewidth=2, label='Теория: 2.8√n (O(√n))')
    ax2.plot(n_array, 4.5 * log2_n, 'g--', linewidth=2, label='Теория: 4.5log₂n (O(log n))')
    ax2.plot(n_array, linear_n, 'm--', linewidth=1.5, label='Теория: 0.15n (O(n))', alpha=0.5)

    ax2.set_xlabel('Количество ключей (n)')
    ax2.set_ylabel('Высота (h)')
    ax2.set_title('Сравнение с теоретическими оценками')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)

    plt.tight_layout()
    plt.show()


def main():

    print("Экспериментальная зависимость высоты BST \nот количества ключей (случайные ключи)")

    MAX_N = 3000
    STEP = 25
    TRIALS = 10

    print(f"  Максимальное количество ключей (n): {MAX_N}")
    print(f"  Шаг n: {STEP}")
    print(f"  Количество испытаний для каждого n: {TRIALS}")

    # Расчет количества точек
    num_points = (MAX_N - STEP) // STEP + 1
    print(f"  Всего будет построено: {num_points} различных n")
    print(f"  Всего будет создано: {num_points * TRIALS} деревьев")

    print("\nНачало эксперимента")
    n_values, avg_heights, min_heights, max_heights = experiment_height_vs_keys(MAX_N, STEP, TRIALS)

    print("Конец Эксперимента\nПостроение графиков")
    plot_results(n_values, avg_heights, min_heights, max_heights)

if __name__ == "__main__":
    main()
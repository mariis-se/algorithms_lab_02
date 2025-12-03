import random
import matplotlib.pyplot as plt
import numpy as np
from avl_tree import AVLTree
from rb_tree import RBTree

def get_avl_height(node):
    if node is None:
        return 0
    return 1 + max(get_avl_height(node.left), get_avl_height(node.right))


def get_rb_height(node):
    if node is None or node.val is None:  # Проверка на NIL узел
        return 0
    return 1 + max(get_rb_height(node.left), get_rb_height(node.right))

def generate_unique_random_keys(n, min_val=1, max_val=1000000):
    return random.sample(range(min_val, max_val), n)

def experiment_trees_height(max_n=3000, step=25, trials=5):
    n_values = []
    avl_heights = []
    rb_heights = []
    avl_min = []
    avl_max = []
    rb_min = []
    rb_max = []

    for n in range(step, max_n + 1, step):
        avl_heights_batch = []
        rb_heights_batch = []

        for _ in range(trials):
            keys = generate_unique_random_keys(n)

            # AVL дерево
            avl = AVLTree()
            for key in keys:
                avl.insert(key)
            avl_height = get_avl_height(avl.root)
            avl_heights_batch.append(avl_height)

            # Красно-черное дерево
            rb = RBTree()
            for key in keys:
                rb.insert(key)
            rb_height = get_rb_height(rb.root)
            rb_heights_batch.append(rb_height)

        # сохраняем результаты
        n_values.append(n)
        avl_heights.append(np.mean(avl_heights_batch))
        rb_heights.append(np.mean(rb_heights_batch))
        avl_min.append(min(avl_heights_batch))
        avl_max.append(max(avl_heights_batch))
        rb_min.append(min(rb_heights_batch))
        rb_max.append(max(rb_heights_batch))
        if n % 500 == 0 or n == step or n == max_n:
            print(f"n={n:4} | AVL: {np.mean(avl_heights_batch):5.1f} | RB: {np.mean(rb_heights_batch):5.1f} | "
                  f"Разница: {np.mean(avl_heights_batch) - np.mean(rb_heights_batch):5.1f}")

    return n_values, avl_heights, rb_heights, avl_min, avl_max, rb_min, rb_max

def plot_results(n_values, avl_heights, rb_heights, avl_min, avl_max, rb_min, rb_max):
    n_array = np.array(n_values)
    avl_array = np.array(avl_heights)
    rb_array = np.array(rb_heights)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Сравнение высот AVL и красно-черного дерева\n(случайные равномерно распределенные ключи, n до 3000)')

    # гр 1 Сравнение высот AVL и RB
    ax1.plot(n_values, avl_heights, 'b-', linewidth=2, label='AVL дерево', marker='o', markersize=3, markevery=10)
    ax1.plot(n_values, rb_heights, 'r-', linewidth=2, label='Красно-черное дерево', marker='s', markersize=3, markevery=10)
    ax1.fill_between(n_values, avl_min, avl_max, alpha=0.1, color='b')
    ax1.fill_between(n_values, rb_min, rb_max, alpha=0.1, color='r')
    ax1.set_xlabel('Количество ключей (n)')
    ax1.set_ylabel('Высота дерева')
    ax1.set_title('Сравнение высот AVL и RB деревьев')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)

    # гр 2 Теоретические оценки
    ax2.plot(n_array, avl_array, 'b-', linewidth=2, label='AVL (эксперимент)', marker='o', markersize=3, markevery=10)
    ax2.plot(n_array, rb_array, 'r-', linewidth=2, label='RB (эксперимент)', marker='s', markersize=3, markevery=10)

    # теория
    log2_n = np.log2(n_array)  # Нижняя оценка для сбалансированных деревьев
    log_phi_n = 1.44 * log2_n  # Верхняя оценка для AVL (log_φ(2) ≈ 1.44)
    two_log2_n = 2.0 * log2_n  # Верхняя оценка для RB

    ax2.plot(n_array, log2_n, 'g--', linewidth=1.5, label='Нижняя оценка: log₂(n)')
    ax2.plot(n_array, log_phi_n, 'm--', linewidth=1.5, label='Верхняя оценка AVL: 1.44log₂(n)')
    ax2.plot(n_array, two_log2_n, 'c--', linewidth=1.5, label='Верхняя оценка RB: 2log₂(n)')

    ax2.set_xlabel('Количество ключей (n)')
    ax2.set_ylabel('Высота (h)')
    ax2.set_title('Сравнение с теоретическими оценками')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

def main():
    print("Сравнение высот AVL и красно-черного дерева (случайные равномерно распределенные ключи)")
    MAX_N = 3000
    STEP = 25
    TRIALS = 5

    print(f"\nПараметры эксперимента:")
    print(f"  Максимальное количество ключей (n): {MAX_N}")
    print(f"  Шаг изменения n: {STEP}")
    print(f"  Количество испытаний для каждого n: {TRIALS}")

    num_points = (MAX_N - STEP) // STEP + 1
    print(f"  Всего будет построено: {num_points} различных n")
    print(f"  Всего будет создано: {num_points * TRIALS * 2} деревьев (AVL + RB)")

    print("\nНачало эксперимента")
    results = experiment_trees_height(MAX_N, STEP, TRIALS)

    print("\nПостроение графиков")
    plot_results(*results)

if __name__ == "__main__":
    main()
import matplotlib.pyplot as plt
import numpy as np
from avl_tree import AVLTree
from rb_tree import RBTree

def get_avl_height(node):
    if node is None:
        return 0
    return 1 + max(get_avl_height(node.left), get_avl_height(node.right))

def get_rb_height(node):
    if node is None or node.val is None:
        return 0
    return 1 + max(get_rb_height(node.left), get_rb_height(node.right))

def generate_monotonic_keys(n, start=1):
    #генерация n монотонно возрастающих ключей
    return list(range(start, start + n))

def experiment_trees_height_monotonic(max_n=3000, step=10, trials=1):
    n_values = []
    avl_heights = []
    rb_heights = []

    for n in range(step, max_n + 1, step):
        # генерируем мон возраст ключи
        keys = generate_monotonic_keys(n)

        # AVL дерево
        avl = AVLTree()
        for key in keys:
            avl.insert(key)
        avl_height = get_avl_height(avl.root)

        # Красно-черное дерево
        rb = RBTree()
        for key in keys:
            rb.insert(key)
        rb_height = get_rb_height(rb.root)

        n_values.append(n)
        avl_heights.append(avl_height)
        rb_heights.append(rb_height)

        if n % 500 == 0 or n == step or n == max_n:
            print(f"n={n:4} | AVL: {avl_height:3} | RB: {rb_height:3} | Разница: {avl_height - rb_height:3}")

    return n_values, avl_heights, rb_heights


def plot_results(n_values, avl_heights, rb_heights):
    n_array = np.array(n_values)
    avl_array = np.array(avl_heights)
    rb_array = np.array(rb_heights)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Высоты деревьев при монотонно возрастающих ключах')

    # гр 1 Высоты AVL и RB
    ax1 = axes[0]
    ax1.plot(n_values, avl_heights, 'b-', linewidth=2, label='AVL дерево', marker='o', markersize=2, markevery=20)
    ax1.plot(n_values, rb_heights, 'r-', linewidth=2, label='Красно-черное дерево', marker='s', markersize=2,markevery=20)
    ax1.set_xlabel('Количество ключей (n)')
    ax1.set_ylabel('Высота дерева')
    ax1.set_title('Фактическая высота деревьев')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=11)

    # гр 2 Увеличенное сравнение с теоретическими оценками
    ax2 = axes[1]

    log2_n = np.log2(n_array)  # Идеальная сбалансированность
    upper_bound_avl = 1.44 * np.log2(n_array + 2)  # Верхняя граница AVL
    upper_bound_rb = 2.0 * np.log2(n_array + 1)  # Верхняя граница RB

    mask = (avl_array <= 25) & (rb_array <= 25)

    ax2.plot(n_array[mask], avl_array[mask], 'b-', linewidth=2, label='AVL (эксперимент)', marker='o', markersize=4, markevery=5)
    ax2.plot(n_array[mask], rb_array[mask], 'r-', linewidth=2, label='RB (эксперимент)', marker='s', markersize=4, markevery=5)

    # теор кривые
    ax2.plot(n_array, log2_n, 'g--', linewidth=1.5, label='Идеал: log₂(n)', alpha=0.7)
    ax2.plot(n_array, upper_bound_avl, 'm--', linewidth=1.5, label='Верхняя граница AVL: 1.44·log₂(n+2)', alpha=0.7)
    ax2.plot(n_array, upper_bound_rb, 'c--', linewidth=1.5, label='Верхняя граница RB: 2.0·log₂(n+1)', alpha=0.7)
    # линия вырожденного дерева
    degenerate_n = n_array[n_array <= 100]
    ax2.plot(degenerate_n, degenerate_n, 'k:', linewidth=1, label='Вырожденное BST (n)', alpha=0.3)

    ax2.set_xlabel('Количество ключей (n)')
    ax2.set_ylabel('Высота (h)')
    ax2.set_title('Увеличенное сравнение с теоретическими оценками\n(масштаб: высота до 25)')
    ax2.set_ylim(0, 25)  # Ограничиваем высоту
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=9)

    if np.max(avl_array) > 25 or np.max(rb_array) > 25:
        ax2.text(0.02, 0.98, f'Макс. высота AVL: {np.max(avl_array):.0f}\nМакс. высота RB: {np.max(rb_array):.0f}',
                 transform=ax2.transAxes, fontsize=9, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.show()

def main():
    print("ИССЛЕДОВАНИЕ: Высоты AVL и красно-черного дерева при монотонно возрастающих ключах")

    MAX_N = 3000
    STEP = 10
    TRIALS = 1
    print(f"\nПараметры эксперимента:")
    print(f"  Максимальное количество ключей (n): {MAX_N}")
    print(f"  Шаг изменения n: {STEP}")
    print(f"  Ключи: монотонно возрастающие (худший случай для BST)")

    num_points = (MAX_N - STEP) // STEP + 1
    print(f"\n  Всего будет построено: {num_points} деревьев каждого типа")
    #print(f"  Всего операций вставки: {num_points * MAX_N * 2:,} (AVL + RB)")

    print("\nНачало эксперимента")
    results = experiment_trees_height_monotonic(MAX_N, STEP, TRIALS)

    print("\nПостроение графиков")
    plot_results(*results)

if __name__ == "__main__":
    main()
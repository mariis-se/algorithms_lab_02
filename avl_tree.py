from bst_tree import BSTNode, BST

class AVLNode(BSTNode):
    def __init__(self, val):
        super().__init__(val)  # вызываем конструктор родителя
        self.height = 1

class AVLTree(BST):
    def __init__(self):
        super().__init__()  # инициализируем базовый класс
        self.step_counter = 0  # счетчик  для пошагового вывода

    def _get_height(self, node):
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node):
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node):
        if node is not None:
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    # повороты
    def _right_rotate(self, y):      #LL
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self._update_height(y)
        self._update_height(x)

        return x  # новый корень поддерева

    def _left_rotate(self, x):   #RR
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self._update_height(x)
        self._update_height(y)

        return y

    # обнов методы

    def insert(self, val):
        self.root = self._insert_avl(self.root, val)

    def _insert_avl(self, node, val):
        if node is None:
            return AVLNode(val)

        if val < node.val:
            node.left = self._insert_avl(node.left, val)
        elif val > node.val:
            node.right = self._insert_avl(node.right, val)
        else:
            return node  # дубликаты не вставляем

        self._update_height(node)

        balance = self._get_balance(node)

        # балансировка
        # LL
        if balance > 1 and val < node.left.val:
            return self._right_rotate(node)

        # RR
        if balance < -1 and val > node.right.val:
            return self._left_rotate(node)

        # LR
        if balance > 1 and val > node.left.val:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # RL
        if balance < -1 and val < node.right.val:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def delete(self, val):
        self.root = self._delete_avl(self.root, val)

    def _delete_avl(self, node, val):
        if node is None:
            return node

        if val < node.val:
            node.left = self._delete_avl(node.left, val)
        elif val > node.val:
            node.right = self._delete_avl(node.right, val)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # узел с двумя потомками
            temp = self._find_min_node(node.right)
            node.val = temp.val
            node.right = self._delete_avl(node.right, temp.val)

        # дерево пустое после удаления
        if node is None:
            return node

        self._update_height(node)

        balance = self._get_balance(node)
        #balance
        # ll
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)

        # LR
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # RR
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)

        # RL
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def insert_with_steps(self, val):
        self.step_counter += 1

        print(f"Шг {self.step_counter}: Вставляем значение {val}")
        # print("дерево ДО:")
        # if self.root is None:
        #     print("Дерево пустое")
        # else:
        #     self.print_vertical()

        self.insert(val)

        #print(f"\nДерево ПОСЛЕ вставки {val}:")
        self.print_vertical()

    def insert_sequence_with_steps(self, values):
        print("\nВставка с балансировкой\n")

        self.step_counter = 0
        for val in values:
            self.insert_with_steps(val)

    def print_vertical(self):
        if self.root is None:
            print("Дерево пустое")
            return

        lines = []
        self._generate_tree_lines(self.root, 0, "root", lines)
        for line in lines:
            print(line)

    def _generate_tree_lines(self, node, level, direction, lines):
        if node is not None:
            balance = self._get_balance(node)
            indent = "    " * level
            lines.append(f"{indent}{direction}: {node.val} [h={node.height}, b={balance}]")

            if node.right is not None or node.left is not None:
                if node.right:
                    self._generate_tree_lines(node.right, level + 1, "right", lines)
                else:
                    lines.append(f"{'    ' * (level + 1)}right: None")

                if node.left:
                    self._generate_tree_lines(node.left, level + 1, "left", lines)
                else:
                    lines.append(f"{'    ' * (level + 1)}left: None")

    def print_tree(self):
        print("\n" + '_' * 50)
        print("Структура авл дерева (значение [баланс]):")
        print("\n" + '_' * 50)
        if self.root is None:
            print("Дерево пустое")
            return
        self._print_tree_recursive(self.root, "", True)

    def _print_tree_recursive(self, node, prefix, is_left):
        if node is not None:
            balance = self._get_balance(node)
            print(prefix + (" left: " if is_left else "rignt: ") + f"{node.val} [{balance}]")

            i = "    " if is_left else "|   "
            new_prefix = prefix + i

            if node.right is not None or node.left is not None:
                if node.right:
                    self._print_tree_recursive(node.right, new_prefix, False)
                else:
                    print(new_prefix + "rignt: None")

                if node.left:
                    self._print_tree_recursive(node.left, new_prefix, True)
                else:
                    print(new_prefix + " left: None")

    def is_balanced(self): #проверка баланса
        return self._is_balanced_recursive(self.root)

    def _is_balanced_recursive(self, node):
        #node = self.root
        if node is None:
            return True

        balance = self._get_balance(node)
        if abs(balance) > 1:
            return False

        return (self._is_balanced_recursive(node.left) and
                self._is_balanced_recursive(node.right))

def main():
    print(" AVL дерево")
    print("\n" + '_' * 50)
    avl1 = AVLTree()
    simple_seq = [10, 20, 30, 40, 50, 60, 70]

    print("1 последовательность ", simple_seq)
    print("\n" + '_' * 50)

    avl1.insert_sequence_with_steps(simple_seq)

    print(f"\nИтоговое дерево сбалансировано: {avl1.is_balanced()}")

    avl2 = AVLTree()
    left_seq = [30, 20, 10]
    print("" + '_' * 50)
    print("2 последовательность ", left_seq)

    avl2.insert_sequence_with_steps(left_seq)

    print(f"\nИтоговое дерево сбалансировано: {avl2.is_balanced()}")

    # RL
    avl3 = AVLTree()
    rl_seq = [10, 30, 20]
    print("" + '_' * 50)
    print("\n3 Право-левая несбалансированность, последовательность  ", rl_seq)

    avl3.insert_sequence_with_steps(rl_seq)

    print(f"\nИтоговое дерево сбалансировано: {avl3.is_balanced()}")

    avl4 = AVLTree()
    worst_seq = [1, 2, 3, 4, 5, 6]
    print("" + '_' * 50)
    print("\n4 последовательность  ", worst_seq)
    #print("\n" + '_' * 50)

    avl4.insert_sequence_with_steps(worst_seq)

    print("\nИтоговая структура:")
    avl4.print_vertical()
    print(f"\nДерево сбалансировано: {avl4.is_balanced()}")

    print("\n" + '_' * 50)
    print("6 Удаление с балансировкой")
    print("\n" + '_' * 50)

    avl6 = AVLTree()
    delete_seq = [50, 30, 70, 20, 40, 60, 80, 35, 45]

    print("\nСоздаем дерево из значений:", delete_seq)
    for val in delete_seq:
        avl6.insert(val)

    print("\nИсходное дерево:")
    avl6.print_vertical()

    deletions = [50, 20, 70]

    for val in deletions:
        print(f"\nУдаляем значение {val}:")
        avl6.delete(val)
        avl6.print_vertical()
        print(f"Дерево сбалансировано: {avl6.is_balanced()}")

if __name__ == "__main__":
    main()
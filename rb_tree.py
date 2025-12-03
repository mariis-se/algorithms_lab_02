from bst_tree import BSTNode, BST

class RBNode(BSTNode):
    RED = "RED"
    BLACK = "BLACK"

    def __init__(self, val):
        super().__init__(val)  # Вызываем конструктор родителя
        self.color = RBNode.RED
        self.parent = None

class RBTree(BST):
    def __init__(self):
        super().__init__()  # Инициализируем базовый класс
        self.NIL = RBNode(None)  # NIL узел
        self.NIL.color = RBNode.BLACK
        self.NIL.left = None
        self.NIL.right = None
        self.root = self.NIL

    def _create_node(self, val):
        node = RBNode(val)
        node.left = self.NIL
        node.right = self.NIL
        node.parent = None
        return node

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right = y
        y.parent = x

    def _fix_insert(self, node):#восстанавливаем св-ва кч дерева
        while node != self.root and node.parent.color == RBNode.RED:
            # Если родитель - левый потомок дедушки
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right

                #  Случай 1 дядя красный
                if uncle.color == RBNode.RED:
                    node.parent.color = RBNode.BLACK
                    uncle.color = RBNode.BLACK
                    node.parent.parent.color = RBNode.RED
                    node = node.parent.parent
                else:
                    # 2 узел - правый потомок
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)

                    #  3 узел - левый потомок
                    node.parent.color = RBNode.BLACK
                    node.parent.parent.color = RBNode.RED
                    self._right_rotate(node.parent.parent)
            else:
                # родитель - правый потомок дедушки
                uncle = node.parent.parent.left

                #  1 дядя красный
                if uncle.color == RBNode.RED:
                    node.parent.color = RBNode.BLACK
                    uncle.color = RBNode.BLACK
                    node.parent.parent.color = RBNode.RED
                    node = node.parent.parent
                else:
                    # 2 узел - левый потомок
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)

                    # 3 Узел - правый потомок
                    node.parent.color = RBNode.BLACK
                    node.parent.parent.color = RBNode.RED
                    self._left_rotate(node.parent.parent)
        self.root.color = RBNode.BLACK # корень всегда черный

    def _transplant(self, u, v):
        #Замена поддерева u на  v
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def _fix_delete(self, node):#восстанавливаем св-ва
        while node != self.root and node.color == RBNode.BLACK:
            if node == node.parent.left:
                sibling = node.parent.right

                #  1 брат красный
                if sibling.color == RBNode.RED:
                    sibling.color = RBNode.BLACK
                    node.parent.color = RBNode.RED
                    self._left_rotate(node.parent)
                    sibling = node.parent.right

                #  2 оба ребенка брата черные
                if sibling.left.color == RBNode.BLACK and sibling.right.color == RBNode.BLACK:
                    sibling.color = RBNode.RED
                    node = node.parent
                else:
                    #  3 правый ребенок брата черный
                    if sibling.right.color == RBNode.BLACK:
                        sibling.left.color = RBNode.BLACK
                        sibling.color = RBNode.RED
                        self._right_rotate(sibling)
                        sibling = node.parent.right

                    #  4 правый ребенок брата красный
                    sibling.color = node.parent.color
                    node.parent.color = RBNode.BLACK
                    sibling.right.color = RBNode.BLACK
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                # симметрично
                sibling = node.parent.left

                # случай 1: брат красный
                if sibling.color == RBNode.RED:
                    sibling.color = RBNode.BLACK
                    node.parent.color = RBNode.RED
                    self._right_rotate(node.parent)
                    sibling = node.parent.left

                # 2 оба ребенка брата черные
                if sibling.right.color == RBNode.BLACK and sibling.left.color == RBNode.BLACK:
                    sibling.color = RBNode.RED
                    node = node.parent
                else:
                    #  3 левый ребенок брата черный
                    if sibling.left.color == RBNode.BLACK:
                        sibling.right.color = RBNode.BLACK
                        sibling.color = RBNode.RED
                        self._left_rotate(sibling)
                        sibling = node.parent.left

                    #  4 левый ребенок брата красный
                    sibling.color = node.parent.color
                    node.parent.color = RBNode.BLACK
                    sibling.left.color = RBNode.BLACK
                    self._right_rotate(node.parent)
                    node = self.root
        node.color = RBNode.BLACK

    def insert(self, val):
        node = self._create_node(val)
        parent = None
        current = self.root
        while current != self.NIL:
            parent = current
            if node.val < current.val:
                current = current.left
            elif node.val > current.val:
                current = current.right
            else:
                return  # дубликаты не вставляем
        node.parent = parent

        if parent is None:
            self.root = node
        elif node.val < parent.val:
            parent.left = node
        else:
            parent.right = node
        # восстанавливаем свойства
        if node.parent is None:
            node.color = RBNode.BLACK
            return

        if node.parent.parent is None:
            return

        self._fix_insert(node)

    def delete(self, val):
        node = self.root
        while node != self.NIL:
            if val == node.val:
                break
            elif val < node.val:
                node = node.left
            else:
                node = node.right

        if node == self.NIL:
            return

        original_color = node.color
        x = None

        # Удаление узла
        if node.left == self.NIL:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self._transplant(node, node.left)
        else:
            # узел с двумя потомками
            successor = self._minimum(node.right)
            original_color = successor.color
            x = successor.right

            if successor.parent == node:
                x.parent = successor
            else:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor

            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
            successor.color = node.color

        # восст свва если нужно
        if original_color == RBNode.BLACK:
            self._fix_delete(x)

    def print_tree(self):
        print("Структура дерева:")
        if self.root == self.NIL:
            print("Дерево пустое")
            return
        self._print_tree_recursive(self.root, "", True)

    def _print_tree_recursive(self, node, prefix, is_left):
        if node != self.NIL:
            color_char = 'R' if node.color == RBNode.RED else 'B'
            print(prefix + (" left: " if is_left else "right: ") + f"{node.val}({color_char})")

            i = "    " if is_left else "|   "
            new_prefix = prefix + i

            if node.right != self.NIL or node.left != self.NIL:
                if node.right != self.NIL:
                    self._print_tree_recursive(node.right, new_prefix, False)
                else:
                    print(new_prefix + "left: NIL(B)")

                if node.left != self.NIL:
                    self._print_tree_recursive(node.left, new_prefix, True)
                else:
                    print(new_prefix + "right: NIL(B)")

    def check_rb_properties(self):
        properties = {
            "Корень черный": True,
            "Красный узел имеет черных детей": True,
            "Черная высота одинакова для всех путей": True
        }

        if self.root != self.NIL and self.root.color != RBNode.BLACK:
            properties["Корень черный"] = False

        properties["Красный узел имеет черных детей"] = self._check_red_property(self.root)

        black_heights = set()
        self._collect_black_heights(self.root, 0, black_heights)
        properties["Черная высота одинакова для всех путей"] = len(black_heights) <= 1

        return properties

    def _check_red_property(self, node):
        if node == self.NIL:
            return True

        if node.color == RBNode.RED:
            if (node.left != self.NIL and node.left.color != RBNode.BLACK or
                    node.right != self.NIL and node.right.color != RBNode.BLACK):
                return False

        return (self._check_red_property(node.left) and
                self._check_red_property(node.right))

    def _collect_black_heights(self, node, current_black, black_heights):
        if node == self.NIL:
            black_heights.add(current_black)
            return

        # ++  если узел черный
        next_black = current_black + (1 if node.color == RBNode.BLACK else 0)

        self._collect_black_heights(node.left, next_black, black_heights)
        self._collect_black_heights(node.right, next_black, black_heights)

    def insert_with_steps(self, val):

        print(f"Вставка значения {val}")

        print("Структура дерева ДО вставки:")
        if self.root == self.NIL:
            print("Дерево пустое")
        else:
            self.print_tree()

        self.insert(val)

        print(f"\nСтруктура дерева ПОСЛЕ вставки {val}:")
        self.print_tree()

        # провекра свойства
        properties = self.check_rb_properties()
        #print("\nПроверка свойств красно-черного дерева:")
        for prop, value in properties.items():
            status = " да " if value else " нет "
            #print(f"  {status} {prop}")

def main():
    print("КЧ дерево (RED-BLACK)")

    rb1 = RBTree()
    test_seq1 = [7, 3, 18, 10, 22, 8, 11, 26]
    print("1 последовательность ", test_seq1)
    print("" + '_' * 50)

    for val in test_seq1:
        rb1.insert_with_steps(val)

    print("\nДерево:")
    rb1.print_tree()

    properties = rb1.check_rb_properties()
    print("\nПроверка всех свойств кч дерева:")
    all_valid = True
    for prop, value in properties.items():
        status = " да " if value else " нет "
        print(f"  {status}: {prop}")

    print("\n" + '_' * 50)
    print("2 Несбалансированная последовательность [1, 2, 3, 4, 5, 6, 7]")
    rb2 = RBTree()
    unbalanced_seq = [1, 2, 3, 4, 5, 6, 7]

    for val in unbalanced_seq:
        rb2.insert(val)

    rb2.print_tree()

    print("\n" + '_' * 50)
    print("3 Удаление элементов")

    rb3 = RBTree()
    delete_seq = [50, 30, 70, 20, 40, 60, 80, 35, 45]

    print("\nСоздаем дерево из значений:", delete_seq)
    for val in delete_seq:
        rb3.insert(val)

    print("\nИсходное дерево:")
    rb3.print_tree()

    deletions = [30, 50, 70]


    for val in deletions:
        print(f"\nУдаляем значение {val}:")
        rb3.delete(val)
        rb3.print_tree()

        # Проверяем свойства после каждого удаления
        properties = rb3.check_rb_properties()
        valid = all(properties.values())
        print(f"Свойства сохранены: {' да ' if valid else ' нет '}")


    print("\n" + "-" * 50 + "\n4 Случайные данные")

    import random
    rb_random = RBTree()
    random_data = random.sample(range(1, 101), 15)

    print(f"\nСлучайные данные: {sorted(random_data)}")

    for val in random_data:
        rb_random.insert(val)

    print("\nСтруктура дерева:")
    rb_random.print_tree()

    properties = rb_random.check_rb_properties()
    print("\nПроверка свойств для случайных данных:")
    for prop, value in properties.items():
        status = " да " if value else " нет "
        print(f"  {status} {prop}")


if __name__ == "__main__":
    main()
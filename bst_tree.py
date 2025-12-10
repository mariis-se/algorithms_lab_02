class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if self.root is None:
            self.root = BSTNode(val)
        else:
            self._insert_recursive(self.root, val)

    def _insert_recursive(self, node, val):
        if val < node.val:
            if node.left is None:
                node.left = BSTNode(val)
            else:
                self._insert_recursive(node.left, val)
        elif val > node.val:
            if node.right is None:
                node.right = BSTNode(val)
            else:
                self._insert_recursive(node.right, val)
        # если значение уже есть проспусак

    def search(self, val):
        return self._search_recursive(self.root, val)

    def _search_recursive(self, node, val):
        if node is None:
            return False
        if val == node.val:
            return True
        elif val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)

    def delete(self, val):
        self.root = self._delete_recursive(self.root, val)

    def _delete_recursive(self, node, val):
        if node is None:
            return None
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:

            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # узел с двумя потомками

            min_val = self._find_min_node(node.right).val
            node.val = min_val
            # удаляем
            node.right = self._delete_recursive(node.right, min_val)

        return node

    def _find_min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def find_min(self):
        if self.root is None:
            return None
        current = self.root
        while current.left is not None:
            current = current.left
        return current.val

    def find_max(self):
        if self.root is None:
            return None
        current = self.root
        while current.right is not None:
            current = current.right
        return current.val

    # обходы
    def inorder(self):     # центрированный обход , возвращает отсортированные значения
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.val)
            self._inorder_recursive(node.right, result)

    def preorder(self):   # прямой обход (корень ,левое поддерево, правое поддерево)
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node is not None:
            result.append(node.val)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder(self):  #Обратный обход (левое поддерево , правое поддерево, корень)
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node is not None:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.val)

    def bfs(self):  # обход в ширину по уровням
        if self.root is None:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def print_tree(self):
        print("\nСтруктура:\n")
        if self.root is None:
            print("Дерево пустое")
            return
        self._print_tree_recursive(self.root, "", True)

    def _print_tree_recursive(self, node, prefix, is_left):
        #рекурсивный вывод
        if node is not None:
            print(prefix + ("  left: " if is_left else " right: ") + str(node.val))

            i = "    " if is_left else "|   "
            new_prefix = prefix + i

            #рекурсивный вывод подддеревьев
            if node.right is not None or node.left is not None:
                if node.right:
                    self._print_tree_recursive(node.right, new_prefix, False)
                else:
                    print(new_prefix + " right: None")

                if node.left:
                    self._print_tree_recursive(node.left, new_prefix, True)
                else:
                    print(new_prefix + "  left:None")



def main():
    print("Бинарное дерево поиска (BST)")

    bst = BST()
    numbers = [50, 30, 70, 20, 40, 60, 80, 35, 45, 65, 75, 85, 10, 25, 1]

    print("\n1 Вставка элементов в дерево:")
    print(f"   Числа: {numbers}")

    for num in numbers:
        bst.insert(num)

    print("\n2 Поиск элементов в дереве:")
    search_values = [40, 25, 70, 100, 35, 90]
    for val in search_values:
        found = bst.search(val)
        print(f"   Поиск {val:3}: {' Найден' if found else ' Не найден'}")

    print(f"   Минимальное значение: {bst.find_min()}")
    print(f"   Максимальное значение: {bst.find_max()}")

    print(f"\n4 Обходы:")
    print(f"   Прямой обход (preorder): {bst.preorder()}")
    print(f"   Центрированный обход (inorder): {bst.inorder()}")
    print(f"   Обратный обход (postorder): {bst.postorder()}")
    print(f"   Обход в ширину (BFS): {bst.bfs()}")

    bst.print_tree()

    print("\n5 Удаление элементов:")

    bst.delete(10)
    print("Удалили лист 10")
    print(f"Inorder после удаления: {bst.inorder()}")

    bst.delete(20)
    print("\nУдалили узел 20 (имел одного потомка)")
    print(f"Inorder после удаления: {bst.inorder()}")

    bst.delete(50)
    print("\nУдалили узел 50 (имел двух потомков)")
    print(f"Inorder после удаления: {bst.inorder()}")

    print("\n6 Проверка:")
    print(f"   Новый минимум: {bst.find_min()}")
    print(f"   Новый максимум: {bst.find_max()}")

    print("\nПоиск удаленных элементов:")
    for val in [10, 20, 50]:
        found = bst.search(val)
        print(f"   Поиск {val:3}: {' Найден' if found else ' Не найден'}")

    print("\n7 Итоговый вид дерева:")
    bst.print_tree()

    print("Несбалансированное BST:")
    print("_" * 50)

    # худший случай
    bst_unbalanced = BST()
    sorted_numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    print(f"\nВставляем отсортированную последовательность: {sorted_numbers}")
    for num in sorted_numbers:
        bst_unbalanced.insert(num)

    print(f"\nBFS обход (показывает вырожденную структуру):")
    print(f"  {bst_unbalanced.bfs()}")

    print(f"\nInorder обход (всегда отсортирован):")
    print(f"  {bst_unbalanced.inorder()}")

if __name__ == "__main__":
    main()



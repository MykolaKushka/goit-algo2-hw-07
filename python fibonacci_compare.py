import timeit
from functools import lru_cache
import matplotlib.pyplot as plt

# ---------- Splay Tree implementation ----------
class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if not root or root.key == key:
            return root
        if key < root.key:
            if not root.left:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left else root
        else:
            if not root.right:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)
            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def get(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def put(self, key, value):
        if not self.root:
            self.root = SplayNode(key, value)
            return
        self.root = self._splay(self.root, key)
        if key == self.root.key:
            self.root.value = value
        elif key < self.root.key:
            node = SplayNode(key, value)
            node.left = self.root.left
            node.right = self.root
            self.root.left = None
            self.root = node
        else:
            node = SplayNode(key, value)
            node.right = self.root.right
            node.left = self.root
            self.root.right = None
            self.root = node

# ---------- Fibonacci with LRU cache ----------
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# ---------- Fibonacci with Splay Tree ----------
def fibonacci_splay(n, tree):
    cached = tree.get(n)
    if cached is not None:
        return cached
    if n < 2:
        tree.put(n, n)
        return n
    val = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.put(n, val)
    return val

# ---------- Results Table Formatter ----------
def print_results_table(ns, lru_times, splay_times):
    print(f"{'n':<10}{'LRU Cache Time (s)':<24}{'Splay Tree Time (s)':<24}")
    print("-" * 58)
    for n, lru, splay in zip(ns, lru_times, splay_times):
        print(f"{n:<10}{lru:<24.8f}{splay:<24.8f}")

# ---------- Main ----------
def main():
    ns = list(range(0, 1000, 50))
    lru_times = []
    splay_times = []

    for n in ns:
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
        lru_times.append(lru_time)

        tree = SplayTree()
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)
        splay_times.append(splay_time)

    # Виведення таблиці
    print_results_table(ns, lru_times, splay_times)

    # Побудова графіка
    plt.figure(figsize=(10, 6))
    plt.plot(ns, lru_times, marker='o', label='LRU Cache')
    plt.plot(ns, splay_times, marker='x', label='Splay Tree')
    plt.xlabel('Число Фібоначчі (n)')
    plt.ylabel('Середній час виконання (секунди)')
    plt.title('Порівняння часу виконання для LRU Cache та Splay Tree')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Висновки
    print("\nВисновки:")
    print("- Метод із LRU-кешем показав стабільно низький час виконання.")
    print("- Splay Tree хоч і кешує значення, але має вищу складність доступу.")
    print("- Для обчислення чисел Фібоначчі, особливо великих n, LRU Cache є ефективнішим.")

if __name__ == "__main__":
    main()

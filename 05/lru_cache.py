class Node:
    """Узел двусвязного списка."""

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, limit=42):
        self.cache = {}
        self.limit = limit
        self.size = 0

        self.head = Node()
        self.tail = Node()

        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Удаляет узел из двусвязного списка."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node):
        """Добавляет узел в начало (сразу после головы)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """Получает значение по ключу. Если ключ не найден, возвращает None."""
        if key not in self.cache:
            return None

        node = self.cache[key]
        self._remove(node)
        self._add(node)

        return node.value

    def set(self, key, value):
        """Добавляет или обновляет значение по ключу."""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)
            self.size += 1

            if self.size > self.limit:
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]
                self.size -= 1

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

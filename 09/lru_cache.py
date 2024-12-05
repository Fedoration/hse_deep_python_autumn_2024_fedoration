import logging
import argparse
import sys


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
            logging.info("Get: key '%s' not found.", key)
            return None

        node = self.cache[key]
        self._remove(node)
        self._add(node)
        logging.info("Get: key '%s' found with value '%s'.", key, node.value)
        return node.value

    def set(self, key, value):
        """Добавляет или обновляет значение по ключу."""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add(node)
            logging.info("Set: updated existing key '%s' with value '%s'.", key, value)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)
            self.size += 1
            logging.info("Set: added new key '%s' with value '%s'.", key, value)

            if self.size > self.limit:
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]
                self.size -= 1
                logging.warning(
                    "Set: capacity reached. Removed LRU key '%s'.", lru_node.key
                )

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)


def configure_logging(args):
    """Настраивает логирование."""
    handlers = [logging.FileHandler("cache.log")]

    if args.s:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(logging.Formatter("%(message)s"))
        handlers.append(stdout_handler)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=handlers,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    if args.f:

        class CustomFilter(logging.Filter):
            def filter(self, record):
                # Пример фильтра: исключаем сообщения с четным количеством слов
                return len(record.msg.split()) % 2 != 0

        for handler in handlers:
            handler.addFilter(CustomFilter())


def main():
    """Пример использования LRUCache с логированием."""
    parser = argparse.ArgumentParser(description="LRUCache logging example.")
    parser.add_argument("-s", action="store_true", help="Log to stdout.")
    parser.add_argument("-f", action="store_true", help="Apply custom filter.")
    args = parser.parse_args()

    configure_logging(args)

    cache = LRUCache(limit=3)
    cache.set("a", 1)  # добавление нового ключа
    cache.set("b", 2)  # добавление нового ключа
    cache.set("c", 3)  # добавление нового ключа
    cache.get("a")  # доступ к существующему ключу
    cache.get("d")  # доступ к отсутствующему ключу
    cache.set("d", 4)  # добавление нового ключа с вытеснением
    cache.set("b", 5)  # обновление существующего ключа


if __name__ == "__main__":
    main()

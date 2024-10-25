import socket
import threading
from collections import Counter
import requests


class Worker(threading.Thread):
    """Класс для обработки запросов клиентов"""

    def __init__(self, connection, address, k, task_tracker):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.k = k
        self.task_tracker = task_tracker

    def run(self):
        try:
            url = self.connection.recv(1024).decode()
            response = requests.get(url, timeout=5)
            words = response.text.lower().split()
            word_count = Counter(words)
            most_common_words = dict(word_count.most_common(self.k))
            self.connection.sendall(str(most_common_words).encode())

            # Увеличиваем счетчик выполненных задач
            self.task_tracker["completed_urls"] += 1
            print(f"Total URLs processed: {self.task_tracker['completed_urls']}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            self.connection.sendall(b"{'error': 'Timeout or network error'}")
        finally:
            self.connection.close()


class Server:
    """Класс для запуска сервера"""

    def __init__(self, host, port, num_workers, k):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.k = k
        self.task_tracker = {"completed_urls": 0}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server listening on {self.port}")

        while True:
            connection, address = self.socket.accept()
            worker = Worker(connection, address, self.k, self.task_tracker)
            worker.start()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 5:
        print("Usage: python server.py <host> <port> <num_workers> <k>")
        sys.exit(1)

    host_arg, port_arg, num_workers_arg, k_arg = (
        sys.argv[1],
        int(sys.argv[2]),
        int(sys.argv[3]),
        int(sys.argv[4]),
    )
    server = Server(host_arg, port_arg, num_workers_arg, k_arg)
    server.start()

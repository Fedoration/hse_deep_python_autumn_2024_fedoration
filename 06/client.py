import threading
import socket


class ClientThread(threading.Thread):
    def __init__(self, host, port, urls):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.urls = urls

    def run(self):
        # Подключаемся к серверу и отправляем URL
        for url in self.urls:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(url.encode())
                data = s.recv(1024).decode()
                print(f"{url}: {data}")


class Client:
    def __init__(self, host, port, num_threads, url_file):
        self.host = host
        self.port = port
        self.num_threads = num_threads
        with open(url_file, "r", encoding="utf-8") as file:
            self.urls = file.read().splitlines()

    def start(self):
        num_urls = len(self.urls)
        chunk_size = max(1, num_urls // self.num_threads)
        threads = []

        # Разбиваем список URL на части для каждого потока
        for i in range(0, num_urls, chunk_size):
            chunk = self.urls[i : i + chunk_size]
            client_thread = ClientThread(self.host, self.port, chunk)
            threads.append(client_thread)
            client_thread.start()

        for t in threads:
            t.join()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 5:
        print("Usage: python client.py <host> <port> <num_threads> <url_file>")
        sys.exit(1)

    host_arg, port_arg, num_threads_arg, url_file_arg = (
        sys.argv[1],
        int(sys.argv[2]),
        int(sys.argv[3]),
        sys.argv[4],
    )
    client = Client(host_arg, port_arg, num_threads_arg, url_file_arg)
    client.start()

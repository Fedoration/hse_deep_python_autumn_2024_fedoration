import unittest
from unittest.mock import patch, MagicMock
import subprocess
import time
import socket

from server import Worker


class TestClientServerInteraction(unittest.TestCase):

    def setUp(self):
        print("Starting server...")
        self.server_process = subprocess.Popen(
            ["python", "server.py", "localhost", "8888", "10", "3"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(2)

    def tearDown(self):
        print("Stopping server...")
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

    def test_server_is_running(self):
        """Подключаемся к серверу чтобы удостовериться, что он работает"""
        print("Checking if server is running...")
        try:
            with socket.create_connection(("localhost", 8888), timeout=3) as sock:
                self.assertTrue(sock)
        except Exception as e:
            self.fail(f"Server is not running: {e}")

    def test_client_server_interaction(self):
        """ "Тестируем взаимодействие клиента и сервера"""
        print("Testing client-server interaction...")
        result = subprocess.run(
            ["python", "client.py", "localhost", "8888", "3", "urls.txt"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        output = result.stdout.strip().split("\n")
        self.assertGreater(len(output), 0, "No output from client.")

    @patch("client.socket.socket")
    def test_mock_client_interaction(self, mock_socket):
        """Тестируем взаимодействие клиента и сервера с использованием моков"""
        mock_conn = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_conn

        # Заполним mock urls
        urls = ["http://example.com", "http://example.org"]
        mock_conn.recv.return_value = b'{"word": 2}'

        for url in urls:
            with socket.create_connection(("localhost", 8888)) as sock:
                sock.sendall(url.encode())
                response = sock.recv(1024).decode()
                self.assertEqual(response, '{"word": 2}')

        # Проверка, что соединение инициировалось для каждого URL
        self.assertEqual(mock_conn.sendall.call_count, len(urls))

    @patch("server.requests.get")
    def test_mock_server_processing(self, mock_get):
        """Тестируем обработку сервером запросов клиента с использованием моков"""
        mock_response = MagicMock()
        mock_response.text = "word1 word2 word1 word2 word3"
        mock_get.return_value = mock_response

        # Создаем Mock соединение и передаем его в Worker
        connection = MagicMock()
        connection.recv.return_value = b"http://example.com"
        task_tracker = {"completed_urls": 0}

        worker = Worker(connection, ("localhost", 8889), 2, task_tracker)
        worker.run()

        # Проверка, что правильные данные были отправлены обратно по socket
        connection.sendall.assert_called_once_with(b"{'word1': 2, 'word2': 2}")

        # Проверка, что счетчик завершенных урлов увеличился
        self.assertEqual(task_tracker["completed_urls"], 1)


if __name__ == "__main__":
    unittest.main()

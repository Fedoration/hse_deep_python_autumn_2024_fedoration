import unittest

from retry_decorator import retry_deco


class TestRetryDecorator(unittest.TestCase):

    def test_success_on_first_attempt(self):
        """Проверяем корректное выполение на первой попытке"""
        attempts = {"count": 0}

        @retry_deco(max_retries=3)
        def func():
            attempts["count"] += 1
            return "success"

        self.assertEqual(func(), "success")
        self.assertEqual(attempts["count"], 1)

    def test_success_on_retry(self):
        """Проверяем корректное выполение на второй попытке"""
        attempts = {"count": 0}

        @retry_deco(max_retries=3)
        def func():
            attempts["count"] += 1
            if attempts["count"] < 2:
                raise ValueError("Try again")
            return "success"

        self.assertEqual(func(), "success")
        self.assertEqual(attempts["count"], 2)

    def test_fail_with_specific_exception(self):
        """Проверяет на передачу исключения в декоратор"""
        attempts = {"count": 0}

        @retry_deco(max_retries=3, exceptions=[ValueError])
        def func():
            attempts["count"] += 1
            raise ValueError("Stop retrying")

        self.assertIsNone(func())
        self.assertEqual(attempts["count"], 1)

    def test_other_exception_does_not_stop_retries(self):
        """Проверяет, что другие исключения не приводят к завершению попыток"""
        attempts = {"count": 0}

        @retry_deco(max_retries=3, exceptions=[ValueError])
        def func():
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise TypeError("Retry")
            return "success"

        self.assertEqual(func(), "success")
        self.assertEqual(attempts["count"], 3)

    def test_no_exceptions_passed(self):
        """Проверяем, что достигнуто маскимальное количество попыток"""
        attempts = {"count": 0}

        @retry_deco(max_retries=3)
        def func():
            attempts["count"] += 1
            raise ValueError("Fail with no exception filter")

        self.assertIsNone(func())
        self.assertEqual(attempts["count"], 3)


if __name__ == "__main__":
    unittest.main()

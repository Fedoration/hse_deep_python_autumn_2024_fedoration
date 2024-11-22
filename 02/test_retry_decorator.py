import unittest
from unittest.mock import patch
from retry_decorator import retry_deco


class TestRetryDecorator(unittest.TestCase):

    def test_success_on_first_attempt(self):
        """Проверяем корректное выполнение на первой попытке"""
        attempts = {"count": 0}

        @retry_deco(max_retries=3)
        def func():
            attempts["count"] += 1
            return "success"

        self.assertEqual(func(), "success")
        self.assertEqual(attempts["count"], 1)

    def test_success_on_retry(self):
        """Проверяем корректное выполнение на второй попытке"""
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
        """Перевыброс разрешенного исключения"""
        attempts = {"count": 0}

        @retry_deco(max_retries=3, exceptions=[ValueError])
        def func():
            attempts["count"] += 1
            raise ValueError("Stop retrying")

        with self.assertRaises(ValueError):
            func()

        self.assertEqual(attempts["count"], 1)

    def test_fail_with_other_exception_after_retries(self):
        """Перевыброс последнего исключения после исчерпания попыток"""
        attempts = {"count": 0}

        @retry_deco(max_retries=3, exceptions=[ValueError])
        def func():
            attempts["count"] += 1
            raise TypeError("Retry")

        with self.assertRaises(TypeError):
            func()

        self.assertEqual(attempts["count"], 3)

    def test_check_output(self):
        """Проверяем вывод декоратора"""
        attempts = {"count": 0}

        @retry_deco(max_retries=2)
        def func():
            attempts["count"] += 1
            if attempts["count"] < 2:
                raise ValueError("Try again")
            return "success"

        with patch("builtins.print") as mock_print:
            self.assertEqual(func(), "success")

            # Проверяем, что вывод декоратора соответствует ожидаемому
            mock_print.assert_any_call(
                "run 'func' with args=(), kwargs={}, attempt=1, exception=ValueError"
            )
            mock_print.assert_any_call(
                "run 'func' with args=(), kwargs={}, attempt=2, result=success"
            )

    def test_retry_exceptions_order(self):
        """Проверяем, что разрешенные исключения отлавливаются раньше других"""
        attempts = {"count": 0}

        @retry_deco(max_retries=3, exceptions=[ValueError])
        def func():
            attempts["count"] += 1
            if attempts["count"] == 1:
                raise ValueError("Stop retrying")
            raise TypeError("Retry again")

        with self.assertRaises(ValueError):
            func()

        self.assertEqual(attempts["count"], 1)


if __name__ == "__main__":
    unittest.main()

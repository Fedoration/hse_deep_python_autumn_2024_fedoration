import unittest
from retry_decorator import retry_deco


@retry_deco(max_retries=3)
def success_function(x):
    return x


@retry_deco(max_retries=3)
def always_failing_function():
    raise ValueError("This always fails")


@retry_deco(max_retries=3, exceptions=[ValueError])
def stop_on_value_error():
    raise ValueError("Stop retrying on this error")


@retry_deco(max_retries=3)
def succeeds_after_two_failures():
    if succeeds_after_two_failures.attempts < 2:
        succeeds_after_two_failures.attempts += 1
        raise RuntimeError("Temporary error")
    return "Success"


succeeds_after_two_failures.attempts = 0


class TestRetryDecorator(unittest.TestCase):
    def test_successful_function(self):
        """Проверяет, что функция без ошибок завершается успешно"""
        result = success_function(5)
        self.assertEqual(result, 5)

    def test_always_failing_function(self):
        """Проверяет, что функция всегда выдает None после максимального количества попыток"""
        result = always_failing_function()
        self.assertIsNone(result)

    def test_stop_on_specific_exception(self):
        """Проверяет, что декоратор корректно обрабатывает исключение ValueError"""
        result = stop_on_value_error()
        self.assertIsNone(result)

    def test_succeeds_after_retries(self):
        """Проверяет, что функция успешно завершается после нескольких неудачных попыток"""
        succeeds_after_two_failures.attempts = 0
        result = succeeds_after_two_failures()
        self.assertEqual(result, "Success")

    def test_retry_limit(self):
        """Проверяет, что декоратор корректно ограничивает количество попыток"""
        retry_count = 5

        @retry_deco(max_retries=retry_count)
        def failing_func():
            raise RuntimeError("This always fails")

        result = failing_func()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

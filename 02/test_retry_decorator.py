import unittest
from retry_decorator import retry_deco


# Sample functions to test the retry_decorator
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
        """Test that a function without errors runs successfully"""
        result = success_function(5)
        self.assertEqual(result, 5)

    def test_always_failing_function(self):
        """Test that a function always fails after maximum retries"""
        result = always_failing_function()
        self.assertIsNone(result)

    def test_stop_on_specific_exception(self):
        """Test that retries stop when a specific exception is raised"""
        result = stop_on_value_error()
        self.assertIsNone(result)  # Should stop immediately since ValueError is raised

    def test_succeeds_after_retries(self):
        """Test that a function succeeds after a few retries"""
        succeeds_after_two_failures.attempts = 0  # Reset attempt count for test
        result = succeeds_after_two_failures()
        self.assertEqual(result, "Success")

    def test_retry_limit(self):
        """Test if retry limit is respected and fails after the max retries"""
        retry_count = 5

        @retry_deco(max_retries=retry_count)
        def failing_func():
            raise RuntimeError("This always fails")

        result = failing_func()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

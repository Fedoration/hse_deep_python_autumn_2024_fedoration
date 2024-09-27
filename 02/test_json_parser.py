import unittest
from unittest.mock import MagicMock

from json_parser import (
    convert_to_lower_remove_punct,
    process_json,
)


class TestJsonParserFunctions(unittest.TestCase):

    def test_convert_to_lower_remove_punct(self):
        """Приведение к нижнему регистру и удаление пунктуации"""

        self.assertEqual(convert_to_lower_remove_punct("Hello, World!"), "hello world")

        self.assertEqual(
            convert_to_lower_remove_punct("This is a Test"), "this is a test"
        )

        self.assertEqual(convert_to_lower_remove_punct("?!.,:"), "")

        self.assertEqual(convert_to_lower_remove_punct(""), "")

        self.assertEqual(convert_to_lower_remove_punct("12345"), "12345")

    def test_process_json_valid(self):
        """Проверяем корректность обработки JSON на двух вызовах"""
        callback = MagicMock()

        json_str = '{"name": "Hello, World!", "description": "A test description"}'
        process_json(
            json_str,
            required_keys=["name", "description"],
            tokens=["hello", "test"],
            callback=callback,
        )

        callback.assert_any_call("name", "hello")
        callback.assert_any_call("description", "test")
        self.assertEqual(callback.call_count, 2)

    def test_process_json_missing_required_keys(self):
        """Обработка JSON строки с отсутствующими ключами"""
        callback = MagicMock()

        json_str = '{"name": "Hello, World!"}'
        process_json(
            json_str,
            required_keys=["name", "description"],
            tokens=["hello"],
            callback=callback,
        )

        callback.assert_called_once_with("name", "hello")

    def test_process_json_no_tokens(self):
        """Валидная JSON строка, но без токенов"""
        callback = MagicMock()

        json_str = '{"name": "Hello, World!"}'
        process_json(json_str, required_keys=["name"], tokens=[], callback=callback)

        callback.assert_not_called()

    def test_process_json_no_required_keys(self):
        """Валидная JSON строка, но нет ключей"""
        callback = MagicMock()

        json_str = '{"name": "Hello, World!"}'
        process_json(json_str, required_keys=[], tokens=["hello"], callback=callback)

        callback.assert_not_called()

    def test_process_json_invalid_json(self):
        """Проверяем обработку невалидной JSON строки"""

        json_str = '{"name": "Hello, World!", "description": "A test description"'

        with self.assertRaises(ValueError):
            process_json(json_str, required_keys=["name"], tokens=["hello"])

    def test_process_json_all_missing_required_keys(self):
        """Обработка JSON строки со всеми отсутствующими ключами"""
        callback = MagicMock()

        json_str = '{"name": "Hello, World!"}'
        process_json(
            json_str,
            required_keys=["some_key", "description"],
            tokens=["hello"],
            callback=callback,
        )

        callback.assert_not_called()

    def test_process_json_all_missing_tokens(self):
        """Обработка JSON строки со всеми отсутствующими токенами"""
        callback = MagicMock()

        json_str = '{"name": "Hello, World!", "description": "A test description"}'
        process_json(
            json_str,
            required_keys=["some_key", "description"],
            tokens=["hi", "bonjour"],
            callback=callback,
        )

        callback.assert_not_called()

    def test_check_case_dependence(self):
        """Проверяем корректность обработки JSON на двух вызовах"""
        callback = MagicMock()

        json_str = '{"name": "Hello, World!", "Description": "A test description"}'
        process_json(
            json_str,
            required_keys=["name", "Description", "Name", "description"],
            tokens=["hello", "World", "test"],
            callback=callback,
        )

        callback.assert_any_call("name", "hello")
        callback.assert_any_call("name", "World")
        callback.assert_any_call("Description", "test")
        self.assertEqual(callback.call_count, 3)


if __name__ == "__main__":
    unittest.main()

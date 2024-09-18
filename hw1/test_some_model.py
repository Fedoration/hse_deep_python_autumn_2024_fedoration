import unittest
from unittest import mock

import hw1.some_model as some_model


class TestSomeModel(unittest.TestCase):

    def test_bad_well_good(self):
        """Проверяем стандартные случаи на пороги"""
        with mock.patch("some_model.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.9
            result = some_model.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.3, good_thresholds=0.8
            )
            self.assertEqual("отл", result)

            mock_fetch.return_value = 0.5
            result = some_model.predict_message_mood(
                "Чапаев", bad_thresholds=0.3, good_thresholds=0.8
            )
            self.assertEqual("норм", result)

            mock_fetch.return_value = 0.2
            result = some_model.predict_message_mood(
                "Чак чак", bad_thresholds=0.3, good_thresholds=0.8
            )
            self.assertEqual("неуд", result)

    def test_coincidence_with_thresholds(self):
        """Проверяем совпадение с порогами"""
        with mock.patch("some_model.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.3
            result = some_model.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.3, good_thresholds=0.8
            )
            self.assertEqual("норм", result)

        with mock.patch("some_model.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.8
            result = some_model.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.3, good_thresholds=0.8
            )
            self.assertEqual("норм", result)

    def test_same_thresholds(self):
        """Проверяем случай, когда пороги совпадают"""
        with mock.patch("some_model.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.5
            result = some_model.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.5, good_thresholds=0.5
            )
            self.assertEqual("норм", result)

        with mock.patch("some_model.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.8
            result = some_model.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.5, good_thresholds=0.5
            )
            self.assertEqual("отл", result)

        with mock.patch("some_model.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.4
            result = some_model.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.5, good_thresholds=0.5
            )
            self.assertEqual("неуд", result)

    def test_zero_thresholds(self):
        """Проверяем случай, когда пороги равны 0"""
        with mock.patch("some_model.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.5
            result = some_model.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0, good_thresholds=0
            )
            self.assertEqual("отл", result)

        with mock.patch("some_model.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0
            result = some_model.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0, good_thresholds=0
            )
            self.assertEqual("норм", result)


if __name__ == "__main__":
    unittest.main()

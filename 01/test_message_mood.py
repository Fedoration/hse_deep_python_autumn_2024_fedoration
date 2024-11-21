import unittest
from unittest import mock
import message_mood


class TestMessageMood(unittest.TestCase):

    def test_bad_well_good(self):
        """Проверяем стандартные случаи на пороги"""
        with mock.patch("message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.9
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.3, good_thresholds=0.8
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("отл", result)

            mock_fetch.reset_mock()
            mock_fetch.return_value = 0.5
            result = message_mood.predict_message_mood(
                "Чапаев", bad_thresholds=0.3, good_thresholds=0.8
            )
            mock_fetch.assert_called_once_with("Чапаев")
            self.assertEqual("норм", result)

            mock_fetch.reset_mock()
            mock_fetch.return_value = 0.2
            result = message_mood.predict_message_mood(
                "Чак чак", bad_thresholds=0.3, good_thresholds=0.8
            )
            mock_fetch.assert_called_once_with("Чак чак")
            self.assertEqual("неуд", result)

    def test_coincidence_with_thresholds(self):
        """Проверяем совпадение с порогами"""
        with mock.patch("message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.3
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.3, good_thresholds=0.8
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("норм", result)

        with mock.patch("message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.8
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.3, good_thresholds=0.8
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("норм", result)

    def test_same_thresholds(self):
        """Проверяем случай, когда пороги совпадают"""
        with mock.patch("message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.5
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.5, good_thresholds=0.5
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("норм", result)

        with mock.patch("message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.8
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.5, good_thresholds=0.5
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("отл", result)

        with mock.patch("message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.4
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.5, good_thresholds=0.5
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("неуд", result)

    def test_close_to_thresholds(self):
        """Проверяем случаи, когда значение предикта близко к порогам"""
        with mock.patch("message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.299
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.3, good_thresholds=0.8
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("неуд", result)

            mock_fetch.reset_mock()
            mock_fetch.return_value = 0.301
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.3, good_thresholds=0.8
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("норм", result)

            mock_fetch.reset_mock()
            mock_fetch.return_value = 0.799
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.3, good_thresholds=0.8
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("норм", result)

            mock_fetch.reset_mock()
            mock_fetch.return_value = 0.801
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0.3, good_thresholds=0.8
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("отл", result)

    def test_zero_thresholds(self):
        """Проверяем случай, когда пороги равны 0"""
        with mock.patch("message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0.5
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0, good_thresholds=0
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("отл", result)

        with mock.patch("message_mood.SomeModel.predict") as mock_fetch:
            mock_fetch.return_value = 0
            result = message_mood.predict_message_mood(
                "Чапаев и пустота", bad_thresholds=0, good_thresholds=0
            )
            mock_fetch.assert_called_once_with("Чапаев и пустота")
            self.assertEqual("норм", result)


if __name__ == "__main__":
    unittest.main()

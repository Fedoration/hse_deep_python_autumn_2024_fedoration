import unittest
from io import StringIO
from file_reader import file_reader


class TestFileReader(unittest.TestCase):
    def test_single_match(self):
        """Проверка строки с совпадением одного слова."""
        file_content = StringIO("Роза упала на лапу Азора\nСократ любит спор\n")
        words_to_search = ["роза"]
        stopwords = []

        result = list(file_reader(file_content, words_to_search, stopwords))
        self.assertEqual(result, ["Роза упала на лапу Азора"])

    def test_stopword_in_line(self):
        """Проверка игнорирования строки с присутствием стоп-слова."""
        file_content = StringIO("Роза упала на лапу Азора\nСократ любит спор\n")
        words_to_search = ["роза", "сократ"]
        stopwords = ["азора"]

        result = list(file_reader(file_content, words_to_search, stopwords))
        self.assertEqual(result, ["Сократ любит спор"])

    def test_case_insensitive_search_and_stopwords(self):
        """Проверка регистронезависимого поиска и стоп-слов."""
        file_content = StringIO("РОЗА упала на лапу Азора\nСОКРАТ любит спор\n")
        words_to_search = ["роза", "сократ"]
        stopwords = ["азора"]

        result = list(file_reader(file_content, words_to_search, stopwords))
        self.assertEqual(result, ["СОКРАТ любит спор"])

    def test_match_entire_line(self):
        """Проверка совпадения строки поиска/стоп-слова с целой строкой."""
        file_content = StringIO("Роза\nАзора\nСократ\n")
        words_to_search = ["роза", "сократ"]
        stopwords = ["азора"]

        result = list(file_reader(file_content, words_to_search, stopwords))
        self.assertEqual(result, ["Роза", "Сократ"])

    def test_empty_file(self):
        """Проверка пустого файла."""
        file_content = StringIO("")
        words_to_search = ["роза"]
        stopwords = []

        result = list(file_reader(file_content, words_to_search, stopwords))
        self.assertEqual(result, [])

    def test_no_match(self):
        """Проверка строки без совпадений."""
        file_content = StringIO("Сократ любит лаванду\nПлатон любит жареный креветки\n")
        words_to_search = ["роза"]
        stopwords = []

        result = list(file_reader(file_content, words_to_search, stopwords))
        self.assertEqual(result, [])

    def test_match_with_stopword_in_other_line(self):
        """Проверка, что стоп-слова из других строк не влияют на результат."""
        file_content = StringIO(
            "Роза упала на лапу Азора\nСократ посадил дерево\nПлатон полил дерево\n"
        )
        words_to_search = ["дерево"]
        stopwords = ["азора"]

        result = list(file_reader(file_content, words_to_search, stopwords))
        self.assertEqual(result, ["Сократ посадил дерево", "Платон полил дерево"])

    def test_file_path_as_input(self):
        """Проверка работы с именем файла."""
        with open("test_file.txt", "w", encoding="utf-8") as file:
            file.write("Роза упала на лапу Азора\nСократ любит спор\n")

        words_to_search = ["роза"]
        stopwords = ["сократ"]

        result = list(file_reader("test_file.txt", words_to_search, stopwords))
        self.assertEqual(result, ["Роза упала на лапу Азора"])

    def test_boundary_cases(self):
        """Проверка граничных случаев."""
        file_content = StringIO(
            " , , ,\n"  # Только запятые и пробелы
            "\n"  # Пустая строка
            "   \n"  # Пробельная строка
            "Сократ!\n"  # Слово со знаком
        )
        words_to_search = ["сократ"]
        stopwords = []

        result = list(file_reader(file_content, words_to_search, stopwords))
        self.assertEqual(result, ["Сократ!"])

    def test_multiple_lines_with_and_without_matches(self):
        """Проверка работы с несколькими строками,
        часть из которых содержит совпадения, а часть — нет.
        """
        file_content = StringIO(
            "Роза упала\nСократ выиграл спор\nСократ и Платон выпили вино\n"
        )
        words_to_search = ["сократ", "платон"]
        stopwords = ["роза"]

        result = list(file_reader(file_content, words_to_search, stopwords))
        self.assertEqual(
            result,
            [
                "Сократ выиграл спор",
                "Сократ и Платон выпили вино",
            ],
        )


if __name__ == "__main__":
    unittest.main()

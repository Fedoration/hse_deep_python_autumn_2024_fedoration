from typing import Generator, Optional, TextIO, Union
import string


def convert_to_lower_remove_punct(line: str) -> str:
    """Преобразует строку в нижний регистр и удаляет пунктуацию."""
    line = line.lower().strip()
    return line.translate(str.maketrans("", "", string.punctuation))


def filter_line(
    line: str, words_to_search: list[str], stopwords: list[str]
) -> Optional[str]:
    """Фильтрует строку по наличию слов для поиска и отсутствию стоп-слов."""
    has_search_word = False
    lowercase_line = convert_to_lower_remove_punct(line)

    for word in lowercase_line.split():
        if word in map(str.lower, stopwords):
            return None

        if word in map(str.lower, words_to_search):
            has_search_word = True

    if has_search_word:
        return line.strip()

    return None


def file_reader(
    source: Union[str, TextIO], words_to_search: list[str], stopwords: list[str]
) -> Generator[str, None, None]:
    """Читает строки из файла или файлового объекта и фильтрует их."""
    if isinstance(source, str):
        with open(source, "r", encoding="utf-8") as file_obj:
            for line in file_obj:
                print(f"reading file line: {line}")
                filtered_line = filter_line(line, words_to_search, stopwords)
                if filtered_line:
                    yield filtered_line
    else:
        for line in source:
            filtered_line = filter_line(line, words_to_search, stopwords)
            if filtered_line:
                yield filtered_line

from typing import Generator, Optional, TextIO
import string


def convert_to_lower_remove_punct(line: str) -> str:
    line = line.lower().strip()
    return line.translate(str.maketrans("", "", string.punctuation))


def filter_line(
    line: str, words_to_search: list[str], stopwords: list[str]
) -> Optional[str]:

    has_search_word = False
    lowercase_line = convert_to_lower_remove_punct(line)
    for word in lowercase_line.split():

        if word in stopwords:
            return None

        if word in words_to_search:
            has_search_word = True

    if has_search_word:
        return line.strip()

    return None


def file_reader(
    file_obj: TextIO, words_to_search: list[str], stopwords: list[str]
) -> Generator[str, None, None]:

    for line in file_obj:
        filtered_line = filter_line(line, words_to_search, stopwords)

        if filtered_line:
            yield filtered_line

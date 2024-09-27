import string
import json
from typing import Callable


def convert_to_lower_remove_punct(line: str) -> str:
    line = line.lower().strip()
    return line.translate(str.maketrans("", "", string.punctuation))


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid json string") from exc

    if required_keys is None or len(required_keys) == 0:
        return

    if tokens is None or len(tokens) == 0:
        return

    lowercase_tokens = {token.lower().strip(): token.strip() for token in tokens}

    for key in required_keys:
        if key not in data:
            continue

        lowercase_line = convert_to_lower_remove_punct(data[key])
        for token in lowercase_line.split():
            if token.lower() in lowercase_tokens and callback:
                callback(key, lowercase_tokens[token])

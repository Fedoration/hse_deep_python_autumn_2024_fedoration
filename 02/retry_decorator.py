from functools import wraps


def retry_deco(max_retries=3, exceptions=None):
    if exceptions is None:
        exceptions = []

    def retry_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    print(
                        f"run '{func.__name__}' with args={args}, kwargs={kwargs}, "
                        f"attempt={attempt}, result={result}"
                    )
                    return result
                except tuple(exceptions) as e:
                    print(
                        f"run '{func.__name__}' with args={args}, kwargs={kwargs}, "
                        f"attempt={attempt}, exception={e.__class__.__name__}"
                    )
                    raise  # Перевыбрасываем исключение из списка разрешенных
                except Exception as e:
                    last_exception = e
                    print(
                        f"run '{func.__name__}' with args={args}, kwargs={kwargs}, "
                        f"attempt={attempt}, exception={e.__class__.__name__}"
                    )

            # После всех попыток перевыбрасываем последнее исключение
            if last_exception:
                raise last_exception

            return None

        return wrapper

    return retry_decorator

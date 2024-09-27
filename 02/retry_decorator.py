from functools import wraps


def retry_deco(max_retries=3, exceptions=None):
    if exceptions is None:
        exceptions = []

    def retry_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    print_str = f"run '{func.__name__}' with"
                    print_str += f"poositional args = {args}, " if args else ""
                    print_str += f"keywords kwargs = {kwargs}, " if kwargs else ""

                    result = func(*args, **kwargs)
                    print(print_str + f"attempt = {attempt + 1}, result = {result}")
                    return result

                except Exception as e:
                    print(
                        print_str
                        + f"attempt = {attempt + 1}, exception = {e.__class__.__name__}"
                    )
                    if isinstance(e, tuple(exceptions)):
                        break
                    continue

            return None

        return wrapper

    return retry_decorator

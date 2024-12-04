import cProfile
import pstats
import io
from functools import wraps


def profile_deco(func):
    stats = pstats.Stats()

    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        try:
            return func(*args, **kwargs)
        finally:
            profiler.disable()
            stream = io.StringIO()
            profiler_stats = pstats.Stats(profiler, stream=stream)
            stats.add(profiler_stats)

    def print_stat():
        print(f"Profiling statistics for function: {func.__name__}")
        stats.sort_stats("cumulative").print_stats()

    # Добавляем метод в обертку
    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


# Вызовы функций
add(1, 2)
add(4, 5)
sub(4, 5)

# Вывод статистики
add.print_stat()
sub.print_stat()

import cProfile
import pstats
import io

from memory_profiler import profile

from .classes import (
    RegularAttributes,
    SlotsAttributes,
    WeakrefAttributesProper,
    measure_creation_time,
    measure_access_time,
    measure_access_with_weakref,
    measure_creation_with_weakref,
)


# Профилирование вызовов
def profile_calls():
    num_objects = 1_000_000

    pr = cProfile.Profile()
    pr.enable()
    _, created_objects_regular = measure_creation_time(RegularAttributes, num_objects)
    measure_access_time(created_objects_regular)
    pr.disable()
    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print("Regular Attributes:")
    print(s.getvalue())

    pr = cProfile.Profile()
    pr.enable()
    _, created_objects_slots = measure_creation_time(SlotsAttributes, num_objects)
    measure_access_time(created_objects_slots)
    pr.disable()
    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print("Slots Attributes:")
    print(s.getvalue())

    pr = cProfile.Profile()
    pr.enable()
    _, created_objects_weakref = measure_creation_with_weakref(
        WeakrefAttributesProper, num_objects
    )
    measure_access_with_weakref(created_objects_weakref)
    pr.disable()
    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print("Weakref Attributes:")
    print(s.getvalue())


@profile
def memory_profiling_regular():
    num_objects = 1_000_000
    _, created_objects_regular = measure_creation_time(RegularAttributes, num_objects)
    measure_access_time(created_objects_regular)


@profile
def memory_profiling_slots():
    num_objects = 1_000_000
    _, created_objects_slots = measure_creation_time(SlotsAttributes, num_objects)
    measure_access_time(created_objects_slots)


@profile
def memory_profiling_weakref():
    num_objects = 1_000_000
    _, created_objects_weakref = measure_creation_with_weakref(
        WeakrefAttributesProper, num_objects
    )
    measure_access_with_weakref(created_objects_weakref)


def main():
    profile_calls()
    memory_profiling_regular()
    memory_profiling_slots()
    memory_profiling_weakref()


if __name__ == "__main__":
    main()

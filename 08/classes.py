import time
import weakref


class RegularAttributes:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class SlotsAttributes:
    __slots__ = ["a", "b", "c"]

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class WeakrefAttributesProper:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


def measure_creation_time(cls, count):
    start_time = time.time()
    objects = [cls(i, i * 2, i * 3) for i in range(count)]
    end_time = time.time()
    return end_time - start_time, objects


def measure_creation_with_weakref(cls, count):
    start_time = time.time()
    objects = [weakref.ref(cls(i, i * 2, i * 3)) for i in range(count)]
    end_time = time.time()
    return end_time - start_time, objects


def measure_access_time(objects):
    start_time = time.time()
    for obj in objects:
        obj.a += 1
        obj.b += 2
        obj.c += 3
        _ = obj.a + obj.b + obj.c
    end_time = time.time()
    return end_time - start_time


def measure_access_with_weakref(objects):
    start_time = time.time()
    for weak_obj in objects:
        obj = weak_obj()
        if obj is not None:
            obj.a += 1
            obj.b += 2
            obj.c += 3
            _ = obj.a + obj.b + obj.c
    end_time = time.time()
    return end_time - start_time

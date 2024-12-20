import time
import weakref


class AttrClass:
    def __init__(self, value):
        self.value = value


class RegularAttributes:
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = value

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = value


class SlotsAttributes:
    __slots__ = ["_a", "_b", "_c"]

    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = value

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = value


class WeakrefAttributes:
    def __init__(self, a, b, c):
        self._a = weakref.ref(a)
        self._b = weakref.ref(b)
        self._c = weakref.ref(c)

    @property
    def a(self):
        obj = self._a()
        if obj is None:
            raise ReferenceError("Referenced object 'a' no longer exists")
        return obj

    @a.setter
    def a(self, value):
        self._a = weakref.ref(value)

    @property
    def b(self):
        obj = self._b()
        if obj is None:
            raise ReferenceError("Referenced object 'b' no longer exists")
        return obj

    @b.setter
    def b(self, value):
        self._b = weakref.ref(value)

    @property
    def c(self):
        obj = self._c()
        if obj is None:
            raise ReferenceError("Referenced object 'c' no longer exists")
        return obj

    @c.setter
    def c(self, value):
        self._c = weakref.ref(value)


def measure_creation_time(cls, count):
    start_time = time.time()
    objects = [
        cls(AttrClass(i), AttrClass(i * 2), AttrClass(i * 3)) for i in range(count)
    ]
    end_time = time.time()
    return end_time - start_time, objects


def measure_access_time(objects):
    start_time = time.time()
    for obj in objects:
        obj.a = AttrClass(1)
        obj.b = AttrClass(2)
        obj.c = AttrClass(3)
        # _ = obj.a.value + obj.b.value + obj.c.value
    end_time = time.time()
    return end_time - start_time


if __name__ == "__main__":
    COUNT = 1_000_000

    print("Testing RegularAttributes...")
    time_regular, objects_regular = measure_creation_time(RegularAttributes, COUNT)
    print(f"Creation time: {time_regular:.2f}s")
    print(f"Access time: {measure_access_time(objects_regular):.2f}s")

    print("\nTesting SlotsAttributes...")
    time_slots, objects_slots = measure_creation_time(SlotsAttributes, COUNT)
    print(f"Creation time: {time_slots:.2f}s")
    print(f"Access time: {measure_access_time(objects_slots):.2f}s")

    print("\nTesting WeakrefAttributes...")
    time_weakref, objects_weakref = measure_creation_time(WeakrefAttributes, COUNT)
    print(f"Creation time: {time_weakref:.2f}s")
    print(f"Access time: {measure_access_time(objects_weakref):.2f}s")

# import time
# import weakref


# class RegularAttributes:
#     def __init__(self, a, b, c):
#         self.a = a
#         self.b = b
#         self.c = c


# class SlotsAttributes:
#     __slots__ = ["a", "b", "c"]

#     def __init__(self, a, b, c):
#         self.a = a
#         self.b = b
#         self.c = c


# class WeakrefAttributesProper:
#     def __init__(self, a, b, c):
#         self.a = a
#         self.b = b
#         self.c = c


# def measure_creation_time(cls, count):
#     start_time = time.time()
#     objects = [cls(i, i * 2, i * 3) for i in range(count)]
#     end_time = time.time()
#     return end_time - start_time, objects


# def measure_creation_with_weakref(cls, count):
#     start_time = time.time()
#     objects = [weakref.ref(cls(i, i * 2, i * 3)) for i in range(count)]
#     end_time = time.time()
#     return end_time - start_time, objects


# def measure_access_time(objects):
#     start_time = time.time()
#     for obj in objects:
#         obj.a += 1
#         obj.b += 2
#         obj.c += 3
#         _ = obj.a + obj.b + obj.c
#     end_time = time.time()
#     return end_time - start_time


# def measure_access_with_weakref(objects):
#     start_time = time.time()
#     for weak_obj in objects:
#         obj = weak_obj()
#         if obj is not None:
#             obj.a += 1
#             obj.b += 2
#             obj.c += 3
#             _ = obj.a + obj.b + obj.c
#     end_time = time.time()
#     return end_time - start_time

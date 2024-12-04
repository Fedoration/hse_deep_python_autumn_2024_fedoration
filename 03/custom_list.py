from __future__ import annotations


class CustomList(list):

    def __add__(self, other):
        if isinstance(other, int):
            return CustomList([x + other for x in self])

        if isinstance(other, list):
            size = max(len(self), len(other))
            result = [0] * size

            for i in range(size):
                if i < len(self):
                    result[i] += self[i]
                if i < len(other):
                    result[i] += other[i]
            return CustomList(result)

        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            return CustomList([x - other for x in self])

        if isinstance(other, list):
            size = max(len(self), len(other))
            result = [0] * size

            for i in range(size):
                if i < len(self):
                    result[i] += self[i]
                if i < len(other):
                    result[i] -= other[i]
            return CustomList(result)

        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, int):
            return CustomList([other - x for x in self])

        if isinstance(other, list):
            size = max(len(self), len(other))
            result = [0] * size

            for i in range(size):
                if i < len(self):
                    result[i] -= self[i]
                if i < len(other):
                    result[i] += other[i]
            return CustomList(result)

        return NotImplemented

    def __eq__(self, other: CustomList) -> bool:
        if isinstance(other, CustomList):
            return sum(self) == sum(other)
        return False

    def __ne__(self, other: CustomList) -> bool:
        if isinstance(other, CustomList):
            return not self.__eq__(other)
        return False

    def __gt__(self, other: CustomList) -> bool:
        if isinstance(other, CustomList):
            return sum(self) > sum(other)
        return False

    def __lt__(self, other: CustomList) -> bool:
        if isinstance(other, CustomList):
            return sum(self) < sum(other)
        return False

    def __ge__(self, other: CustomList) -> bool:
        if isinstance(other, CustomList):
            return sum(self) >= sum(other)
        return False

    def __le__(self, other: CustomList) -> bool:
        if isinstance(other, CustomList):
            return sum(self) <= sum(other)
        return False

    def __str__(self):
        return f"CustomList elements: {list(self)} with sum: {sum(self)}"

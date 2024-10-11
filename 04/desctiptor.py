class BaseDescriptor:
    """Базовый класс для дескрипторов."""

    def __init__(self):
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.name] = value

    def validate(self, value):
        raise NotImplementedError("Метод validate должен быть реализован в подклассе.")


class Integer(BaseDescriptor):
    """Дескриптор для целых чисел."""

    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"{self.name} должен быть целым числом.")


class String(BaseDescriptor):
    """Дескриптор для строк."""

    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"{self.name} должен быть строкой.")


class PositiveInteger(Integer):
    """Дескриптор для положительных целых чисел."""

    def validate(self, value):
        super().validate(value)
        if value <= 0:
            raise ValueError(f"{self.name} должен быть положительным целым числом.")


class PaperData:
    idx = Integer()
    title = String()
    num_citations = PositiveInteger()

    def __init__(self, idx, title, num_citations):
        self.idx = idx
        self.title = title
        self.num_citations = num_citations

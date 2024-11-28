class CustomMeta(type):
    def __new__(mcs, name, bases, dct):
        new_dct = {}
        for key, value in dct.items():
            # Если это не магический метод, добавляем префикс "custom_"
            if not (key.startswith("__") and key.endswith("__")):
                new_dct[f"custom_{key}"] = value
            else:
                new_dct[key] = value
        cls = super().__new__(mcs, name, bases, new_dct)

        orig_setattr = cls.__setattr__

        def custom_setattr(self, name, value):
            if not (name.startswith("__") and name.endswith("__")):
                self.__dict__[f"custom_{name}"] = value
            else:
                orig_setattr(self, name, value)

        cls.__setattr__ = custom_setattr
        return cls

    def __call__(cls, *args, **kwargs):
        # Создаем экземпляр класса
        instance = super().__call__(*args, **kwargs)
        return instance

    def __setattr__(cls, name, value):
        # Динамическая обработка атрибутов класса
        if not (name.startswith("__") and name.endswith("__")):
            super().__setattr__(f"custom_{name}", value)
        else:
            super().__setattr__(name, value)


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"

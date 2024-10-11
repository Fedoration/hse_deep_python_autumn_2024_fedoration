import pytest

from custom_class import CustomClass


def test_class_attributes():
    """Проверка аттрибутов класса с префиксами"""
    assert hasattr(CustomClass, "custom_x")
    assert CustomClass.custom_x == 50
    with pytest.raises(AttributeError):
        _ = CustomClass.x


def test_instance_attributes():
    """Проверка аттрибутов экземпляра с префиксами"""
    inst = CustomClass()

    assert hasattr(inst, "custom_x")
    assert inst.custom_x == 50
    assert hasattr(inst, "custom_val")
    assert inst.custom_val == 99

    assert hasattr(inst, "custom_line")
    assert inst.custom_line() == 100

    assert str(inst) == "Custom_by_metaclass"

    with pytest.raises(AttributeError):
        _ = inst.x

    with pytest.raises(AttributeError):
        _ = inst.val

    with pytest.raises(AttributeError):
        _ = inst.line()


def test_dynamic_attributes():
    """Добавление динамических аттрибутов"""
    inst = CustomClass()

    inst.dynamic = "added later"
    assert hasattr(inst, "custom_dynamic")
    assert inst.custom_dynamic == "added later"

    with pytest.raises(AttributeError):
        _ = inst.dynamic

import pytest
from desctiptor import PaperData


def test_valid_data():
    """Тесты для корректных значений"""
    data = PaperData(1, "Научное исследование", 150)
    assert data.idx == 1
    assert data.title == "Научное исследование"
    assert data.num_citations == 150


def test_invalid_idx_type():
    """Тесты для некорректных типов"""
    with pytest.raises(ValueError, match="idx должен быть целым числом."):
        PaperData("один", "Научное исследование", 150)


def test_invalid_title_type():
    """Тесты для некорректных типов"""
    with pytest.raises(ValueError, match="title должен быть строкой."):
        PaperData(1, 12345, 150)


def test_invalid_num_citations_type():
    """Тесты для некорректных типов"""
    with pytest.raises(ValueError, match="num_citations должен быть целым числом."):
        PaperData(1, "Научное исследование", "сто пятьдесят")


def test_negative_num_citations():
    """Тесты для некорректных значений (отрицательные числа)"""
    with pytest.raises(
        ValueError, match="num_citations должен быть положительным целым числом."
    ):
        PaperData(1, "Научное исследование", -150)


def test_update_valid_num_citations():
    """Тесты для изменения значения"""
    data = PaperData(1, "Научное исследование", 150)
    data.num_citations = 200
    assert data.num_citations == 200


def test_update_invalid_num_citations():
    data = PaperData(1, "Научное исследование", 150)
    with pytest.raises(
        ValueError, match="num_citations должен быть положительным целым числом."
    ):
        data.num_citations = -10


def test_independent_instances():
    """Проверка независимости экземпляров"""
    data1 = PaperData(1, "Исследование 1", 150)
    data2 = PaperData(2, "Исследование 2", 200)

    assert data1.idx == 1
    assert data2.idx == 2

    data1.idx = 10
    assert data1.idx == 10
    assert data2.idx == 2  # Значение другого экземпляра не меняется


def test_update_valid_values():
    """Проверка установки валидных значений"""
    data = PaperData(1, "Исследование", 100)
    data.idx = 42
    data.title = "Новое исследование"
    data.num_citations = 300

    assert data.idx == 42
    assert data.title == "Новое исследование"
    assert data.num_citations == 300


def test_update_invalid_values():
    """Проверка установки невалидных значений"""
    data = PaperData(1, "Исследование", 100)

    with pytest.raises(ValueError, match="idx должен быть целым числом."):
        data.idx = "invalid"

    with pytest.raises(
        ValueError, match="num_citations должен быть положительным целым числом."
    ):
        data.num_citations = -50

    assert data.idx == 1  # Значение не изменилось
    assert data.num_citations == 100  # Значение не изменилось


def test_invalid_set_does_not_change_value():
    """Проверка, что невалидное значение не меняет текущее значение"""
    data = PaperData(1, "Исследование", 150)

    with pytest.raises(ValueError, match="idx должен быть целым числом."):
        data.idx = "не число"

    with pytest.raises(
        ValueError, match="num_citations должен быть положительным целым числом."
    ):
        data.num_citations = -100

    assert data.idx == 1  # Остается прежним
    assert data.num_citations == 150  # Остается прежним

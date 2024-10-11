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

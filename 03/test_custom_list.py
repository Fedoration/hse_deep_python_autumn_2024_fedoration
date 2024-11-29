import unittest
from custom_list import CustomList


def assert_equal_lists(list1, list2):
    """Проверка равенства списков"""
    if len(list1) != len(list2):
        return False
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return False
    return True


class TestCustomList(unittest.TestCase):

    def test_sum(self):
        """Тест на сумму элементов списка"""
        custom_list = CustomList([1, 2, 3, 4])
        self.assertEqual(sum(custom_list), 10)

        custom_list = CustomList([])
        self.assertEqual(sum(custom_list), 0)

    def test_add_with_int(self):
        """Тест на сложение числа с списком"""
        custom_list = CustomList([1, 2, 3])
        original = custom_list[:]

        result = custom_list + 2

        assert_equal_lists(result, CustomList([3, 4, 5]))
        assert_equal_lists(custom_list, original)  # Проверка неизменности

    def test_add_with_list(self):
        """Тест на сложение списка с списком"""
        custom_list = CustomList([1, 2, 3])
        other_list = [4, 5, 6]
        original_custom = custom_list[:]
        original_other = other_list[:]

        result = custom_list + other_list

        assert_equal_lists(result, CustomList([5, 7, 9]))
        assert_equal_lists(custom_list, original_custom)  # Проверка неизменности
        assert_equal_lists(other_list, original_other)  # Проверка неизменности

    def test_radd(self):
        """Тест на сложение числа с списком"""
        custom_list = CustomList([1, 2, 3])
        original = custom_list[:]

        result = 2 + custom_list

        assert_equal_lists(result, CustomList([3, 4, 5]))
        assert_equal_lists(custom_list, original)  # Проверка неизменности

        custom_list = CustomList([])
        original = custom_list[:]

        result = 2 + custom_list

        assert_equal_lists(result, CustomList([]))
        assert_equal_lists(custom_list, original)  # Проверка неизменности

    def test_sub_with_int(self):
        """Тест на вычитание из списка числа"""
        custom_list = CustomList([5, 6, 7])
        original = custom_list[:]

        result = custom_list - 2

        assert_equal_lists(result, CustomList([3, 4, 5]))
        assert_equal_lists(custom_list, original)  # Проверка неизменности

        custom_list = CustomList([])
        original = custom_list[:]

        result = custom_list - 2

        assert_equal_lists(result, CustomList([]))
        assert_equal_lists(custom_list, original)  # Проверка неизменности

    def test_sub_with_list(self):
        """Тест на вычитание из списка списка"""
        custom_list = CustomList([10, 8, 6])
        original = custom_list[:]
        result = custom_list - [5, 3, 1]
        assert_equal_lists(result, CustomList([5, 5, 5]))
        assert_equal_lists(custom_list, original)  # Проверка неизменности

        custom_list = CustomList([])
        original = custom_list[:]
        result = custom_list - [5, 3, 1]
        assert_equal_lists(result, CustomList([-5, -3, -1]))
        assert_equal_lists(custom_list, original)  # Проверка неизменности

    def test_rsub_with_int(self):
        """Тест на вычитание из числа списка"""
        custom_list = CustomList([1, 2, 3])
        original = custom_list[:]
        result = 5 - custom_list
        assert_equal_lists(result, CustomList([4, 3, 2]))
        assert_equal_lists(custom_list, original)  # Проверка неизменности

        custom_list = CustomList([])
        original = custom_list[:]
        result = 5 - custom_list
        assert_equal_lists(result, CustomList([]))
        assert_equal_lists(custom_list, original)  # Проверка неизменности

    def test_eq(self):
        """Тест на равенство"""
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([1, 2, 3])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        assert_equal_lists(custom_list1, custom_list2)
        assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert_equal_lists(custom_list2, original2)  # Проверка неизменности

        custom_list1 = CustomList([])
        custom_list2 = CustomList([])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        assert_equal_lists(custom_list1, custom_list2)
        assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert_equal_lists(custom_list2, original2)  # Проверка неизменности

    def test_ne(self):
        """Тест на неравенство"""
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([1, 2, 4])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        assert not assert_equal_lists(custom_list1, custom_list2)
        assert assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert assert_equal_lists(custom_list2, original2)  # Проверка неизменности

        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        assert not assert_equal_lists(custom_list1, custom_list2)
        assert assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert assert_equal_lists(custom_list2, original2)  # Проверка неизменности

    def test_gt(self):
        """Тест на больше"""
        custom_list1 = CustomList([3, 2, 5])
        custom_list2 = CustomList([1, 2, 3])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        self.assertTrue(custom_list1 > custom_list2)
        assert assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert assert_equal_lists(custom_list2, original2)  # Проверка неизменности

        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        self.assertTrue(custom_list1 > custom_list2)
        assert assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert assert_equal_lists(custom_list2, original2)  # Проверка неизменности

    def test_lt(self):
        """Тест на меньше"""
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([5, 5, 5])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        self.assertTrue(custom_list1 < custom_list2)
        assert assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert assert_equal_lists(custom_list2, original2)  # Проверка неизменности

        custom_list1 = CustomList([])
        custom_list2 = CustomList([5, 5, 5])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        self.assertTrue(custom_list1 < custom_list2)
        assert assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert assert_equal_lists(custom_list2, original2)  # Проверка неизменности

    def test_ge(self):
        """Тест больше или равно"""
        custom_list1 = CustomList([3, 2, 5])
        custom_list2 = CustomList([3, 2, 5])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        self.assertTrue(custom_list1 >= custom_list2)
        assert assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert assert_equal_lists(custom_list2, original2)  # Проверка неизменности

        custom_list1 = CustomList([3, 2, 5])
        custom_list2 = CustomList([])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        self.assertTrue(custom_list1 >= custom_list2)
        assert assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert assert_equal_lists(custom_list2, original2)  # Проверка неизменности

    def test_le(self):
        """Тест меньше или равно"""
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([5, 5, 5])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        self.assertTrue(custom_list1 <= custom_list2)
        assert assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert assert_equal_lists(custom_list2, original2)  # Проверка неизменности

        custom_list1 = CustomList([])
        custom_list2 = CustomList([5, 5, 5])
        original1 = custom_list1[:]
        original2 = custom_list2[:]
        self.assertTrue(custom_list1 <= custom_list2)
        assert assert_equal_lists(custom_list1, original1)  # Проверка неизменности
        assert assert_equal_lists(custom_list2, original2)  # Проверка неизменности

    def test_str(self):
        """Тест на вывод списка"""
        custom_list = CustomList([1, 2, 3])
        original = custom_list[:]
        self.assertEqual(str(custom_list), "CustomList elements: [1, 2, 3] with sum: 6")
        assert assert_equal_lists(custom_list, original)  # Проверка неизменности

        custom_list = CustomList([])
        original = custom_list[:]
        self.assertEqual(str(custom_list), "CustomList elements: [] with sum: 0")
        assert assert_equal_lists(custom_list, original)  # Проверка неизменности

    def test_add_different_sizes(self):
        """Тест на сложение списков разного размера"""
        custom_list = CustomList([1, 2])
        origiginal = custom_list[:]
        other_list = [3, 4, 5]
        result = custom_list + other_list
        assert assert_equal_lists(result, CustomList([4, 6, 5]))
        assert assert_equal_lists(custom_list, origiginal)  # Проверка неизменности

        custom_list = CustomList([1, 2])
        origiginal = custom_list[:]
        other_list = [3, 4, 5]
        result = other_list + custom_list
        assert assert_equal_lists(result, CustomList([4, 6, 5]))
        assert assert_equal_lists(custom_list, origiginal)  # Проверка неизменности

        custom_list = CustomList([1, 2, 3])
        origiginal = custom_list[:]
        other_list = [4]
        result = custom_list + other_list
        assert assert_equal_lists(result, CustomList([5, 2, 3]))
        assert assert_equal_lists(custom_list, origiginal)  # Проверка неизменности

        custom_list = CustomList([1, 2, 3])
        origiginal = custom_list[:]
        other_list = [4]
        result = other_list + custom_list
        assert assert_equal_lists(result, CustomList([5, 2, 3]))
        assert assert_equal_lists(custom_list, origiginal)  # Проверка неизменности

    def test_sub_different_sizes(self):
        """Тест на вычитание списков разного размера"""
        custom_list = CustomList([10, 8])
        original = custom_list[:]
        other_list = [5, 3, 1]
        result = custom_list - other_list
        assert assert_equal_lists(result, CustomList([5, 5, -1]))
        assert assert_equal_lists(custom_list, original)  # Проверка неизменности

        custom_list = CustomList([10, 8])
        original = custom_list[:]
        other_list = [5, 3, 1]
        result = other_list - custom_list
        assert assert_equal_lists(result, CustomList([-5, -5, 1]))
        assert assert_equal_lists(custom_list, original)  # Проверка неизменности

        custom_list = CustomList([10, 8, 6])
        original = custom_list[:]
        other_list = [5]
        result = custom_list - other_list
        assert assert_equal_lists(result, CustomList([5, 8, 6]))
        assert assert_equal_lists(custom_list, original)  # Проверка неизменности

        custom_list = CustomList([10, 8, 6])
        original = custom_list[:]
        other_list = [5]
        result = other_list - custom_list
        assert assert_equal_lists(result, CustomList([-5, -8, -6]))
        assert assert_equal_lists(custom_list, original)  # Проверка неизменности


if __name__ == "__main__":
    unittest.main()

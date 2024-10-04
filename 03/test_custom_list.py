import unittest
from custom_list import CustomList


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
        result = custom_list + 2
        self.assertEqual(result, CustomList([3, 4, 5]))

        custom_list = CustomList([])
        result = custom_list + 2
        self.assertEqual(result, CustomList([]))

    def test_add_with_list(self):
        """Тест на сложение списка с списком"""
        custom_list = CustomList([1, 2, 3])
        result = custom_list + [4, 5, 6]
        self.assertEqual(result, CustomList([5, 7, 9]))

        custom_list = CustomList([])
        result = custom_list + [4, 5, 6]
        self.assertEqual(result, CustomList([4, 5, 6]))

    def test_radd(self):
        """Тест на сложение числа с списком"""
        custom_list = CustomList([1, 2, 3])
        result = 2 + custom_list
        self.assertEqual(result, CustomList([3, 4, 5]))

        custom_list = CustomList([])
        result = 2 + custom_list
        self.assertEqual(result, CustomList([]))

    def test_sub_with_int(self):
        """Тест на вычитание из списка числа"""
        custom_list = CustomList([5, 6, 7])
        result = custom_list - 2
        self.assertEqual(result, CustomList([3, 4, 5]))

        custom_list = CustomList([])
        result = custom_list - 2
        self.assertEqual(result, CustomList([]))

    def test_sub_with_list(self):
        """Тест на вычитание из списка списка"""
        custom_list = CustomList([10, 8, 6])
        result = custom_list - [5, 3, 1]
        self.assertEqual(result, CustomList([5, 5, 5]))

        custom_list = CustomList([])
        result = custom_list - [5, 3, 1]
        self.assertEqual(result, CustomList([-5, -3, -1]))

    def test_rsub_with_int(self):
        """Тест на вычитание из числа списка"""
        custom_list = CustomList([1, 2, 3])
        result = 5 - custom_list
        self.assertEqual(result, CustomList([4, 3, 2]))

        custom_list = CustomList([])
        result = 5 - custom_list
        self.assertEqual(result, CustomList([]))

    def test_eq(self):
        """Тест на равенство"""
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([2, 1, 3])
        self.assertEqual(custom_list1, custom_list2)

        custom_list1 = CustomList([])
        custom_list2 = CustomList([])
        self.assertEqual(custom_list1, custom_list2)

    def test_ne(self):
        """Тест на неравенство"""
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([1, 2, 4])
        self.assertNotEqual(custom_list1, custom_list2)

        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([])
        self.assertNotEqual(custom_list1, custom_list2)

    def test_gt(self):
        """Тест на больше"""
        custom_list1 = CustomList([3, 2, 5])
        custom_list2 = CustomList([1, 2, 3])
        self.assertTrue(custom_list1 > custom_list2)

        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([])
        self.assertTrue(custom_list1 > custom_list2)

    def test_lt(self):
        """Тест на меньше"""
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([5, 5, 5])
        self.assertTrue(custom_list1 < custom_list2)

        custom_list1 = CustomList([])
        custom_list2 = CustomList([5, 5, 5])
        self.assertTrue(custom_list1 < custom_list2)

    def test_ge(self):
        """Тест больше или равно"""
        custom_list1 = CustomList([3, 2, 5])
        custom_list2 = CustomList([3, 2, 5])
        self.assertTrue(custom_list1 >= custom_list2)

        custom_list1 = CustomList([3, 2, 5])
        custom_list2 = CustomList([])
        self.assertTrue(custom_list1 >= custom_list2)

    def test_le(self):
        """Тест меньше или равно"""
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([5, 5, 5])
        self.assertTrue(custom_list1 <= custom_list2)

        custom_list1 = CustomList([])
        custom_list2 = CustomList([5, 5, 5])
        self.assertTrue(custom_list1 <= custom_list2)

    def test_str(self):
        """Тест на вывод списка"""
        custom_list = CustomList([1, 2, 3])
        self.assertEqual(str(custom_list), "CustomList elements: [1, 2, 3] with sum: 6")

        custom_list = CustomList([])
        self.assertEqual(str(custom_list), "CustomList elements: [] with sum: 0")


if __name__ == "__main__":
    unittest.main()

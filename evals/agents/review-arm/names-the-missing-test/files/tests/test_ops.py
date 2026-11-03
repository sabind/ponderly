import unittest

from calc.ops import add, divide, multiply


class OpsTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)

    def test_divide_by_zero_raises_its_message(self):
        with self.assertRaises(ZeroDivisionError) as caught:
            divide(1, 0)
        self.assertEqual(str(caught.exception), "divide: the divisor b is zero")

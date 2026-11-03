import unittest

from calc.average import mean


class MeanTest(unittest.TestCase):
    def test_mean_of_empty_is_zero(self):
        self.assertEqual(mean([]), 0.0)

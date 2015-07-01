from fractions import Fraction
import unittest
from math import trunc, floor, ceil

from fixedpoint import FixedPoint, QFormat


class TestNumerator(unittest.TestCase):

    def test_numerator_for_zero(self):
        f = FixedPoint(0)
        self.assertEqual(f.numerator, 0)

    def test_numerator_for_positive_integer(self):
        f = FixedPoint(10)
        self.assertEqual(f.numerator, 10)

    def test_numerator_for_negative_integer(self):
        f = FixedPoint(-10)
        self.assertEqual(f.numerator, -10)

    def test_numerator_for_fractional(self):
        f = FixedPoint(0.625) # 5/8
        self.assertEqual(f.numerator, 5)

    def test_numerator_for_improper_fraction(self):
        f = FixedPoint(1.625)  # 1 5/8
        self.assertEqual(f.numerator, 13)


class TestDenominator(unittest.TestCase):

    def test_denominator_for_zero(self):
        f = FixedPoint(0)
        self.assertEqual(f.denominator, 1)

    def test_denominator_for_positive_integer(self):
        f = FixedPoint(10)
        self.assertEqual(f.denominator, 1)

    def test_denominator_for_negative_integer(self):
        f = FixedPoint(-10)
        self.assertEqual(f.denominator, 1)

    def test_denominator_for_fractional(self):
        f = FixedPoint(0.625)  # 5/8
        self.assertEqual(f.denominator, 8)

    def test_denominator_for_improper_fractional(self):
        f = FixedPoint(1.625)  # 1 5/8
        self.assertEqual(f.denominator, 8)


class TestEquality(unittest.TestCase):

    def test_equal_fixed_point_expecting_true(self):
        a = FixedPoint(37.875)
        b = FixedPoint(37.875)
        self.assertTrue(a == b)

    def test_equal_fixed_point_expecting_false(self):
        a = FixedPoint(37.875)
        b = FixedPoint(42)
        self.assertFalse(a == b)

    def test_equal_float_expecting_true(self):
        a = FixedPoint(37.875)
        b = 37.875
        self.assertTrue(a == b)

    def test_equal_float_expecting_false(self):
        a = FixedPoint(37.875)
        b = 42
        self.assertFalse(a == b)

    def test_equal_int_expecting_true(self):
        a = FixedPoint(42)
        b = 42
        self.assertTrue(a == b)

    def test_equal_int_expecting_false(self):
        a = FixedPoint(42)
        b = 37
        self.assertFalse(a == b)

    def test_equal_complex_expecting_true(self):
        a = FixedPoint(37.5)
        b = complex(37.5)
        self.assertTrue(a == b)

    def test_equal_complex_expecting_false(self):
        a = FixedPoint(37.5)
        b = complex(13.6)
        self.assertFalse(a == b)

    def test_equal_fraction_expecting_true(self):
        a = FixedPoint(0.1875)
        b = Fraction(3, 16)
        self.assertTrue(a == b)

    def test_equal_fraction_expecting_false(self):
        a = FixedPoint(0.1875)
        b = Fraction(5, 16)
        self.assertFalse(a == b)


class TestInequality(unittest.TestCase):

    def test_unequal_fixed_point_expecting_false(self):
        a = FixedPoint(37.875)
        b = FixedPoint(37.875)
        self.assertFalse(a != b)

    def test_unequal_fixed_point_expecting_true(self):
        a = FixedPoint(37.875)
        b = FixedPoint(42)
        self.assertTrue(a != b)

    def test_unequal_float_expecting_false(self):
        a = FixedPoint(37.875)
        b = 37.875
        self.assertFalse(a != b)

    def test_unequal_float_expecting_true(self):
        a = FixedPoint(37.875)
        b = 42
        self.assertTrue(a != b)

    def test_unequal_int_expecting_false(self):
        a = FixedPoint(42)
        b = 42
        self.assertFalse(a != b)

    def test_unequal_int_expecting_true(self):
        a = FixedPoint(42)
        b = 37
        self.assertTrue(a != b)

    def test_unequal_complex_expecting_false(self):
        a = FixedPoint(37.5)
        b = complex(37.5)
        self.assertFalse(a != b)

    def test_unequal_complex_expecting_true(self):
        a = FixedPoint(37.5)
        b = complex(13.6)
        self.assertTrue(a != b)

    def test_unequal_fraction_expecting_false(self):
        a = FixedPoint(0.1875)
        b = Fraction(3, 16)
        self.assertFalse(a != b)

    def test_unequal_fraction_expecting_true(self):
        a = FixedPoint(0.1875)
        b = Fraction(5, 16)
        self.assertTrue(a != b)


class TestFixedPointLessThan(unittest.TestCase):

    def test_less_than_fixed_point_expecting_false(self):
        a = FixedPoint(37.875)
        b = FixedPoint(37.875)
        self.assertFalse(a < b)

    def test_less_than_fixed_point_expecting_true(self):
        a = FixedPoint(37.875)
        b = FixedPoint(42)
        self.assertTrue(a < b)

    def test_less_than_float_expecting_false(self):
        a = FixedPoint(37.875)
        b = 37.875
        self.assertFalse(a < b)

    def test_less_than_float_expecting_true(self):
        a = FixedPoint(37.875)
        b = 42
        self.assertTrue(a < b)

    def test_less_than_int_expecting_false(self):
        a = FixedPoint(42)
        b = 42
        self.assertFalse(a < b)

    def test_less_than_int_expecting_true(self):
        a = FixedPoint(37)
        b = 42
        self.assertTrue(a < b)

    def test_less_than_fraction_expecting_false(self):
        a = FixedPoint(0.1875)
        b = Fraction(3, 16)
        self.assertFalse(a < b)

    def test_less_than_fraction_expecting_true(self):
        a = FixedPoint(0.1874)
        b = Fraction(3, 16)
        self.assertTrue(a < b)


class TestFixedPointLessThanOrEqualTo(unittest.TestCase):

    def test_less_than_or_equal_to_fixed_point_expecting_false_because_greater_than(self):
        a = FixedPoint(38.125)
        b = FixedPoint(37.875)
        self.assertFalse(a <= b)

    def test_less_than_or_equal_to_fixed_point_expecting_true_because_equal(self):
        a = FixedPoint(37.875)
        b = FixedPoint(37.875)
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_fixed_point_expecting_true_because_less_than(self):
        a = FixedPoint(35.125)
        b = FixedPoint(37.875)
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_float_expecting_false_because_greater_than(self):
        a = FixedPoint(38.125)
        b = 37.875
        self.assertFalse(a <= b)

    def test_less_than_or_equal_to_float_expecting_true_because_equal(self):
        a = FixedPoint(37.875)
        b = 37.875
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_float_expecting_true_because_less_than(self):
        a = FixedPoint(35.125)
        b = 37.875
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_int_expecting_false_because_greater_than(self):
        a = FixedPoint(43)
        b = 42
        self.assertFalse(a <= b)

    def test_less_than_or_equal_to_int_expecting_true_because_equal(self):
        a = FixedPoint(37)
        b = 37
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_int_expecting_true_because_less_than(self):
        a = FixedPoint(36)
        b = 37
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_fraction_expecting_false_because_greater_than(self):
        a = FixedPoint(0.5)
        b = Fraction(3, 16)
        self.assertFalse(a <= b)

    def test_less_than_or_equal_to_fraction_expecting_true_because_equal(self):
        a = FixedPoint(0.1875)
        b = Fraction(3, 16)
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_fraction_expecting_true_because_less_than(self):
        a = FixedPoint(0.1)
        b = Fraction(3, 16)
        self.assertTrue(a <= b)


class TestFixedPointGreaterThan(unittest.TestCase):

    def test_greater_than_fixed_point_expecting_false(self):
        a = FixedPoint(37.875)
        b = FixedPoint(37.875)
        self.assertFalse(a > b)

    def test_greater_than_fixed_point_expecting_true(self):
        a = FixedPoint(42)
        b = FixedPoint(37.875)
        self.assertTrue(a > b)

    def test_greater_than_float_expecting_false(self):
        a = FixedPoint(37.875)
        b = 37.875
        self.assertFalse(a > b)

    def test_greater_than_float_expecting_true(self):
        a = FixedPoint(42)
        b = 37.875
        self.assertTrue(a > b)

    def test_greater_than_int_expecting_false(self):
        a = FixedPoint(42)
        b = 42
        self.assertFalse(a > b)

    def test_greater_than_int_expecting_true(self):
        a = FixedPoint(42)
        b = 37
        self.assertTrue(a > b)

    def test_greater_than_fraction_expecting_false(self):
        a = FixedPoint(0.1875)
        b = Fraction(3, 16)
        self.assertFalse(a > b)

    def test_greater_than_fraction_expecting_true(self):
        a = FixedPoint(0.1876)
        b = Fraction(3, 16)
        self.assertTrue(a > b)


class TestFixedPointGreaterThanOrEqualTo(unittest.TestCase):

    def test_greater_than_or_equal_to_fixed_point_expecting_false_because_less_than(self):
        a = FixedPoint(37.875)
        b = FixedPoint(38.125)
        self.assertFalse(a >= b)

    def test_greater_than_or_equal_to_fixed_point_expecting_true_because_equal(self):
        a = FixedPoint(37.875)
        b = FixedPoint(37.875)
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_fixed_point_expecting_true_because_greater_than(self):
        a = FixedPoint(37.875)
        b = FixedPoint(35.125)
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_float_expecting_false_because_less_than(self):
        a = FixedPoint(37.875)
        b = 38.125
        self.assertFalse(a >= b)

    def test_greater_than_or_equal_to_float_expecting_true_because_equal(self):
        a = FixedPoint(37.875)
        b = 37.875
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_float_expecting_true_because_greater_than(self):
        a = FixedPoint(37.875)
        b = 35.125
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_int_expecting_false_because_less_than(self):
        a = FixedPoint(43)
        b = 44
        self.assertFalse(a >= b)

    def test_greater_than_or_equal_to_int_expecting_true_because_equal(self):
        a = FixedPoint(37)
        b = 37
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_int_expecting_true_because_greater_than(self):
        a = FixedPoint(37)
        b = 36
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_fraction_expecting_false_because_less_than(self):
        a = FixedPoint(0.125)
        b = Fraction(3, 16)
        self.assertFalse(a >= b)

    def test_greater_than_or_equal_to_fraction_expecting_true_because_equal(self):
        a = FixedPoint(0.1875)
        b = Fraction(3, 16)
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_fraction_expecting_true_because_greater_than(self):
        a = FixedPoint(0.25)
        b = Fraction(3, 16)
        self.assertTrue(a >= b)


class TestLessThanFixedPoint(unittest.TestCase):

    def test_less_than_float_expecting_false(self):
        a = 37.875
        b = FixedPoint(37.875)
        self.assertFalse(a < b)

    def test_less_than_float_expecting_true(self):
        a = 37.875
        b = FixedPoint(42)
        self.assertTrue(a < b)

    def test_less_than_int_expecting_false(self):
        a = 42
        b = FixedPoint(42)
        self.assertFalse(a < b)

    def test_less_than_int_expecting_true(self):
        a = 37
        b = FixedPoint(42)
        self.assertTrue(a < b)

    def test_less_than_fraction_expecting_false(self):
        a = Fraction(3, 16)
        b = FixedPoint(0.1875)
        self.assertFalse(a < b)

    def test_less_than_fraction_expecting_true(self):
        a = Fraction(3, 16)
        b = FixedPoint(0.1876)
        self.assertTrue(a < b)


class TestLessThanOrEqualToFixedPoint(unittest.TestCase):

    def test_less_than_or_equal_to_float_expecting_false_because_greater_than(self):
        a = 38.125
        b = FixedPoint(37.875)
        self.assertFalse(a <= b)

    def test_less_than_or_equal_to_float_expecting_true_because_equal(self):
        a = 37.875
        b = FixedPoint(37.875)
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_float_expecting_true_because_less_than(self):
        a = 35.125
        b = FixedPoint(37.875)
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_int_expecting_false_because_greater_than(self):
        a = 43
        b = FixedPoint(42)
        self.assertFalse(a <= b)

    def test_less_than_or_equal_to_int_expecting_true_because_equal(self):
        a = 37
        b = FixedPoint(37)
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_int_expecting_true_because_less_than(self):
        a = 36
        b = FixedPoint(37)
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_fraction_expecting_false_because_greater_than(self):
        a = Fraction(3, 16)
        b = FixedPoint(0.1)
        self.assertFalse(a <= b)

    def test_less_than_or_equal_to_fraction_expecting_true_because_equal(self):
        a = Fraction(3, 16)
        b = FixedPoint(0.1875)
        self.assertTrue(a <= b)

    def test_less_than_or_equal_to_fraction_expecting_true_because_less_than(self):
        a = Fraction(3, 16)
        b = FixedPoint(0.5)
        self.assertTrue(a <= b)


class TestGreaterThanFixedPoint(unittest.TestCase):

    def test_greater_than_float_expecting_false(self):
        a = 37.875
        b = FixedPoint(37.875)
        self.assertFalse(a > b)

    def test_greater_than_float_expecting_true(self):
        a = 42
        b = FixedPoint(37.875)
        self.assertTrue(a > b)

    def test_greater_than_int_expecting_false(self):
        a = 42
        b = FixedPoint(42)
        self.assertFalse(a > b)

    def test_greater_than_int_expecting_true(self):
        a = 42
        b = FixedPoint(37)
        self.assertTrue(a > b)

    def test_greater_than_fraction_expecting_false(self):
        a = Fraction(3, 16)
        b = FixedPoint(0.1875)
        self.assertFalse(a > b)

    def test_greater_than_fraction_expecting_true(self):
        a = Fraction(3, 16)
        b = FixedPoint(0.1874)
        self.assertTrue(a > b)


class TestGreaterThanOrEqualToFixedPoint(unittest.TestCase):

    def test_greater_than_or_equal_to_float_expecting_false_because_less_than(self):
        a = 37.875
        b = FixedPoint(38.125)
        self.assertFalse(a >= b)

    def test_greater_than_or_equal_to_float_expecting_true_because_equal(self):
        a = 37.875
        b = FixedPoint(37.875)
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_float_expecting_true_because_greater_than(self):
        a = 37.875
        b = FixedPoint(35.125)
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_int_expecting_false_because_less_than(self):
        a = 43
        b = FixedPoint(44)
        self.assertFalse(a >= b)

    def test_greater_than_or_equal_to_int_expecting_true_because_equal(self):
        a = 37
        b = FixedPoint(37)
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_int_expecting_true_because_greater_than(self):
        a = 37
        b = FixedPoint(36)
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_fraction_expecting_false_because_less_than(self):
        a = Fraction(3, 16)
        b = FixedPoint(0.25)
        self.assertFalse(a >= b)

    def test_greater_than_or_equal_to_fraction_expecting_true_because_equal(self):
        a = Fraction(3, 16)
        b = FixedPoint(0.1875)
        self.assertTrue(a >= b)

    def test_greater_than_or_equal_to_fraction_expecting_true_because_greater_than(self):
        a = Fraction(3, 16)
        b = FixedPoint(0.1)
        self.assertTrue(a >= b)


class TestAddedToFixedPoint(unittest.TestCase):

    def test_add_fixed_point_to_fixed_point(self):
        a = FixedPoint(18.875)
        b = FixedPoint(18.875)
        c = a + b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(37.75))

    def test_add_fixed_point_to_int(self):
        a = FixedPoint(10.5)
        b = 5
        c = a + b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(15.5))

    def test_add_fixed_point_to_fraction(self):
        a = FixedPoint(10.5)
        b = Fraction(11, 4)
        c = a + b
        self.assertIsInstance(c, Fraction)
        self.assertEqual(c, Fraction(53, 4))

    def test_add_fixed_point_to_float(self):
        a = FixedPoint(10.5)
        b = 6.125
        c = a + b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 16.625)

    def test_add_fixed_point_to_complex(self):
        a = FixedPoint(10.5)
        b = (6.125+1j)
        c = a + b
        self.assertIsInstance(c, complex)
        self.assertEqual(c, 16.625+1j)


class TestFixedPointAddedTo(unittest.TestCase):

    def test_add_fixed_point_to_int(self):
        a = 5
        b = FixedPoint(10.5)
        c = a + b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(15.5))

    def test_add_fixed_point_to_fraction(self):
        a = Fraction(11, 4)
        b = FixedPoint(10.5)
        c = a + b
        self.assertIsInstance(c, Fraction)
        self.assertEqual(c, Fraction(53, 4))

    def test_add_fixed_point_to_float(self):
        a = 6.125
        b = FixedPoint(10.5)
        c = a + b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 16.625)

    def test_add_fixed_point_to_complex(self):
        a = (6.125+1j)
        b = FixedPoint(10.5)
        c = a + b
        self.assertIsInstance(c, complex)
        self.assertEqual(c, 16.625+1j)


class TestSubtractedFromFixedPoint(unittest.TestCase):

    def test_subtract_fixed_point_from_fixed_point(self):
        a = FixedPoint(18.875)
        b = FixedPoint(10.875)
        c = a - b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(8))

    def test_subtract_fixed_point_from_int(self):
        a = FixedPoint(10.5)
        b = 5
        c = a - b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(5.5))

    def test_subtract_fixed_point_from_fraction(self):
        a = FixedPoint(10.5)
        b = Fraction(5, 4)
        c = a - b
        self.assertIsInstance(c, Fraction)
        self.assertEqual(c, Fraction(37, 4))

    def test_subtract_fixed_point_from_float(self):
        a = FixedPoint(10.5)
        b = 6.125
        c = a - b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 4.375)

    def test_subtract_fixed_point_from_complex(self):
        a = FixedPoint(10.5)
        b = (6.125+1j)
        c = a - b
        self.assertIsInstance(c, complex)
        self.assertEqual(c, 4.375-1j)


class TestFixedPointSubtractedFrom(unittest.TestCase):

    def test_subtract_fixed_point_from_int(self):
        a = 10
        b = FixedPoint(4.5)
        c = a - b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(5.5))

    def test_subtract_fixed_point_from_fraction(self):
        a = Fraction(11, 4)
        b = FixedPoint(1.5)
        c = a - b
        self.assertIsInstance(c, Fraction)
        self.assertEqual(c, Fraction(5, 4))

    def test_subtract_fixed_point_from_float(self):
        a = 6.125
        b = FixedPoint(2.5)
        c = a - b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 3.625)

    def test_subtract_fixed_point_from_complex(self):
        a = (6.125+1j)
        b = FixedPoint(3)
        c = a - b
        self.assertIsInstance(c, complex)
        self.assertEqual(c, 3.125+1j)

class TestFixedPointNegation(unittest.TestCase):

    def test_negate_positive(self):
        a = FixedPoint(3.5)
        b = -a
        self.assertIsInstance(b, FixedPoint)
        self.assertEqual(b, FixedPoint(-3.5))

    def test_negate_negative(self):
        a = FixedPoint(-3.5)
        b = -a
        self.assertIsInstance(b, FixedPoint)
        self.assertEqual(b, FixedPoint(3.5))

    def test_negate_zero(self):
        a = FixedPoint(0)
        b = -a
        self.assertIsInstance(b, FixedPoint)
        self.assertEqual(b, FixedPoint(0))

class TestFixedPointPos(unittest.TestCase):

    def test_pos_positive(self):
        a = FixedPoint(3.5)
        b = +a
        self.assertIsInstance(b, FixedPoint)
        self.assertEqual(b, FixedPoint(3.5))

    def test_pos_negative(self):
        a = FixedPoint(-3.5)
        b = +a
        self.assertIsInstance(b, FixedPoint)
        self.assertEqual(b, FixedPoint(-3.5))

    def test_negate_zero(self):
        a = FixedPoint(0)
        b = +a
        self.assertIsInstance(b, FixedPoint)
        self.assertEqual(b, FixedPoint(0))


class TestFixedPointAbs(unittest.TestCase):

    def test_pos_positive(self):
        a = FixedPoint(3.5)
        b = abs(a)
        self.assertIsInstance(b, FixedPoint)
        self.assertEqual(b, FixedPoint(3.5))

    def test_pos_negative(self):
        a = FixedPoint(-3.5)
        b = abs(a)
        self.assertIsInstance(b, FixedPoint)
        self.assertEqual(b, FixedPoint(3.5))

    def test_negate_zero(self):
        a = FixedPoint(0)
        b = abs(a)
        self.assertIsInstance(b, FixedPoint)
        self.assertEqual(b, FixedPoint(0))


class TestFixedPointMultipliedBy(unittest.TestCase):

    def test_multiply_fixed_point_fixed_point_integers(self):
        a = FixedPoint(3, QFormat(5, 3))
        b = FixedPoint(5, QFormat(6, 2))
        c = a * b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(15))

    def test_multiply_fixed_point_fixed_point_fractional(self):
        a = FixedPoint(3.125, QFormat(8, 8))
        b = FixedPoint(12.1875, QFormat(8, 8))
        c = a * b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(38.0859375))

    def test_multiply_fixed_point_float(self):
        a = FixedPoint(3.125, QFormat(8, 8))
        b = 12.1875
        c = a * b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 38.0859375)

    def test_multiply_fixed_point_int(self):
        a = FixedPoint(12.1875, QFormat(8, 8))
        b = 7
        c = a * b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(85.3125))

    def test_multiply_fixed_point_fraction(self):
        a = FixedPoint(12.1875, QFormat(8, 8))
        b = Fraction(1, 3)
        c = a * b
        self.assertIsInstance(c, Fraction)
        self.assertEqual(c, Fraction(65, 16))

    def test_multiply_fixed_point_complex(self):
        a = FixedPoint(14.625, QFormat(5, 11))
        b = 3-2j
        c = a * b
        self.assertIsInstance(c, complex)
        self.assertEqual(c, 43.875-29.25j)


class TestMultipliedByFixedPoint(unittest.TestCase):

    def test_multiply_float_fixed_point(self):
        a = 12.1875
        b = FixedPoint(3.125, QFormat(8, 8))
        c = a * b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 38.0859375)

    def test_multiply_int_fixed_point(self):
        a = 7
        b = FixedPoint(12.1875, QFormat(8, 8))
        c = a * b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(85.3125))

    def test_multiply_fraction_fixed_point(self):
        a = Fraction(1, 3)
        b = FixedPoint(12.1875, QFormat(8, 8))
        c = a * b
        self.assertIsInstance(c, Fraction)
        self.assertEqual(c, Fraction(65, 16))

    def test_multiply_complex_fixed_point(self):
        a = 3-2j
        b = FixedPoint(14.625, QFormat(5, 11))
        c = a * b
        self.assertIsInstance(c, complex)
        self.assertEqual(c, 43.875-29.25j)

class TestFixedPointDividedBy(unittest.TestCase):

    def test_divide_fixed_point_fixed_point_integers(self):
        a = FixedPoint(12)
        b = FixedPoint(3)
        c = a / b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(4))

    def test_divide_fixed_point_fixed_point_fractional(self):
        a = FixedPoint(8.25)
        b = FixedPoint(1.5)
        c = a / b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(5.5))

    def test_divide_fixed_point_float(self):
        a = FixedPoint(8.25)
        b = 1.5
        c = a / b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 5.5)

    def test_divide_fixed_point_int(self):
        a = FixedPoint(14)
        b = 4
        c = a / b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(3.5))

    def test_divide_fixed_point_int_infinite_precision(self):
        a = FixedPoint(10, QFormat(8, 8))
        b = 3
        c = a / b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(3.33349609375))

    def test_divide_fixed_point_fraction(self):
        a = FixedPoint(12.1875)
        b = Fraction(1, 16)
        c = a / b
        self.assertIsInstance(c, Fraction)
        self.assertEqual(c, Fraction(195, 1))

    def test_divide_fixed_point_complex(self):
        a = FixedPoint(14.625, QFormat(5, 11))
        b = 3-1j
        c = a / b
        self.assertIsInstance(c, complex)
        self.assertEqual(c, (4.3875+1.4625j))


class TestDividedByFixedPoint(unittest.TestCase):

    def test_divide_float_fixed_point(self):
        a = 8.25
        b = FixedPoint(1.5)
        c = a / b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 5.5)

    def test_divide_int_fixed_point(self):
        a = 12
        b = FixedPoint(4, QFormat(8, 8))
        c = a / b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(3))

    def test_divide_int_fixed_point_infinite_precision(self):
        a = 10
        b = FixedPoint(3, QFormat(8, 8))
        c = a / b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(3.33203125))

    def test_divide_fraction_fixed_point(self):
        a = Fraction(195/16)
        b = FixedPoint(0.0625)
        c = a / b
        self.assertIsInstance(c, Fraction)
        self.assertEqual(c, Fraction(195, 1))

    def test_divide_complex_fixed_point(self):
        a = 12+6j
        b = FixedPoint(3, QFormat(5, 11))
        c = a / b
        self.assertIsInstance(c, complex)
        self.assertEqual(c, (4+2j))

    def test_reciprocal(self):
        a = FixedPoint(1)
        b = FixedPoint(16)
        c = a / b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(0.0625))


class TestTruncation(unittest.TestCase):

    def test_trunc_positive_fractional(self):
        a = FixedPoint(2.6)
        b = trunc(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, 2)

    def test_trunc_positive_integral(self):
        a = FixedPoint(3)
        b = trunc(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, 3)

    def test_trunc_zero(self):
        a = FixedPoint(0)
        b = trunc(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, 0)

    def test_trunc_negative_integral(self):
        a = FixedPoint(-3)
        b = trunc(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, -3)

    def test_trunc_negative_fractional(self):
        a = FixedPoint(-2.6)
        b = trunc(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, -2)


class TestFloor(unittest.TestCase):

    def test_floor_integer(self):
        a = FixedPoint(496)
        b = floor(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, 496)

    def test_floor_positive_fraction_nearest_lower(self):
        a = FixedPoint(496.2)
        b = floor(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, 496)

    def test_floor_positive_fraction_nearest_upper(self):
        a = FixedPoint(496.6)
        b = floor(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, 496)

    def test_floor_negative_fraction_nearest_lower(self):
        a = FixedPoint(-496.6)
        b = floor(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, -497)

    def test_floor_negative_fraction_nearest_upper(self):
        a = FixedPoint(-496.2)
        b = floor(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, -497)

class TestCeil(unittest.TestCase):

    def test_ceil_integer(self):
        a = FixedPoint(496)
        b = ceil(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, 496)

    def test_floor_positive_fraction_nearest_lower(self):
        a = FixedPoint(496.2)
        b = ceil(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, 497)

    def test_ceil_positive_fraction_nearest_upper(self):
        a = FixedPoint(496.6)
        b = ceil(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, 497)

    def test_ceil_negative_fraction_nearest_lower(self):
        a = FixedPoint(-496.6)
        b = ceil(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, -496)

    def test_floor_negative_fraction_nearest_upper(self):
        a = FixedPoint(-496.2)
        b = ceil(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, -496)


class TestRound(unittest.TestCase):

    def test_round_integer(self):
        a = FixedPoint(42)
        b = round(a)
        self.assertEqual(b, 42)

    def test_round_integer_negative_ndigits_round_down(self):
        a = FixedPoint(42)
        b = round(a, -1)
        self.assertEqual(b, 40)

    def test_round_integer_negative_ndigit_round_up(self):
        a = FixedPoint(47)
        b = round(a, -1)
        self.assertEqual(b, 50)

    def test_round_fractional(self):
        a = FixedPoint(31.16)
        b = round(a, 1)
        self.assertEqual(b, 31.1875)

    def test_round_half_up(self):
        a = FixedPoint(1.5)
        b = round(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, 2)

    def test_round_half_down(self):
        a = FixedPoint(2.5)
        b = round(a)
        self.assertIsInstance(b, int)
        self.assertEqual(b, 2)

class TestFixedPointFloorDividedBy(unittest.TestCase):

    def test_divide_fixed_point_fixed_point_integers(self):
        a = FixedPoint(12)
        b = FixedPoint(3)
        c = a // b
        self.assertIsInstance(c, int)
        self.assertEqual(c, 4)

    def test_divide_fixed_point_fixed_point_fractional(self):
        a = FixedPoint(8.25)
        b = FixedPoint(1.5)
        c = a // b
        self.assertIsInstance(c, int)
        self.assertEqual(c, 5)

    def test_divide_fixed_point_float(self):
        a = FixedPoint(8.25)
        b = 1.5
        c = a // b
        self.assertIsInstance(c, int)
        self.assertEqual(c, 5)

    def test_divide_fixed_point_int(self):
        a = FixedPoint(14)
        b = 4
        c = a // b
        self.assertIsInstance(c, int)
        self.assertEqual(c, 3)

    def test_divide_fixed_point_int_infinite_precision(self):
        a = FixedPoint(10, QFormat(8, 8))
        b = 3
        c = a // b
        self.assertIsInstance(c, int)
        self.assertEqual(c, 3)

    def test_divide_fixed_point_fraction(self):
        a = FixedPoint(12.1875)
        b = Fraction(1, 16)
        c = a // b
        self.assertIsInstance(c, int)
        self.assertEqual(c, 195)

    def test_divide_fixed_point_complex(self):
        a = FixedPoint(14.625, QFormat(5, 11))
        b = 3-1j
        with self.assertRaises(TypeError):
            c = a // b


class TestFloorDividedByFixedPoint(unittest.TestCase):

    def test_divide_float_fixed_point(self):
        a = 8.25
        b = FixedPoint(1.5)
        c = a // b
        self.assertIsInstance(c, int)
        self.assertEqual(c, 5)

    def test_divide_int_fixed_point(self):
        a = 12
        b = FixedPoint(5, QFormat(8, 8))
        c = a // b
        self.assertIsInstance(c, int)
        self.assertEqual(c, 2)

    def test_divide_int_fixed_point_infinite_precision(self):
        a = 10
        b = FixedPoint(3, QFormat(8, 8))
        c = a // b
        self.assertIsInstance(c, int)
        self.assertEqual(c, 3)

    def test_divide_fraction_fixed_point(self):
        a = Fraction(195/16)
        b = FixedPoint(0.125)
        c = a // b
        self.assertIsInstance(c, int)
        self.assertEqual(c, 97)

    def test_divide_complex_fixed_point(self):
        a = 12+6j
        b = FixedPoint(3, QFormat(5, 11))
        with self.assertRaises(TypeError):
            c = a // b

    def test_reciprocal(self):
        a = FixedPoint(1)
        b = FixedPoint(16)
        c = a // b
        self.assertIsInstance(c, int)
        self.assertEqual(c, 0)

class TestFixedPointModBy(unittest.TestCase):

    def test_mod_fixed_point_fixed_point_integers(self):
        a = FixedPoint(12)
        b = FixedPoint(5)
        c = a % b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, 2)

    def test_mod_fixed_point_fixed_point_fractional(self):
        a = FixedPoint(8.25)
        b = FixedPoint(1.5)
        c = a % b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(0.75))

    def test_mod_fixed_point_float(self):
        a = FixedPoint(8.25)
        b = 1.5
        c = a % b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 0.75)

    def test_mod_fixed_point_int(self):
        a = FixedPoint(14.5)
        b = 3
        c = a % b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(2.5))

    def test_mod_fixed_point_fraction(self):
        a = FixedPoint(12.1875)
        b = Fraction(1, 2)
        c = a % b
        self.assertIsInstance(c, Fraction)
        self.assertEqual(c, Fraction(3, 16))

    def test_mod_fixed_point_complex(self):
        a = FixedPoint(14.625, QFormat(5, 11))
        b = 3-1j
        with self.assertRaises(TypeError):
            c = a % b


class TestModByFixedPoint(unittest.TestCase):

    def test_mod_float_fixed_point(self):
        a = 8.25
        b = FixedPoint(1.5)
        c = a % b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 0.75)

    def test_mod_int_fixed_point(self):
        a = 12
        b = FixedPoint(5, QFormat(8, 8))
        c = a % b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(2))

    def test_mod_fraction_fixed_point(self):
        a = Fraction(13/5)
        b = FixedPoint(0.0625)
        c = a % b
        self.assertIsInstance(c, Fraction)
        self.assertEqual(c, Fraction(84442493013197, 2251799813685248))

    def test_mod_complex_fixed_point(self):
        a = 12+6j
        b = FixedPoint(3, QFormat(5, 11))
        with self.assertRaises(TypeError):
            c = a % b


class TestFixedPointRaisedToPowerOf(unittest.TestCase):

    def test_pow_fixed_point_fixed_point_positive_integers(self):
        a = FixedPoint(5)
        b = FixedPoint(3)
        c = a ** b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(125))

    def test_pow_fixed_point_fixed_point_negative_integers(self):
        a = FixedPoint(4)
        b = FixedPoint(-2)
        c = a ** b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(0.0625))

    def test_pow_fixed_point_fixed_point_fractional(self):
        a = FixedPoint(2)
        b = FixedPoint(0.5)
        c = a ** b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 1.4142135623730951)

    def test_pow_fixed_point_float(self):
        a = FixedPoint(3.125)
        b = 12.1875
        c = a ** b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 1073951.4265564263)

    def test_pow_fixed_point_int(self):
        a = FixedPoint(12)
        b = 7
        c = a ** b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(35831808))

    def test_pow_fixed_point_fraction(self):
        a = FixedPoint(12.1875)
        b = Fraction(1, 3)
        c = a ** b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 2.301291020628972)

    def test_pow_fixed_point_complex(self):
        a = FixedPoint(2.5, QFormat(5, 11))
        b = 3-2j
        c = a ** b
        self.assertIsInstance(c, complex)
        self.assertEqual(c, (-4.043832497129643-15.092648665332344j))


class TestRaisedToPowerOfFixedPoint(unittest.TestCase):

    def test_pow_float_fixed_point(self):
        a = 2.5
        b = FixedPoint(3)
        c = a ** b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 15.625)

    def test_pow_int_fixed_point_integer(self):
        a = 7
        b = FixedPoint(3)
        c = a ** b
        self.assertIsInstance(c, FixedPoint)
        self.assertEqual(c, FixedPoint(343))

    def test_pow_int_fixed_point_fractional(self):
        a = 7
        b = FixedPoint(3.5)
        c = a ** b
        self.assertIsInstance(c, float)
        self.assertEqual(c, 907.4926996951546)

    def test_pow_fraction_fixed_point(self):
        a = Fraction(1, 3)
        b = FixedPoint(2)
        c = a ** b
        self.assertIsInstance(c, Fraction)
        self.assertEqual(c, Fraction(1, 9))

    def test_pow_complex_fixed_point(self):
        a = 3-2j
        b = FixedPoint(2)
        c = a ** b
        self.assertIsInstance(c, complex)
        self.assertEqual(c, (5-12j))


if __name__ == '__main__':
    unittest.main()


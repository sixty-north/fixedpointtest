import operator

from fractions import Fraction, gcd
from functools import lru_cache
from numbers import Real, Integral, Rational, Complex
from math import trunc, frexp, log10, log2, isnan, isinf, floor
from itertools import count

from fixedpoint.qformat import QFormat


def lowest_set_bit(x):
    """The lowest set bit in a value.

    Args:
        x: An integer in which to find the lowest set bit.

    Returns:
        An integer which at most one set bit which will be
        the lowest set bit of x.
    """
    lowest_bit = (x & ~(x - 1))
    return lowest_bit


def signed_left_shift(x, shift):
    """An arithmetic shift operator which can shift left or right.

    Args:
        shift: The signed number of bits to shift. Negative values
        shift right. Positive values shift left.

    Returns:
        The x shifted left by shift places.
    """
    if shift < 0:
        return x << -shift
    if shift > 0:
        return x >> shift
    return x


def prime_factors(n):
    """The prime factors of n.

    Args:
        n: The positive integer for which to find prime factors.

    Returns:
        A list of the prime factors of n.
    """
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


@lru_cache()
def has_finite_expansion(denominator, base):
    """Can a fraction with denominator be expressed with a power-of-base denominator?

    Example:

        # Can 3/16 be represented as a fraction of the form 1/10**x
        # for some value of x?
        >>> has_finite_expansion(16, 10)
        True

    Args:
        denominator: The denominator of the source fraction we wish to represent.
        base: The base of the denominator of the target representation.

    Returns:
        True if a fraction with the source denominator can be represented as a
        fraction whose denominator is a power of base.
    """
    denominator_factors = set(prime_factors(denominator))
    base_factors = set(prime_factors(base))
    return len(denominator_factors - base_factors) == 0


def fraction_with_base(f, base):
    """Convert Fraction f into a fraction with a denominator that is a power-of-base.

    Example:

        # For example, how can 3/16 be represented as a fraction of the form 1/10**x
        # for some value of x?
        >>> fraction_with_base(Fraction(3, 16), 10)
        (1875, 10000)

    Args:
        f: A Fraction to be represented with a different denominator.
        base: The base of the denominator of the target representation.

    Returns:
        A 2-tuple containing the numerator and denominator of the result fraction. Note that
        a tuple is returned, rather than a Fraction, to prevent the result being simplified
        back to the argument f.

    Raises:
        ValueError: If f cannot be exactly represented as a fraction with a denominator which
            is a power of base.
    """
    if not has_finite_expansion(f.denominator, base):
        raise ValueError("Cannot convert {f} to a fraction with power-of-{base} denominator without"
                         "loss of precision".format(f=f, base=base))

    for power in count():
        decimal_denominator = base**power
        factor = Fraction(decimal_denominator, f.denominator)
        if factor.denominator == 1:
            return (f.numerator * factor.numerator,
                    f.denominator * factor.numerator)


def _make_operators(mono, poly):

    def op(self, other):
        if isinstance(other, FixedPoint):
            return mono(self, other)
        elif isinstance(other, int):
            return mono(self, FixedPoint(other))
        elif isinstance(other, Fraction):
            return poly(Fraction(self), other)
        elif isinstance(other, float):
            return poly(float(self), other)
        elif isinstance(other, complex):
            return poly(complex(self), other)
        return NotImplemented

    op.__name__ = '__{}__'.format(poly.__name__)
    op.__doc__ = mono.__doc__

    def rop(self, other):
        if isinstance(other, FixedPoint):
            return mono(other, self)
        if isinstance(other, Integral):
            return mono(FixedPoint(other), self)
        elif isinstance(other, Rational):
            return poly(Fraction(other), Fraction(self))
        elif isinstance(other, Real):
            return poly(float(other), float(self))
        elif isinstance(other, Complex):
            return poly(complex(other), complex(self))
        return NotImplemented

    rop.__name__ = '__r{}__'.format(poly.__name__)
    rop.__doc__ = mono.__doc__

    return op, rop


def _add(a, b):
    assert isinstance(a, FixedPoint)
    assert isinstance(b, FixedPoint)
    promoted_qformat = QFormat.from_qformats(a.qformat, b.qformat)
    result_qformat = QFormat(promoted_qformat.integer_bits + 1, promoted_qformat.fraction_bits)
    lhs_op = FixedPoint(a, result_qformat)
    rhs_op = FixedPoint(b, result_qformat)
    result_numerator = lhs_op._numerator + rhs_op._numerator
    return FixedPoint._from_numerator(result_numerator, result_qformat)


def _mul(a, b):
    assert isinstance(a, FixedPoint)
    assert isinstance(b, FixedPoint)
    result_qformat = QFormat(a.qformat.integer_bits + b.qformat.integer_bits + 1,
                             a.qformat.fraction_bits + b.qformat.fraction_bits)
    lhs_op = FixedPoint(a, result_qformat)
    rhs_op = FixedPoint(b, result_qformat)
    result_numerator = (lhs_op._numerator * rhs_op._numerator) // result_qformat.denominator
    return FixedPoint._from_numerator(result_numerator, result_qformat)


def _truediv(dividend, divisor):
    assert isinstance(dividend, FixedPoint)
    assert isinstance(divisor, FixedPoint)
    result_qformat = QFormat(dividend.qformat.integer_bits + divisor.qformat.fraction_bits + 1,
                             divisor.qformat.integer_bits + dividend.qformat.fraction_bits)

    working_qformat = QFormat.from_qformats(dividend.qformat, divisor.qformat, result_qformat)

    lhs_op = FixedPoint(dividend, working_qformat)
    rhs_op = FixedPoint(divisor, working_qformat)

    # We use Fraction's round() here rather than floor division to get correct rounding
    working_numerator = round(Fraction(lhs_op._numerator * working_qformat.denominator,  rhs_op._numerator))
    working_result = FixedPoint._from_numerator(working_numerator, working_qformat)
    return FixedPoint(working_result, result_qformat)


def _pow(base, exponent):
    assert isinstance(base, FixedPoint)
    assert isinstance(base, FixedPoint)
    if exponent.is_integer():
        integer_exponent = abs(floor(exponent))
        result_qformat = QFormat(max(base.qformat.integer_bits - 1, 0) * integer_exponent + 1,
                                 base.qformat.fraction_bits * integer_exponent)
        result_numerator = base._numerator ** integer_exponent
        positive_result = FixedPoint._from_numerator(result_numerator, result_qformat)
        if exponent >= 0:
            return positive_result
        else:
            reciprocal_result = 1 / positive_result
            return reciprocal_result
    return float(base) ** float(exponent)


class FixedPoint(Rational):
    """A signed, fixed-point, binary, immutable, number type."""

    @classmethod
    def _from_float(cls, f):
        """Create a FixedPoint using a QFormat without loss of precision.

        Args:
            f (float): A float of which to create an equivalent FixedPoint representation.

        Returns:
            A FixedPoint object the QFormat for which will have sufficient precision to
            exactly represent the float.

        Raises:
            OverflowError: If f is NaN or infinite.
        """
        assert isinstance(f, Real)
        if isnan(f) or isinf(f):
            raise OverflowError("{} cannot be represented by {}".format(f, cls.__name__))

        # 1. Work out where the binary point is
        fr, exp = frexp(f)
        numerator = int(fr * (2**53))  # 53 binary places in the fraction
        binary_point_index = 53 - exp  # Is one based

        # 2. Work out how many significant figures there are to the left of the binary point; call this m
        most_significant_set_index = numerator.bit_length() - 1
        num_leading_bits = 1 + most_significant_set_index - binary_point_index
        m = max(num_leading_bits, 0) + 1  # One to accommodate sign

        # 3. Work out how many significant figures there are to the right of the binary point; call this n
        lowest_bit = lowest_set_bit(numerator)
        least_significant_set_index = lowest_bit.bit_length() - 1
        num_trailing_bits = binary_point_index - least_significant_set_index
        n = max(num_trailing_bits, 0)

        # 4. Make QFormat(m, n)
        qformat = QFormat(m, n)

        # 5. Shift the numerator to fit Qm.n
        #    We want the binary point to be at index n
        shift = binary_point_index - n
        shifted_numerator = signed_left_shift(numerator, shift)

        return cls._from_numerator(shifted_numerator, qformat)

    @classmethod
    def _from_integer(cls, i):
        """Create a FixedPoint using a QFormat with sufficient precision to represent the integer.

        Args:
            i: The integer to be represented in FixedPoint.

        Returns:
            A FixedPoint representation with sufficient precision to represent i.
        """
        assert isinstance(i, int)
        num_bits = i.bit_length() + 1  # Additional bit for sign information
        qformat = QFormat(num_bits, 0)
        return cls._from_numerator(i, qformat)

    @classmethod
    def _from_rational_exact(cls, r):
        """Create a FixedPoint using a QFormat with sufficient precision to represent the integer.

        Args:
            r: A rational number to be represented exactly.

        Returns:
            An exact FixedPoint representation of r.

        Raises:
            ValueError: If r cannot be represented exactly.
        """
        assert isinstance(r, Rational)
        integer_part = trunc(r)
        fraction_part = abs(r - integer_part)
        binary_numerator, binary_denominator = fraction_with_base(fraction_part, base=2)
        qformat = QFormat(integer_part.bit_length() + 1,
                          int(log2(binary_denominator)))
        return cls._from_numerator(binary_numerator, qformat)

    @classmethod
    def _from_value_approximately(cls, value, qformat):
        """Create a possibly approximate representation of value with specified precision.

        Args:
            value: The value to be represented in fixed point.

            qformat: The precision of the result.
        """
        assert qformat is not None
        numerator = round(value * qformat.denominator)
        return cls._from_numerator(numerator, qformat)

    @classmethod
    def _from_number_with_arbitrary_precision(cls, value):
        """Represent a number in FixedPoint with sufficient precision.

        Args:
            value: The Number to be converted to a FixedPoint representation.

        Raises:
            TypeError: If value cannot be represented with finite precision.
        """
        if not isinstance(value, Real):
            raise TypeError("{} cannot represent non-real value {} of type {}"
                            .format(cls.__name__, value, type(value).__name__))
        # Exact type check. Subclasses handed by Rational case, below
        if type(value) == cls:
            return value
        if isinstance(value, int):
            return cls._from_integer(value)
        if isinstance(value, Rational):
            return cls._from_rational_exact(value)
        if isinstance(value, Real):
            return cls._from_float(value)
        raise TypeError("{} cannot represent value {}".format(cls.__name__, value))

    @classmethod
    def _from_fixed_point_with_specific_precision(cls, value, qformat):
        """Represent an existing FixedPoint number with different precision.

        Args:
            value: The FixedPoint number to be represented.

            qformat: The precision of the result.

        Raises:
            OverflowError: If value cannot be represented without overflow.
        """
        if qformat == value.qformat:
            return value
        numerator = qformat.rescale_numerator(value._numerator, value.qformat)
        return cls._from_numerator(numerator, qformat)

    @classmethod
    def _from_numerator(cls, numerator, qformat):
        """Allocate a new FixedPoint object.

        Args:
            numerator: The numerator value, which when divided by qformat.denominator gives
                the actual numeric value of the new object.

            qformat: The precision of the new object.

        Returns:
            A new FixedPoint instance.

        Raises:
            OverflowError: If numerator exceeds the precision of qformat.
        """
        n = qformat.check_numerator(numerator)
        obj = super().__new__(cls)
        obj._numerator = n
        obj._qformat = qformat
        return obj

    def __new__(cls, value, qformat=None):
        """Obtain a FixedPoint instance.

        Args:
            value (Real): A real number type. e.g. float, int, or an existing FixedPoint.

            qformat: An optional QFormat. If not supplied a QFormat with sufficient precision to
                represent value without loss of information will be used.  If supplied this will
                be the QFormat of the returned FixedPoint instance.

        Raises:
            ValueError: If value cannot be represented in finite precision when a qformat was not supplied.
            TypeError: If value cannot be represented as a FixedPoint value.
        """

        try:
            fixed_point = cls._from_number_with_arbitrary_precision(value)
        except ValueError:
            if qformat is None:
                raise
            fixed_point = cls._from_value_approximately(value, qformat)
        except OverflowError as e:
            raise ValueError(str(e))
        return fixed_point if (qformat is None) else cls._from_fixed_point_with_specific_precision(fixed_point, qformat)

    @property
    def qformat(self):
        """Obtain the Q format of the number as a 2-tuple.

        The zeroth element gives the signed integer precision in bits, the first element gives
        the fractional precision in bits.
        """
        return self._qformat

    def __repr__(self):
        return "{}({!s}, {!r})".format(self.__class__.__name__, self, self.qformat)

    def __str__(self):
        # All fractions with a finite binary representation (i.e. FixedPoint instances) also have a finite decimal
        # representation since all binary fractions have the form of k/2**a and all decimals have the form
        # k/(2**a * 5**b). The latter is a special case of the former.

        # To avoid loss of precision we construct the representation using integer math only, avoiding going via float.

        if self._numerator < 0:
            integer_part = -(abs(self._numerator) >> self._qformat.fraction_bits)
        else:
            integer_part = self._numerator >> self._qformat.fraction_bits

        integer_digits = str(integer_part)

        fractional_part = abs(self._numerator) & (2**self._qformat.fraction_bits - 1)
        if fractional_part == 0:
            return integer_digits

        fraction = Fraction(fractional_part, self._qformat.denominator)
        decimal_numerator, decimal_denominator = fraction_with_base(fraction, base=10)
        decimal_digits = str(decimal_numerator).zfill(int(log10(decimal_denominator)))
        return "{}.{}".format(integer_digits, decimal_digits)

    @property
    def numerator(self):
        """The numerator of an irreducible rational representation of the number.

        Note: This is NOT the same as the internal _numerator value, which may be in reducible form.
        """
        g = gcd(self._numerator, self._qformat.denominator)
        return self._numerator // g

    @property
    def denominator(self):
        """The denominator of an irreducible rational representation of the number.

        Note: This is NOT the same as the qformat.denominator, which may be in reducible form.
        """
        g = gcd(self._numerator, self._qformat.denominator)
        return self._qformat.denominator // g

    def __eq__(self, other):
        return Fraction(self) == other

    def __lt__(self, other):
        return Fraction(self) < other

    def __le__(self, other):
        return Fraction(self) <= other

    def __gt__(self, other):
        return Fraction(self) > other

    def __ge__(self, other):
        return Fraction(self) >= other

    __add__, __radd__ = _make_operators(_add, operator.add)
    __mul__, __rmul__ = _make_operators(_mul, operator.mul)
    __truediv__, __rtruediv__ = _make_operators(_truediv, operator.truediv)
    __pow__, __rpow__ = _make_operators(_pow, operator.pow)

    def __neg__(self):
        # This can overflow for the most negative value of the current QFormat - the positive value can't be
        # represented - so the result must have one additional bit of precision.
        result_qformat = QFormat(self._qformat.integer_bits + 1, self._qformat.fraction_bits)
        return FixedPoint._from_numerator(-self._numerator, result_qformat)

    def __pos__(self):
        return self

    def __abs__(self):
        return FixedPoint._from_numerator(abs(self._numerator), self._qformat)

    def __trunc__(self):
        if self._numerator < 0:
            return -(abs(self._numerator) >> self._qformat.fraction_bits)
        return self._numerator >> self._qformat.fraction_bits

    def __floor__(self):
        return self.numerator // self.denominator

    def __ceil__(self):
        return -(-self.numerator // self.denominator)

    def __round__(self, ndigits=None):
        """Round to nearest with optional decimal precision.

        Numbers exactly halfway between two nearest numbers are
        rounded towards the nearest ending with an even digit.

        Args:
            ndigits: An optional number of decimal places to which
                to round. Positive values round to fractional places
                (0.1, 0.01, etc) and negative values round to integer
                places(10, 100, etc). Zero rounds to whole numbers.

        Returns:
            If ndigits is None, the nearest integer, otherwise the
            nearest FixedPoint at the precision specified by ndigits.
        """

        if ndigits is None:
            quotient, remainder = divmod(self.numerator, self.denominator)
            if remainder * 2 < self.denominator:
                return quotient
            elif remainder * 2 > self.denominator:
                return quotient + 1
            else:
                return quotient if quotient % 2 == 0 else quotient + 1

        shift = 10**abs(ndigits)

        if ndigits > 0:
            shifted = self * shift
            rounded_to_integer = round(shifted)
            rounded_fixed_point = FixedPoint(rounded_to_integer)
            unshifted_fixed_point = rounded_fixed_point / shift
            return FixedPoint(unshifted_fixed_point, self._qformat)
        else:
            shifted = self / shift
            rounded_to_integer = round(shifted)
            rounded_fixed_point = FixedPoint(rounded_to_integer)
            unshifted_fixed_point = rounded_fixed_point * shift
            return FixedPoint(unshifted_fixed_point, self._qformat)

    def __floordiv__(self, other):
        return floor(self / other)

    def __rfloordiv__(self, other):
        return floor(other / self)

    def __mod__(self, other):
        div = self // other
        return self - other*div

    def __rmod__(self, other):
        div = other // self
        return other - self*div

    def is_integer(self):
        return floor(self) == self


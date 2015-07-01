from fractions import Fraction
from numbers import Integral
from weakref import WeakValueDictionary


class QFormat:
    """The precision and position of the binary point in a signed fixed point number.
    """

    _instances = WeakValueDictionary()

    @classmethod
    def from_str(cls, s):
        """Create a QFormat from a string of the format 'Qm.n' where m and n are integers.

        Args:
            s: A string of the form 'Qm.n' where m is an integer specifying the number of bits
                of precision in the integer part and n is the number of bits of precision in
                the fractional part.

        Returns:
            A QFormat.
        """
        if not s.startswith("Q"):
            raise ValueError("Q format {!r} does not conform to Qm.n".format(s))
        s_integer, _, s_fraction = s[1:].partition('.')

        try:
            integer_bits = int(s_integer)
            fraction_bits = int(s_fraction)
        except ValueError:
            raise ValueError("Q format {!r} does not conform to Qm.n".format(s))

        return cls(integer_bits, fraction_bits)

    @classmethod
    def from_qformats(cls, *qformats):
        """Create a QFormat with sufficient precision to represent values with the given QFormats.

        Args:
            *qformats: One or more QFormat objects.

        Returns:
            A QFormat.

        Raises:
            TypeError: If at least one QFormat is not supplied.
        """
        if len(qformats) < 1:
            raise TypeError("At least one QFormat must be supplied.")
        max_integer_bits = max(q.integer_bits for q in qformats)
        max_fraction_bits = max(q.fraction_bits for q in qformats)
        return cls(max_integer_bits, max_fraction_bits)

    def __new__(cls, integer_bits, fraction_bits):
        """Initialize a QFormat with specified integer and fractional precision."""
        precision = (integer_bits, fraction_bits)
        try:
            obj = cls._instances[precision]
        except KeyError:
            obj = super().__new__(cls)
            obj._integer_bits = integer_bits
            obj._fraction_bits = fraction_bits
            cls._instances[precision] = obj
        return obj

    @property
    def integer_bits(self):
        """The number of bits of integer precision."""
        return self._integer_bits

    @property
    def fraction_bits(self):
        """The number of bits of fractional precision."""
        return self._fraction_bits

    @property
    def denominator(self):
        """The divisor by which the numerator in a a fixed point value must be divided to give the number value."""
        return 2**self.fraction_bits

    def _max_signed_numerator(self):
        return 2 ** (self.integer_bits + self.fraction_bits - 1) - 1

    def _min_signed_numerator(self):
        return -(2 ** (self.integer_bits + self.fraction_bits - 1))

    def rescale_numerator(self, src_numerator, src_qformat):
        """Rescale a numerator to a different QFormat.

        Args:
            src_numerator: A numerator representing a value in a src_qformat.
            src_qformat: The QFormat in which src_numerator represents a value.

        Returns:
            An integer numerator representing in this QFormat the same value as represented
            by src_numerator and src_qformat.
        """
        # We use fraction here to implicitly perform the division, rather than true division which is limited by the
        # precision of floats), or floor division which doesn't round correctly.
        ratio = Fraction(self.denominator, src_qformat.denominator)
        numerator = round(src_numerator * ratio)
        return self.check_numerator(numerator)

    def check_numerator(self, numerator):
        """Check that a numerator is within the bound representable by this QFormat.

        Args:
            numerator: The integer numerator value to be checked.

        Returns:
            The checked numerator (i.e. the argument value)

        Raises:
            OverflowError: If numerator is out of bounds.
        """
        assert isinstance(numerator, Integral)
        lower = self._min_signed_numerator()
        upper = self._max_signed_numerator()
        if not lower <= numerator <= upper:
            raise OverflowError("Numerator {} is out of range {} <= numerator <= {} for {!r}"
                                .format(numerator, lower, upper, self))
        return numerator

    def __repr__(self):
        return "{}({!r}, {!r})".format(self.__class__.__name__, self._integer_bits, self._fraction_bits)

    def __str__(self):
        return "Q{}.{}".format(self._integer_bits, self._fraction_bits)
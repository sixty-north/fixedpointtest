==========
fixedpoint
==========

The ``fixedpoint`` package provides an arbitrary-precision fixed-point
binary number type to Python 3, supporting the full range of numeric
operations.

Usage
=====

To use ``fixedpoint`` import the ``FixedPoint`` and ``QFormat`` types::

  >>> from fixedpoint import FixedPoint, QFormat

Fixed point numbers can be created from existing numbers, with specific
precision. To represent 1 1/8 in fixed point with five bits of integer
precision and three bits of fractional precision::

  >>> f = FixedPoint(1.125, QFormat(5, 3))
  >>> f
  FixedPoint(1.125, QFormat(5, 3))

Alternatively, fixed-point instances can be created with automatic
precision sufficient to represent the supplied number::

  >>> g = FixedPoint(298.75)
  >>> g
  FixedPoint(298.75, QFormat(10, 2))

The ``FixedPoint`` type implements all operations required by the
``numbers.Rational`` abstract base class::

  >>> f + g
  FixedPoint(299.875, QFormat(11, 3))
  >>> f - g
  FixedPoint(-297.625, QFormat(12, 3))
  >>> f * g
  FixedPoint(336.09375, QFormat(16, 5))
  >>> f / g
  FixedPoint(0.0037841796875, QFormat(8, 13))
  >>> f // g
  0

and so on.
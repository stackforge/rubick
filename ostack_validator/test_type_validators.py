from ostack_validator.common import Error, MarkedError
from ostack_validator.schema import TypeValidatorRegistry

import unittest

class TypeValidatorTestHelper(object):
  def setUp(self):
    super(TypeValidatorTestHelper, self).setUp()
    self.validator = TypeValidatorRegistry.get_validator(self.type_name)

  def assertValid(self, value):
    self.assertIsNone(self.validator.validate(value))

  def assertInvalid(self, value):
    self.assertIsInstance(self.validator.validate(value), Error)

class StringTypeValidatorTests(TypeValidatorTestHelper, unittest.TestCase):
  type_name = 'string'

  def test_empty_string_passes(self):
    self.assertValid('')

  def test_validation_always_passes(self):
    self.assertValid('foo bar')

class BooleanTypeValidatorTests(TypeValidatorTestHelper, unittest.TestCase):
  type_name = 'boolean'

  def test_True(self):
    self.assertValid('True')

  def test_False(self):
    self.assertValid('False')

  def test_other_values_produce_error(self):
    self.assertInvalid('foo')

class IntegerTypeValidatorTests(TypeValidatorTestHelper, unittest.TestCase):
  type_name = 'integer'

  def test_positive_values_are_valid(self):
    self.assertValid('123')

  def test_zero_is_valid(self):
    self.assertValid('0')

  def test_negative_values_are_valid(self):
    self.assertValid('-123')

  def test_leading_whitespace_is_ignored(self):
    self.assertValid('   5')

  def test_trailing_whitespace_is_ignored(self):
    self.assertValid('7   ')

  def test_non_digits_are_invalid(self):
    self.assertInvalid('12a45')

  def test_invalid_char_error_contains_proper_column_in_mark(self):
    error = self.validator.validate('12a45')
    self.assertIsInstance(error, MarkedError)
    self.assertEqual(3, error.mark.column)

  def test_invalid_char_error_contains_proper_column_if_leading_whitespaces(self):
    error = self.validator.validate('  12a45')
    self.assertIsInstance(error, MarkedError)
    self.assertEqual(5, error.mark.column)

class PortTypeValidatorTests(TypeValidatorTestHelper, unittest.TestCase):
  type_name = 'port'

  def test_positive_integer(self):
    self.assertValid('123')

  def test_zero_invalid(self):
    self.assertInvalid('0')

  def test_negatives_are_invalid(self):
    self.assertInvalid('-1')

  def test_values_greater_than_65535_are_invalid(self):
    self.assertInvalid('65536')

  def test_low_boundary_is_valid(self):
    self.assertValid('1')

  def test_high_boundary_is_valid(self):
    self.assertValid('65535')

  def test_non_digits_are_invalid(self):
    self.assertInvalid('12a5')

  def test_leading_and_or_trailing_whitespace_is_ignored(self):
    self.assertValid('  123')
    self.assertValid('456  ')
    self.assertValid('  123  ')

if __name__ == '__main__':
  unittest.main()


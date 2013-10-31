from rubick.common import Issue, MarkedIssue
from rubick.schema import TypeValidatorRegistry

import unittest


class TypeValidatorTestHelper(object):
    def setUp(self):
        super(TypeValidatorTestHelper, self).setUp()
        self.validator = TypeValidatorRegistry.get_validator(self.type_name)

    def assertValid(self, value):
        self.assertNotIsInstance(self.validator.validate(value), Issue)

    def assertInvalid(self, value):
        self.assertIsInstance(
            self.validator.validate(value), Issue)


class StringTypeValidatorTests(TypeValidatorTestHelper, unittest.TestCase):
    type_name = 'string'

    def test_empty_string_passes(self):
        self.assertValid('')

    def test_validation_always_passes(self):
        self.assertValid('foo bar')

    def test_should_return_same_string_if_valid(self):
        s = 'foo bar'
        self.assertEqual(s, self.validator.validate(s))


class BooleanTypeValidatorTests(TypeValidatorTestHelper, unittest.TestCase):
    type_name = 'boolean'

    def test_True(self):
        v = self.validator.validate('True')
        self.assertEqual(True, v)

    def test_False(self):
        v = self.validator.validate('False')
        self.assertEqual(False, v)

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
        self.assertIsInstance(error, MarkedIssue)
        self.assertEqual(3, error.mark.column)

    def test_invalid_char_error_contains_proper_column_if_leading_whitespaces(
            self):
        error = self.validator.validate('  12a45')
        self.assertIsInstance(error, MarkedIssue)
        self.assertEqual(5, error.mark.column)

    def test_returns_integer_if_valid(self):
        v = self.validator.validate('123')
        self.assertEqual(123, v)


class HostAddressTypeValidatorTests(TypeValidatorTestHelper,
                                    unittest.TestCase):
    type_name = 'host_address'

    def test_ipv4_address(self):
        self.assertValid('127.0.0.1')

    def test_returns_address(self):
        s = '10.0.0.1'
        v = self.validator.validate(s)
        self.assertEqual(s, v)

    def test_value_with_less_than_4_numbers_separated_by_dots(self):
        self.assertInvalid('10.0.0')

    def test_ipv4_like_string_with_numbers_greater_than_255(self):
        self.assertInvalid('10.0.256.1')

    def test_host_name(self):
        self.assertValid('foo.bar.baz')

    def test_host_with_empty_parts(self):
        self.assertInvalid('.foo.bar')
        self.assertInvalid('foo..bar')
        self.assertInvalid('foo.bar.')

    def test_host_parts_with_invalid_chars(self):
        self.assertInvalid('foo.ba r.baz')
        self.assertInvalid('foo.x_y.bar')

    def test_host_with_single_host_label(self):
        self.assertValid('foo')

    def test_host_part_starting_with_non_letter(self):
        self.assertInvalid('123foo')

    def test_host_that_ends_with_a_hyphen(self):
        self.assertInvalid('foo-')

    def test_mark_should_point_to_incorrect_symbol(self):
        e = self.validator.validate('')
        self.assertEqual(0, e.mark.column)

        e = self.validator.validate('123foo')
        self.assertEqual(0, e.mark.column)

        e = self.validator.validate('foo-')
        self.assertEqual(3, e.mark.column)

        e = self.validator.validate('foo.bar.-baz')
        self.assertEqual(8, e.mark.column)


class NetworkAddressTypeValidatorTests(TypeValidatorTestHelper,
                                       unittest.TestCase):
    type_name = 'network_address'

    def test_ipv4_network(self):
        self.assertValid('127.0.0.1/24')

    def test_returns_address(self):
        s = '10.0.0.1/32'
        v = self.validator.validate(s)
        self.assertEqual(s, v)

    def test_value_with_less_than_4_numbers_separated_by_dots(self):
        self.assertInvalid('10.0.0/24')

    def test_ipv4_like_string_with_numbers_greater_than_255(self):
        self.assertInvalid('10.0.256.1/24')

    def test_no_prefix_length(self):
        self.assertInvalid('10.0.0.0')
        self.assertInvalid('10.0.0.0/')

    def test_non_integer_prefix_length(self):
        self.assertInvalid('10.0.0.0/1a')

    def test_prefix_greater_than_32(self):
        self.assertInvalid('10.0.0.0/33')


class PortTypeValidatorTests(TypeValidatorTestHelper, unittest.TestCase):
    type_name = 'port'

    def test_empty(self):
        self.assertInvalid('')

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

    def test_returns_integer_if_valid(self):
        v = self.validator.validate('123')
        self.assertEqual(123, v)


class HostAndPortTypeValidatorTests(TypeValidatorTestHelper,
                                    unittest.TestCase):
    type_name = 'host_and_port'

    def test_ipv4_address(self):
        self.assertValid('127.0.0.1:80')

    def test_returns_address(self):
        s = '10.0.0.1:80'
        v = self.validator.validate(s)
        self.assertEqual(('10.0.0.1', 80), v)

    def test_value_with_less_than_4_numbers_separated_by_dots(self):
        self.assertInvalid('10.0.0:1234')

    def test_ipv4_like_string_with_numbers_greater_than_255(self):
        self.assertInvalid('10.0.256.1:1234')

    def test_no_port(self):
        self.assertInvalid('10.0.0.1')
        self.assertInvalid('10.0.0.1:')

    def test_port_is_not_an_integer(self):
        self.assertInvalid('10.0.0.1:abc')

    def test_port_is_greater_than_65535(self):
        self.assertInvalid('10.0.0.1:65536')


class StringListTypeValidatorTests(TypeValidatorTestHelper, unittest.TestCase):
    type_name = 'string_list'

    def test_empty_value(self):
        v = self.validator.validate('')
        self.assertEqual([], v)

    def test_single_value(self):
        v = self.validator.validate(' foo bar ')

        self.assertIsInstance(v, list)
        self.assertEqual('foo bar', v[0])
        self.assertEqual(1, len(v))

    def test_list_of_values(self):
        v = self.validator.validate(' foo bar, baz ')

        self.assertIsInstance(v, list)
        self.assertEqual('foo bar', v[0])
        self.assertEqual('baz', v[1])
        self.assertEqual(2, len(v))


class StringDictTypeValidatorTests(TypeValidatorTestHelper, unittest.TestCase):
    type_name = 'string_dict'

    def test_empty_value(self):
        v = self.validator.validate('')
        self.assertEqual({}, v)

    def test_single_value(self):
        v = self.validator.validate(' foo: bar ')

        self.assertIsInstance(v, dict)
        self.assertEqual('bar', v['foo'])
        self.assertEqual(1, len(v))

    def test_list_of_values(self):
        v = self.validator.validate(' foo: bar, baz: 123 ')

        self.assertIsInstance(v, dict)
        self.assertEqual('bar', v['foo'])
        self.assertEqual('123', v['baz'])
        self.assertEqual(2, len(v))


class RabbitmqBindValidatorTest(TypeValidatorTestHelper, unittest.TestCase):
    type_name = 'rabbitmq_bind'

    def test_empty_value_is_an_error(self):
        self.assertInvalid('')

    def test_integer(self):
        v = self.validator.validate('123')

        self.assertEqual(('0.0.0.0', 123), v)

    def test_integer_outside_port_range(self):
        self.assertInvalid('65536')

    def test_host_port(self):
        v = self.validator.validate('{"127.0.0.1",8080}')

        self.assertEqual(('127.0.0.1', 8080), v)


class RabbitmqListValidatorTest(TypeValidatorTestHelper, unittest.TestCase):
    type_name = 'rabbitmq_bind_list'

    def test_empty(self):
        self.assertInvalid('')

    def test_empty_list(self):
        v = self.validator.validate('[]')

        self.assertEqual([], v)

    def test_single_entry(self):
        v = self.validator.validate('[123]')

        self.assertEqual([('0.0.0.0', 123)], v)

    def test_multiple_entries(self):
        v = self.validator.validate('[1080,{"localhost",8080}]')

        self.assertEqual([('0.0.0.0', 1080), ('localhost', 8080)], v)


if __name__ == '__main__':
    unittest.main()

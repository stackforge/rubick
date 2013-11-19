import unittest

from six import StringIO

from rubick.common import Mark
from rubick.config_formats.ini import IniConfigParser


class IniConfigParserTests(unittest.TestCase):

    def setUp(self):
        self.parser = IniConfigParser()

    def _strip_margin(self, content):
        lines = content.split("\n")
        if lines[0] == '' and lines[-1].strip() == '':
            lines = lines[1:-1]
        first_line = lines[0]
        margin_size = 0
        while margin_size < len(first_line) \
                and first_line[margin_size].isspace():
            margin_size += 1

        stripped_lines = [line[margin_size:] for line in lines]

        return "\n".join(stripped_lines)

    def parse(self, content, margin=False):
        if margin:
            content = self._strip_margin(content)

        return self.parser.parse('test.conf', Mark(''), content)

    def test_parsing(self):
        config = self.parse("param1 = value1")

        self.assertEqual(0, len(config.errors))

        self.assertParameter(
            'param1',
            'value1',
            config.sections[0].parameters[0])
        self.assertEqual(1, len(config.sections[0].parameters))

    def test_colon_as_delimiter(self):
        c = self.parse('param1 : value1')

        self.assertEqual(0, len(c.errors))
        self.assertParameter('param1', 'value1', c.sections[0].parameters[0])

    def test_use_colon_delimiter_if_it_comes_before_equals_sign(self):
        c = self.parse('param1: value=123')
        self.assertEqual(0, len(c.errors))
        self.assertParameter(
            'param1',
            'value=123',
            c.sections[0].parameters[0])

    def test_use_equals_delimiter_if_it_comes_before_colon(self):
        c = self.parse('param1=value:123')
        self.assertEqual(0, len(c.errors))
        self.assertParameter(
            'param1',
            'value:123',
            c.sections[0].parameters[0])

    def test_wrapping_value_with_single_quotes(self):
        c = self.parse("param = 'foo bar'")

        self.assertEqual(0, len(c.errors))
        self.assertParameter('param', 'foo bar', c.sections[0].parameters[0])
        self.assertEqual("'", c.sections[0].parameters[0].value.quotechar)

    def test_wrapping_value_with_single_quotes_and_trailing_whitespace(self):
        c = self.parse("param = 'foo bar'   ")

        self.assertEqual(0, len(c.errors))
        self.assertParameter('param', 'foo bar', c.sections[0].parameters[0])

    def test_wrapping_value_with_double_quotes(self):
        c = self.parse("param = \"foo bar\"")

        self.assertEqual(0, len(c.errors))
        self.assertParameter('param', 'foo bar', c.sections[0].parameters[0])
        self.assertEqual('"', c.sections[0].parameters[0].value.quotechar)

    def test_wrapping_value_with_double_quotes_and_trailing_whitespace(self):
        c = self.parse("param = \"foo bar\"   ")

        self.assertEqual(0, len(c.errors))
        self.assertParameter('param', 'foo bar', c.sections[0].parameters[0])

    def test_parsing_iolike_source(self):
        c = self.parse(StringIO("param1 = value1"))

        self.assertEqual(0, len(c.errors))

        self.assertParameter('param1', 'value1', c.sections[0].parameters[0])
        self.assertEqual(1, len(c.sections[0].parameters))

    def test_default_section_name(self):
        c = self.parse("param1 = value1")

        self.assertEqual('', c.sections[0].name.text)

    def test_parsing_with_section(self):
        c = self.parse("""
      [section1]
      param1 = value1
    """, margin=True)

        self.assertEqual(0, len(c.errors))
        self.assertEqual('section1', c.sections[0].name.text)
        self.assertEqual(1, len(c.sections[0].parameters))

    def test_parsing_with_same_section(self):
        c = self.parse("""
      [section1]
      param1 = value1
      param2 = value2
    """, margin=True)

        self.assertEqual(0, len(c.errors))
        self.assertEqual(2, len(c.sections[0].parameters))

    def test_parsing_with_different_sections(self):
        c = self.parse("""
      [section1]
      param1 = value1
      [section2]
      param2 = value2
    """, margin=True)

        self.assertEqual(0, len(c.errors))

        self.assertEqual('section1', c.sections[0].name.text)
        self.assertParameter('param1', 'value1', c.sections[0].parameters[0])
        self.assertEqual(1, len(c.sections[0].parameters))
        self.assertEqual('section2', c.sections[1].name.text)
        self.assertParameter('param2', 'value2', c.sections[1].parameters[0])
        self.assertEqual(1, len(c.sections[1].parameters))

    def test_whole_line_comments_starting_with_hash(self):
        c = self.parse("#param=value")
        self.assertEqual(0, len(c.errors))
        self.assertEqual(0, len(c.sections))

    def test_whole_line_comments_starting_with_semicolon(self):
        c = self.parse(";param=value")
        self.assertEqual(0, len(c.errors))
        self.assertEqual(0, len(c.sections))

    def test_hash_in_value_is_part_of_the_value(self):
        c = self.parse("param=value#123")
        self.assertEqual(0, len(c.errors))
        self.assertParameter("param", "value#123", c.sections[0].parameters[0])

    def test_multiline_value(self):
        c = self.parse("""
      param1 = line1
        line2
    """, margin=True)

        self.assertEqual(0, len(c.errors))
        self.assertParameter(
            'param1',
            'line1line2',
            c.sections[0].parameters[0])

    def test_multiline_value_finished_by_other_parameter(self):
        c = self.parse("""
      param1 = foo
        bar
      param2 = baz
    """, margin=True)

        self.assertEqual(0, len(c.errors))
        self.assertParameter('param1', 'foobar', c.sections[0].parameters[0])

    def test_multiline_value_finished_by_empty_line(self):
        c = self.parse("""
      param1 = foo
        bar

      param2 = baz
    """, margin=True)

        self.assertEqual(0, len(c.errors))
        self.assertParameter('param1', 'foobar', c.sections[0].parameters[0])

    def test_unclosed_section_causes_error(self):
        c = self.parse("[section1\nparam1=123")
        self.assertEqual(1, len(c.errors))

    def test_missing_equals_sign_or_colon_causes_error(self):
        c = self.parse("param1 value1")
        self.assertEqual(1, len(c.errors))

    def test_spaces_in_key_causes_error(self):
        c = self.parse("param 1 = value1")
        self.assertEqual(1, len(c.errors))

    def test_returning_multiple_errors(self):
        c = self.parse("[unclosed section\npararm 1 = value1")
        self.assertEqual(2, len(c.errors))

    def test_errors_doesnt_affect_valid_parameters(self):
        c = self.parse('param1 value1\nparam2 = value2')
        self.assertEqual(1, len(c.errors))
        self.assertParameter('param2', 'value2', c.sections[0].parameters[0])

    def _getattr(self, o, name):
        if name.find('.') != -1:
            parts = name.split('.')
            o = getattr(o, parts[0])
            if o is None:
                return None
            return self._getattr(o, '.'.join(parts[1:]))
        else:
            return getattr(o, name)

    def assertAttributes(self, attribute_values, subject):
        for attr, expected in attribute_values.items():
            actual = self._getattr(subject, attr)
            self.assertEqual(
                expected, actual,
                "%s expected to have %s = %s, but the value was %s" %
                (subject, attr, expected, actual))

    def assertParameter(self, name, value, o):
        self.assertAttributes({'name.text': name, 'value.text': value}, o)


if __name__ == '__main__':
    unittest.main()

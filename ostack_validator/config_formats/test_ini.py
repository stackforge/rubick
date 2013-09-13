import unittest

from ostack_validator.config_formats.ini import *

class IniConfigParserTests(unittest.TestCase):
  def setUp(self):
    self.parser = IniConfigParser()

  def parse(self, content):
    return self.parser.parse('test.conf', content)

  def test_parsing(self):
    result = self.parse("param1 = value1")

    self.assertTrue(result.success)

    config = result.value
    self.assertParameter('param1', 'value1', config.sections[0].parameters[0])
    self.assertEqual(1, len(config.sections[0].parameters))

  def test_parsing_iolike_source(self):
    r = self.parse(StringIO("param1 = value1"))

    self.assertTrue(r.success)

    c = r.value
    self.assertParameter('param1', 'value1', c.sections[0].parameters[0])
    self.assertEqual(1, len(c.sections[0].parameters))

  def test_default_section_name(self):
    r = self.parse("param1 = value1")

    self.assertEqual('', r.value.sections[0].name.text)

  def test_parsing_with_section(self):
    r = self.parse("""
      [section1]
      param1 = value1
    """)

    self.assertEqual('section1', r.value.sections[0].name.text)
    self.assertEqual(1, len(r.value.sections[0].parameters))

  def test_parsing_with_same_section(self):
    r = self.parse("""
      [section1]
      param1 = value1
      param2 = value2
    """)

    self.assertEqual(2, len(r.value.sections[0].parameters))

  def test_parsing_with_different_sections(self):
    r = self.parse("""
      [section1]
      param1 = value1
      [section2]
      param2 = value2
    """)

    c = r.value

    self.assertEqual('section1', c.sections[0].name.text)
    self.assertParameter('param1', 'value1', c.sections[0].parameters[0])
    self.assertEqual(1, len(c.sections[0].parameters))
    self.assertEqual('section2', c.sections[1].name.text)
    self.assertParameter('param2', 'value2', c.sections[1].parameters[0])
    self.assertEqual(1, len(c.sections[1].parameters))

  def test_whole_line_comments(self):
    r = self.parse("#param=value")
    self.assertEqual(0, len(r.value.sections))

  def test_hash_in_value_is_part_of_the_value(self):
    r = self.parse("param=value#123")
    self.assertParameter("param", "value#123", r.value.sections[0].parameters[0])

  def test_unclosed_section_causes_error(self):
    r = self.parse("[section1\nparam1=123")
    self.assertFalse(r.success)
    self.assertEqual(1, len(r.value))
  
  def test_missing_equals_sign_causes_error(self):
    r = self.parse("param1 value1")
    self.assertFalse(r.success)
    self.assertEqual(1, len(r.value))

  def test_spaces_in_key_causes_error(self):
    r = self.parse("param 1 = value1")
    self.assertFalse(r.success)
    self.assertEqual(1, len(r.value))

  def test_returning_multiple_errors(self):
    r = self.parse("[unclosed section\npararm 1 = value1")
    self.assertFalse(r.success)
    self.assertEqual(2, len(r.value))


  def _getattr(self, o, name):
    if name.find('.') != -1:
      parts = name.split('.')
      o = getattr(o, parts[0])
      if o == None:
        return None
      return self._getattr(o, '.'.join(parts[1:]))
    else:
      return getattr(o, name)

  def assertAttributes(self, attribute_values, subject):
    for attr, expected in attribute_values.items():
      actual = self._getattr(subject, attr)
      self.assertEqual(expected, actual, "%s expected to have %s = %s, but the value was %s" % (subject, attr, expected, actual))
  
  def assertParameter(self, name, value, o):
    self.assertAttributes({'name.text': name, 'value.text': value}, o)


if __name__ == '__main__':
  unittest.main()


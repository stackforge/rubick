# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.
import unittest

from rubick.config_model import Configuration
from rubick.schema import ConfigSchema, ConfigParameterSchema, \
    InvalidValueError


class ConfigurationTests(unittest.TestCase):
    section = 'section1'
    param = 'param1'
    fullparam = '%s.%s' % (section, param)
    value = 'foobar'
    default_value = 'bar123'

    def test_empty(self):
        c = Configuration()
        self.assertIsNone(c.get('section1.param1'))

    def test_storage(self):
        c = Configuration()
        c.set(self.fullparam, self.value)

        self.assertEqual(self.value, c.get(self.fullparam))

    def test_parameter_names_containing_sections(self):
        c = Configuration()
        c.set(self.fullparam, self.value)

        self.assertEqual(
            self.value, c.get('%s.%s' %
                              (self.section, self.param)))

    def test_parameter_with_default_section(self):
        c = Configuration()
        c.set(self.param, self.value)

        self.assertEqual(self.value, c.get(self.param))

    def test_explicit_default_on_get(self):
        c = Configuration()
        override_value = '12345'

        self.assertEqual(
            override_value,
            c.get(self.fullparam,
                  default=override_value))

    def test_default(self):
        c = Configuration()
        c.set_default(self.fullparam, self.default_value)

        self.assertEqual(self.default_value, c.get(self.fullparam))

    def test_normal_overrides_default(self):
        c = Configuration()
        c.set(self.fullparam, self.value)
        c.set_default(self.fullparam, self.default_value)

        self.assertEqual(self.value, c.get(self.fullparam))

    def test_contains(self):
        c = Configuration()
        self.assertFalse(c.contains(self.fullparam))

    def test_contains_default(self):
        c = Configuration()
        c.set_default(self.fullparam, self.default_value)

        self.assertTrue(c.contains(self.fullparam))
        self.assertFalse(c.contains(self.fullparam, ignoreDefault=True))

    def test_contains_normal(self):
        c = Configuration()
        c.set(self.fullparam, self.value)

        self.assertTrue(c.contains(self.fullparam))
        self.assertTrue(c.contains(self.fullparam, ignoreDefault=True))

    def test_is_default_returns_false_if_param_missing(self):
        c = Configuration()
        self.assertFalse(c.is_default(self.fullparam))

    def test_is_default_returns_true_if_only_default_value_set(self):
        c = Configuration()
        c.set_default(self.fullparam, self.default_value)

        self.assertTrue(c.is_default(self.fullparam))

    def test_is_default_returns_false_if_normal_value_set(self):
        c = Configuration()
        c.set(self.fullparam, self.value)

        self.assertFalse(c.is_default(self.fullparam))

    def test_is_default_returns_false_if_both_values_set(self):
        c = Configuration()
        c.set_default(self.fullparam, self.default_value)
        c.set(self.fullparam, self.value)

        self.assertFalse(c.is_default(self.fullparam))

    def test_subsection_set(self):
        c = Configuration()
        c.section(self.section).set(self.param, self.value)

        self.assertEqual(self.value, c.get(self.fullparam))

    def test_keys(self):
        c = Configuration()
        c.set_default('section1.param1', '123')
        c.set('section2.param1', '456')

        self.assertEqual(['section1', 'section2'], sorted(c.keys()))

    def test_subsection_keys(self):
        c = Configuration()
        c.set_default('%s.param1' % self.section, '123')
        c.set('%s.param2' % self.section, '456')

        self.assertEqual(
            ['param1', 'param2'], sorted(c.section(self.section).keys()))

    def test_subsection_items(self):
        c = Configuration()
        c.set('%s.param1' % self.section, 'value1')
        c.set_default('%s.param2' % self.section, 'value2')

        self.assertEqual(
            [('param1', 'value1'), ('param2', 'value2')],
            sorted(c.section(self.section).items()))

    def test_subsection_get(self):
        c = Configuration()

        c.set(self.fullparam, self.value)

        cs = c.section(self.section)
        self.assertEqual(self.value, cs.get(self.param))

    def test_getitem(self):
        c = Configuration()
        c.set(self.fullparam, self.value)

        self.assertEqual(self.value, c[self.fullparam])

    def test_subsection_getitem(self):
        c = Configuration()
        c.set(self.fullparam, self.value)

        cs = c.section(self.section)

        self.assertEqual(self.value, cs[self.param])

    def test_setitem(self):
        c = Configuration()

        c[self.fullparam] = self.value

        self.assertEqual(self.value, c.get(self.fullparam))

    def test_subsection_setitem(self):
        c = Configuration()

        cs = c.section(self.section)

        cs[self.param] = self.value

        self.assertEqual(self.value, c.get(self.fullparam))

    def test_section_in(self):
        c = Configuration()

        self.assertFalse(self.section in c)

        c.set(self.fullparam, self.value)
        self.assertTrue(self.section in c)

    def test_subsection_contains(self):
        c = Configuration()

        c.set('section1.param1', '123')
        c.set_default('section2.param2', '234')

        self.assertTrue('param1' in c.section('section1'))
        self.assertTrue('param2' in c.section('section2'))
        self.assertFalse('param1' in c.section('section2'))

    def test_returns_section_object_even_if_section_doesnot_exist(self):
        c = Configuration()
        self.assertIsNotNone(c.section('foo'))

    def test_template_substitution(self):
        c = Configuration()
        c.set('a', 'x')
        c.set('b', '$a')
        c.set('c', '$b')

        self.assertEqual('x', c.get('c'))

    def test_cycle_template_substitution_resolves_in_empty_string(self):
        c = Configuration()
        c.set('a', 'a$c')
        c.set('b', 'b$a')
        c.set('c', 'c$b')

        self.assertEqual('cba', c.get('c'))

    def test_getting_raw_values(self):
        c = Configuration()

        c.set('a', '$b')
        c.set('b', 'x')

        self.assertEqual('$b', c.get('a', raw=True))

    def test_typed_params(self):
        schema = ConfigSchema('test', '1.0', 'ini', [
            ConfigParameterSchema('param1', type='integer', section='DEFAULT')
        ])

        c = Configuration(schema)

        c.set('param1', '123')

        self.assertEqual(123, c.get('param1'))

    def test_typed_params_update(self):
        schema = ConfigSchema('test', '1.0', 'ini', [
            ConfigParameterSchema('param1', type='integer', section='DEFAULT')
        ])

        c = Configuration(schema)

        c.set('param1', '123')

        self.assertEqual(123, c.get('param1'))

        c.set('param1', '456')

        self.assertEqual(456, c.get('param1'))

    def test_type_for_unknown_param(self):
        schema = ConfigSchema('test', '1.0', 'ini', [])

        c = Configuration(schema)

        c.set('param1', '123')

        self.assertEqual('123', c.get('param1'))

    def test_typed_param_with_invalid_value_returns_string_value(self):
        schema = ConfigSchema('test', '1.0', 'ini', [
            ConfigParameterSchema('param1', type='integer', section='DEFAULT')
        ])

        c = Configuration(schema)

        c.set('param1', '123a')

        self.assertEqual('123a', c.get('param1'))

    def test_getting_typed_param_raw_value(self):
        schema = ConfigSchema('test', '1.0', 'ini', [
            ConfigParameterSchema('param1', type='integer', section='DEFAULT')
        ])

        c = Configuration(schema)

        c.set('param1', '123')

        self.assertEqual('123', c.get('param1', raw=True))

    def test_validate_returns_none_if_value_is_valid(self):
        schema = ConfigSchema('test', '1.0', 'ini', [
            ConfigParameterSchema('param1', type='integer', section='DEFAULT')
        ])

        c = Configuration(schema)

        c.set('param1', '123')

        self.assertIsNone(c.validate('param1'))

    def test_validate_returns_error_if_valid_is_invalid(self):
        schema = ConfigSchema('test', '1.0', 'ini', [
            ConfigParameterSchema('param1', type='integer', section='DEFAULT')
        ])

        c = Configuration(schema)

        c.set('param1', 'abc')

        self.assertTrue(isinstance(c.validate('param1'), InvalidValueError))

    def test_validate_returns_none_for_unknown_param(self):
        schema = ConfigSchema('test', '1.0', 'ini', [])

        c = Configuration(schema)

        c.set('param1', '123')

        self.assertIsNone(c.validate('param1'))

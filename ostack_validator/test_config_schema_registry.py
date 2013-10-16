from ostack_validator.schema import ConfigSchemaRegistry, Version
from ostack_validator.common import find

import unittest


class ConfigSchemaRegistryTests(unittest.TestCase):

    def test_sample(self):
        nova = ConfigSchemaRegistry.register_schema(project='nova')

        nova.version('1.0.0')
        nova.section('DEFAULT')
        nova.param(name='verbose', type='boolean')
        nova.param(name='rabbit_host', type='address')

        nova.version('1.1.0')
        nova.section('DEFAULT')
        nova.param(name='verbose', type='boolean', default=False)
        nova.remove_param('rabbit_host')

        nova.commit()

        schema10 = ConfigSchemaRegistry.get_schema(
            project='nova', version='1.0.0')

        self.assertEqual(Version('1.0.0'), schema10.version)
        self.assertEqual('ini', schema10.format)

        verbose_param = find(
            schema10.parameters,
            lambda p: p.name == 'verbose')
        self.assertIsNotNone(verbose_param)
        self.assertEqual('boolean', verbose_param.type)
        self.assertEqual(None, verbose_param.default)

        rabbit_host_param = find(
            schema10.parameters,
            lambda p: p.name == 'rabbit_host')
        self.assertIsNotNone(rabbit_host_param)
        self.assertEqual('address', rabbit_host_param.type)

        schema11 = ConfigSchemaRegistry.get_schema(
            project='nova', version='1.1.0')

        verbose_param11 = find(
            schema11.parameters,
            lambda p: p.name == 'verbose')
        self.assertIsNotNone(verbose_param11)
        self.assertEqual(False, verbose_param11.default)

        rabbit_host_param11 = find(
            schema11.parameters,
            lambda p: p.name == 'rabbit_host')
        self.assertIsNone(rabbit_host_param11)


if __name__ == '__main__':
    unittest.main()

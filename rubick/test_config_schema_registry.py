from rubick.schema import ConfigSchemaRegistry, Version
from rubick.common import find

import unittest


class ConfigSchemaRegistryTests(unittest.TestCase):

    def test_sample(self):
        nova = ConfigSchemaRegistry.register_schema(project='nova')

        with nova.version('1.0.0', checkpoint=True) as cfg:
            cfg.param(name='verbose', type='boolean')
            cfg.param(name='rabbit_host', type='address')

        with nova.version('1.1.0') as cfg:
            cfg.param(name='verbose', type='boolean', default=False)
            cfg.remove_param('rabbit_host')

        schema10 = ConfigSchemaRegistry.get_schema(project='nova',
                                                   version='1.0.0')

        self.assertEqual(Version('1.0.0'), schema10.version)
        self.assertEqual('ini', schema10.format)

        def find_param(params, name):
            return find(params, lambda p: p.name == name)

        verbose_param = find_param(schema10.parameters, 'verbose')
        self.assertIsNotNone(verbose_param)
        self.assertEqual('boolean', verbose_param.type)
        self.assertEqual(None, verbose_param.default)

        rabbit_host_param = find_param(schema10.parameters, 'rabbit_host')
        self.assertIsNotNone(rabbit_host_param)
        self.assertEqual('address', rabbit_host_param.type)

        schema11 = ConfigSchemaRegistry.get_schema(project='nova',
                                                   version='1.1.0')

        verbose_param11 = find_param(schema11.parameters, 'verbose')
        self.assertIsNotNone(verbose_param11)
        self.assertEqual(False, verbose_param11.default)

        rabbit_host_param11 = find_param(schema11.parameters, 'rabbit_host')
        self.assertIsNone(rabbit_host_param11)


if __name__ == '__main__':
    unittest.main()

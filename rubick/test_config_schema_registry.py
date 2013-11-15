import unittest
from contextlib import contextmanager

from rubick.schema import ConfigSchemaRegistry, Version
from rubick.common import find


class TestConfigSchemaLoader(object):
    def __init__(self):
        super(TestConfigSchemaLoader, self).__init__()
        self._records = []

    @contextmanager
    def version(self, version, checkpoint=False):
        self._current_version = dict(version=version, checkpoint=checkpoint,
                                     added=[], removed=[])
        self._records.append(self._current_version)
        yield
        self._current_version = None

    def param(self, name, type, default=None, description=None):
        self._current_version['added'].append(
            dict(name=name, type=type, default=default,
                 description=description))

    def removed_param(self, name):
        self._current_version['removed'].append(name)

    def load(self, project, configname):
        return self._records


class ConfigSchemaRegistryTests(unittest.TestCase):

    def test_sample(self):
        loader = TestConfigSchemaLoader()
        with loader.version('1.0.0', checkpoint=True):
            loader.param('verbose', type='boolean')
            loader.param('rabbit_host', type='address')

        with loader.version('1.1.0'):
            loader.param('verbose', type='boolean', default=False)
            loader.removed_param('rabbit_host')

        schema10 = ConfigSchemaRegistry.get_schema(
            project='nova', version='1.0.0', schema_loader=loader)

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

        schema11 = ConfigSchemaRegistry.get_schema(
            project='nova', version='1.1.0', schema_loader=loader)

        verbose_param11 = find_param(schema11.parameters, 'verbose')
        self.assertIsNotNone(verbose_param11)
        self.assertEqual(False, verbose_param11.default)

        rabbit_host_param11 = find_param(schema11.parameters, 'rabbit_host')
        self.assertIsNone(rabbit_host_param11)


if __name__ == '__main__':
    unittest.main()

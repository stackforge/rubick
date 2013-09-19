from ostack_validator.model_parser import ModelParser

import unittest

class ModelParserTests(unittest.TestCase):
  def test_sample(self):
    parser = ModelParser()

    model = parser.parse('config_samples/config')

    for host in model.hosts:
      self.assertTrue(host.name in ['host1', 'host2'])

      for component in host.components:
        self.assertTrue(component.name in ['cinder', 'glance', 'horizon', 'keystone', 'nova', 'quantum', 'swift'])

      self.assertTrue(len(host.components) > 0)

    self.assertEqual(2, len(model.hosts))

if __name__ == '__main__':
  unittest.main()


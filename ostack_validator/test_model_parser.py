from ostack_validator.model_parser import ModelParser

import unittest

class ModelParserTests(unittest.TestCase):
  def test_sample(self):
    parser = ModelParser()

    model = parser.parse('config')

    for host in model.hosts:
      print('Host %s' % host.name)

      for component in host.components:
        print('Component %s version %s' % (component.name, component.version))

        print(component.get_config())

if __name__ == '__main__':
  unittest.main()

